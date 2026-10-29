"""Reconcile RewardGuard-owned checks/comments for one immutable reviewed head."""
from __future__ import annotations
import argparse
import os
import re
import sys
from . import content_checks, report as reporting
from .github import Client
from .models import Finding, Report, RewardGuardError

PREFIX = 'rewardguard:content:'


def current(client, head, pr):
    if pr is None:
        return True
    return client.get(f'pulls/{pr}').get('head', {}).get('sha') == head


def _owned(check):
    return (check.get('app', {}).get('slug') == 'github-actions'
            and isinstance(check.get('external_id'), str) and check['external_id'].startswith(PREFIX)
            and type(check.get('id')) is int and check['id'] > 0)


def publish(client, data, head, *, pr=None, checks=True, comment=False):
    if not re.fullmatch(r'[0-9a-f]{40}', head) or data.get('run_identity', {}).get('head') != head:
        raise RewardGuardError('Report head does not match publication head')
    if not current(client, head, pr):
        return 'stale'
    if checks:
        desired = content_checks.build_checks(data)
        existing = client.pages(f'commits/{head}/check-runs?filter=all', 'check_runs')
        owned = [c for c in existing if _owned(c) and c.get('head_sha') == head]
        retained = set()
        for check in desired:
            if not current(client, head, pr):
                return 'stale'
            external = PREFIX + check['name']
            matches = sorted((c for c in owned if c['external_id'] == external), key=lambda c: c['id'])
            check['output']['summary'] = content_checks.display_limit(check['output']['summary'], 60000)
            check['output']['title'] = content_checks.display_limit(check['output']['title'], 250)
            payload = dict(check, external_id=external, status='completed')
            if matches:
                chosen = matches[-1]
                retained.add(chosen['id'])
                client.write(f"check-runs/{chosen['id']}", payload, 'PATCH')
            else:
                client.write('check-runs', dict(payload, head_sha=head))
        for old in owned:
            if old['id'] in retained:
                continue
            if not current(client, head, pr):
                return 'stale'
            client.write(f"check-runs/{old['id']}", {'status': 'completed', 'conclusion': 'neutral',
                'output': {'title': 'Superseded RewardGuard scope',
                           'summary': 'This previous scope is absent or duplicated in the current exact-head report; it makes no current verdict.'}}, 'PATCH')
    if comment and pr:
        # Human text containing the marker cannot authorize edits to that human's comment.
        comments = client.pages(f'issues/{pr}/comments')
        matches = sorted((c for c in comments if isinstance(c.get('body'), str)
            and c['body'].startswith(reporting.MARKER)
            and c.get('user', {}).get('login') == 'github-actions[bot]'
            and c.get('user', {}).get('type') == 'Bot'
            and type(c.get('id')) is int), key=lambda c: c['id'])
        rep = Report(**{k: data[k] for k in ('errors', 'notes', 'content', 'code', 'usage', 'run_identity', 'diagnostics') if k in data},
                     findings=[Finding(**f) for f in data.get('findings', [])])
        body = content_checks.display_limit(reporting.markdown(rep), 60000)
        if not current(client, head, pr):
            return 'stale'
        if matches:
            client.write(f"issues/comments/{matches[-1]['id']}", {'body': body}, 'PATCH')
            for duplicate in matches[:-1]:
                if not current(client, head, pr):
                    return 'stale'
                client.write(f"issues/comments/{duplicate['id']}",
                             {'body': 'Superseded RewardGuard report; see the current bot report in this PR.'}, 'PATCH')
        else:
            client.write(f'issues/{pr}/comments', {'body': body})
    # Detect head movement during the final write as well as between writes.
    return 'published' if current(client, head, pr) else 'stale'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    parser.add_argument('--head', required=True)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--pr', type=int)
    parser.add_argument('--checks', choices=('true', 'false'), default='true')
    parser.add_argument('--comment', choices=('true', 'false'), default='false')
    parser.add_argument('--preflight', action='store_true')
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r'[0-9a-f]{40}', args.head) or (args.pr is not None and args.pr <= 0):
            raise RewardGuardError('Invalid resolved head or PR number')
        client = Client(args.repo)
        if args.preflight:
            state = 'current' if current(client, args.head, args.pr) else 'stale'
        else:
            state = publish(client, content_checks.load_report(args.report), args.head, pr=args.pr,
                            checks=args.checks == 'true', comment=args.comment == 'true')
        if os.environ.get('GITHUB_OUTPUT'):
            with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
                output.write(f'state={state}\n')
        print('RewardGuard publication: ' + state)
        return 0
    except (OSError, ValueError, TypeError, KeyError, RewardGuardError) as error:
        print(f'::error::RewardGuard publication/preflight failed ({type(error).__name__}); inspect original review errors.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
