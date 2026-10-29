"""Request/explanation reuse at fake paid boundaries; no real providers."""
import json
import subprocess
from dataclasses import replace
import pytest
from rewardguard import config, content_review, content_rules, judge, explainer, gitops
from rewardguard.models import RewardGuardError
from conftest import FakeJev
from test_publication_boundary import git

RULE_IDS = {'CG_AMBIGUOUS_MEANING', 'CG_REDUNDANT_STAGING'}


@pytest.fixture
def setup(tmp_path, monkeypatch):
    repo = tmp_path / 'repo'; repo.mkdir()
    git(repo, 'init', '-qb', 'main'); git(repo, 'config', 'user.name', 'Test')
    git(repo, 'config', 'user.email', 'test@example.test')
    (repo / 'page.md').write_text('# Product\n\nOriginal copy.\n')
    git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'base')
    base = git(repo, 'rev-parse', 'HEAD')
    (repo / 'page.md').write_text('# Product\n\nAlpha new paragraph.\n\nBeta new paragraph.\n')
    git(repo, 'commit', '-qam', 'public change')
    cfg = config.Config(None, [], run_tests=False)
    cfg.content.publications = [config.Publication('site', ('*.md',), 'page', '/')]
    cfg.content.packs = ['writing', 'style']
    rules = [r for r in content_rules.all_rules() if r.id in RULE_IDS]
    monkeypatch.setattr(content_rules, 'all_rules', lambda: rules)
    monkeypatch.setenv('REWARDGUARD_CACHE_DIR', str(tmp_path / 'cache'))
    monkeypatch.setattr(explainer, '_which', lambda _: '/fake/claude')
    api = FakeJev(rules={(key, ''): value for r in rules for key, value in
                        [('applies_' + r.id, .9), (r.id, .8)]})
    explanation_calls = []
    def run_cli(cmd, **kwargs):
        explanation_calls.append(kwargs['input'])
        prompt = kwargs['input']; rule = prompt.split('Requested rule: ')[1].split('\n')[0]
        body = json.loads(prompt.split('unit_relative_source.\n', 1)[1])
        code = body['unit_relative_source']['1']
        payload = {'structured_output': {'issues': [{'rule': rule, 'line': 1, 'code': code,
                    'problem': 'Concrete defect in this unit.', 'fix': 'Correct this unit.'}]}}
        return subprocess.CompletedProcess(cmd, 0, json.dumps(payload), '')
    monkeypatch.setattr(explainer, '_run', run_cli)
    def review(description=''):
        client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
        haiku = explainer.HaikuExplainer(cfg, token='fake-oauth', cache_signing_key='signing-key', repository='test/repo')
        return content_review.review(str(repo), base, 'HEAD', cfg, gitops.changed_files(str(repo), base, 'HEAD'),
                                    description, client=client, haiku=haiku, log=lambda _: None)
    return repo, cfg, rules, api, explanation_calls, review


@pytest.mark.parametrize('probability', [.2, .6, .8])
def test_restored_clean_warning_failure_and_explanations_make_zero_calls(setup, probability):
    repo, cfg, rules, api, calls, review = setup
    for rule in rules: api.rules[(rule.id, '')] = probability
    first = review('Initial PR description')
    paid = (len(api.calls), len(calls))
    second = review('Entirely unrelated edited PR description')
    assert first.status == second.status == 'reviewed'
    assert [{k: v for k, v in row.items() if k != 'reused'} for row in first.coverage] == [
        {k: v for k, v in row.items() if k != 'reused'} for row in second.coverage]
    assert second.result_cache_hits == 4
    assert all(row.get('reused') is True for row in second.coverage if row['status'] == 'evaluated')
    assert [f.to_dict() for f in first.findings] == [f.to_dict() for f in second.findings]
    assert (len(api.calls), len(calls)) == paid
    assert bool(first.findings) == (probability >= .6)
    assert all('page.md' not in body['state'] and git(repo, 'rev-parse', 'HEAD') not in body['state'] for body in api.calls)


def test_paragraph_edit_only_reissues_that_unit_and_move_reanchors(setup):
    repo, cfg, rules, api, calls, review = setup
    first = review(); before = len(api.calls), len(calls)
    (repo / 'page.md').write_text('# Product\n\nAlpha edited paragraph.\n\nBeta new paragraph.\n')
    git(repo, 'commit', '-qam', 'one paragraph')
    review()
    assert len(api.calls) - before[0] == 4  # applicability + grade, two rules, one changed unit
    assert len(calls) - before[1] == 2
    before = len(api.calls), len(calls)
    (repo / 'page.md').write_text('\n\n# Product\n\nAlpha edited paragraph.\n\nBeta new paragraph.\n')
    git(repo, 'commit', '-qam', 'line move')
    moved = review()
    assert (len(api.calls), len(calls)) == before
    assert {f.line for f in first.findings} == {3, 5}
    assert {f.line for f in moved.findings} == {5, 7}


def test_rule_change_does_not_reissue_another_rule(setup):
    repo, cfg, rules, api, calls, review = setup
    review(); before = len(api.calls), len(calls)
    rules[0] = replace(rules[0], statement=rules[0].statement + ' Focus revised.', revision='new-rule-revision')
    review()
    fresh = api.calls[before[0]:]
    assert len(fresh) == 4 and len(calls) - before[1] == 2
    assert all(all(rules[1].id not in key for key in body['questions']) for body in fresh)


def test_deleted_unit_removes_stale_findings_without_refetching_survivor(setup):
    repo, cfg, rules, api, calls, review = setup
    review(); before = len(api.calls), len(calls)
    (repo / 'page.md').write_text('# Product\n\nBeta new paragraph.\n')
    git(repo, 'commit', '-qam', 'delete paragraph')
    result = review()
    assert (len(api.calls), len(calls)) == before
    assert len(result.findings) == 2 and {f.line for f in result.findings} == {3}
    assert all('Alpha' not in str(f.details) for f in result.findings)


def test_path_move_reanchors_and_ignores_location_for_pure_copy(setup):
    repo, cfg, rules, api, calls, review = setup
    review(); before = len(api.calls), len(calls)
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'rename')
    result = review()
    assert (len(api.calls), len(calls)) == before
    assert {f.file for f in result.findings} == {'moved.md'}


def test_completed_results_survive_later_explanation_failure(setup, monkeypatch):
    repo, cfg, rules, api, calls, review = setup
    original = explainer._run
    def fail_second(*args, **kwargs):
        if calls: raise OSError('provider unavailable')
        return original(*args, **kwargs)
    monkeypatch.setattr(explainer, '_run', fail_second)
    result = review()
    assert result.status == 'error' and result.errors
    assert len(result.findings) == 2
    assert result.findings[0].details
    assert result.findings[1].probability == .8
    assert sum(r['status'] == 'evaluated' for r in result.coverage) == 2


def test_rule_inventory_keeps_all_ids_and_explicit_outside_scope():
    inventory = content_rules.inventory()
    assert len(inventory) == 243
    assert len({r['id'] for r in inventory}) == 243
    assert all(r['revision'] and r['scope'] in {'public_enabled', 'adopted_policy_only', 'outside_website'} for r in inventory)
    assert all(r['scope'] == 'outside_website' and not r['artifact_types'] for r in inventory
               if r['pack'] in {'research', 'seo_research', 'ads', 'email', 'sales', 'briefs'})


def test_move_only_pr_restores_prior_results_without_provider_work(setup):
    repo, cfg, rules, api, calls, review = setup
    first = review(); before = len(api.calls), len(calls)
    move_base = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'move-only PR')
    client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    haiku = explainer.HaikuExplainer(cfg, token='fake-oauth', cache_signing_key='signing-key', repository='test/repo')
    result = content_review.review(str(repo), move_base, 'HEAD', cfg,
        gitops.changed_files(str(repo), move_base, 'HEAD'), client=client, haiku=haiku)
    assert (len(api.calls), len(calls)) == before
    assert len(result.findings) == len(first.findings) == 4
    assert {f.file for f in result.findings} == {'moved.md'}
    assert {f.line for f in result.findings} == {3, 5}


def test_move_only_uncached_local_units_are_explicitly_unreviewed(setup):
    repo, cfg, rules, api, calls, review = setup
    move_base = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'move-only PR')
    client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    result = content_review.review(str(repo), move_base, 'HEAD', cfg,
        gitops.changed_files(str(repo), move_base, 'HEAD'), client=client)
    assert not api.calls and not calls
    assert not result.findings and result.status == 'skipped'
    assert all(row['status'] == 'unchanged' for row in result.coverage)
    assert any(row.get('cache_miss') for row in result.coverage)


def test_explainer_change_does_not_invalidate_completed_clean_jev(setup):
    repo, cfg, rules, api, calls, review = setup
    for rule in rules: api.rules[(rule.id, '')] = .2
    review(); before = len(api.calls), len(calls)
    cfg.explainer_model = 'another-explainer'
    result = review()
    assert result.status == 'reviewed' and not result.findings
    assert (len(api.calls), len(calls)) == before


def test_explainer_change_reuses_jev_but_refreshes_explanation(setup):
    repo, cfg, rules, api, calls, review = setup
    review(); before = len(api.calls), len(calls)
    cfg.explainer_model = 'another-explainer'
    result = review()
    assert result.status == 'reviewed' and len(result.findings) == 4
    assert len(api.calls) == before[0]
    assert len(calls) == before[1] + 4


def test_authenticated_malformed_final_result_is_revalidated_against_jev(setup):
    from rewardguard.content_results import ContentResults
    from rewardguard.review_cache import repository_identity
    repo, cfg, rules, api, calls, review = setup
    review(); before = len(api.calls), len(calls)
    signer = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    records = ContentResults(cfg, repository_identity(str(repo)), signer)
    state = api.calls[0]['state']
    body = records.body(state, rules[0])
    # Even a correctly signed but malformed completed record cannot clear a Jev failure.
    records.cache.save(body, {'coverage': [{'rule': rules[0].id, 'status': 'evaluated', 'probability': .8}],
                             'findings': [], 'explanation_identity': records.explanation_identity(rules[0])})
    result = review()
    assert len(result.findings) == 4 and all(f.probability == .8 for f in result.findings)
    assert (len(api.calls), len(calls)) == before  # original authenticated provider-stage records recover it


def test_move_with_changed_explainer_preserves_authenticated_jev_findings(setup):
    repo, cfg, rules, api, calls, review = setup
    original = review(); before = len(api.calls), len(calls)
    move_base = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'move-only PR')
    cfg.explainer_model = 'changed-explainer'
    client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    result = content_review.review(str(repo), move_base, 'HEAD', cfg,
        gitops.changed_files(str(repo), move_base, 'HEAD'), client=client)
    assert (len(api.calls), len(calls)) == before
    assert len(result.findings) == len(original.findings) == 4
    assert all(f.probability == .8 and f.severity == 'fail' for f in result.findings)
    assert all(not f.details for f in result.findings)
    assert all(row['explanation_status'] == 'not_evaluated' for row in result.coverage if row['status'] == 'evaluated')


@pytest.mark.parametrize('multiple_fields', [False, True])
def test_explanation_failure_then_move_recovers_known_jev_grade_only(setup, monkeypatch, multiple_fields):
    repo, cfg, rules, api, calls, review = setup
    rules[:] = rules[:1]
    if multiple_fields:
        monkeypatch.setitem(content_review.FIELDS, rules[0].id, ('first', 'pending'))
        api.rules[(rules[0].id + '__first', '')] = .8
        api.rules[(rules[0].id + '__pending', '')] = .2
    def fail(*args, **kwargs):
        raise OSError('simulated explanation failure')
    monkeypatch.setattr(explainer, '_run', fail)
    original = review()
    assert original.status == 'error' and original.findings[0].probability == .8
    before = len(api.calls), len(calls)
    move_base = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'move after failure')
    client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    result = content_review.review(str(repo), move_base, 'HEAD', cfg,
        gitops.changed_files(str(repo), move_base, 'HEAD'), client=client)
    assert (len(api.calls), len(calls)) == before
    assert len(result.findings) == 1 and result.findings[0].probability == .8
    assert result.findings[0].severity == 'fail' and result.findings[0].file == 'moved.md'
    evaluated = [row for row in result.coverage if row['status'] == 'evaluated']
    assert evaluated and all(row['explanation_status'] == 'not_evaluated' for row in evaluated)
    if multiple_fields:
        assert any(row.get('instance') == 'pending' and row['status'] == 'not_evaluated'
                   for row in result.coverage)


def test_partial_clean_grade_replay_keeps_other_required_fields_unverified(setup, monkeypatch):
    from rewardguard import content_checks
    repo, cfg, rules, api, calls, review = setup
    rules[:] = rules[:1]
    monkeypatch.setitem(content_review.FIELDS, rules[0].id, ('first', 'pending'))
    api.rules[(rules[0].id + '__first', '')] = .2
    original_ask = judge.JevClient.ask
    def stop_on_pending(self, state, questions):
        if rules[0].id + '__pending' in questions:
            raise RewardGuardError('simulated later Jev failure')
        return original_ask(self, state, questions)
    monkeypatch.setattr(judge.JevClient, 'ask', stop_on_pending)
    first = review()
    assert first.status == 'error' and not first.findings
    before = len(api.calls), len(calls)
    move_base = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'mv', 'page.md', 'moved.md'); git(repo, 'commit', '-qm', 'move partial evaluation')
    client = judge.JevClient(cfg, api_key='signing-key', opener=api, repository='test/repo', phase='content')
    result = content_review.review(str(repo), move_base, 'HEAD', cfg,
        gitops.changed_files(str(repo), move_base, 'HEAD'), client=client)
    assert (len(api.calls), len(calls)) == before
    assert result.grade_cache_hits == 1 and result.result_cache_hits == 0
    assert any(row['status'] == 'evaluated' and row['probability'] == .2 and not row['result_complete'] for row in result.coverage)
    assert any(row.get('instance') == 'pending' and row['status'] == 'not_evaluated' for row in result.coverage)
    checks = content_checks.build_checks({'content': result.to_dict(), 'findings': [], 'notes': result.notes})
    assert next(check for check in checks if check['name'].endswith(rules[0].id))['conclusion'] == 'neutral'
