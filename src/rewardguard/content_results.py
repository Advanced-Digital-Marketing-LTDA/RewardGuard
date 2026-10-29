"""Authenticated final unit/rule results, with relative anchors and strict replay checks.

The immutable records are their own recoverable index. No commit, path, release
version, or wall-clock TTL is part of semantic identity. Provider request caches
remain authoritative when a final record is absent or an explanation input changes.
"""
import json
import math
import os

from . import explainer
from .models import Finding, grade
from .review_cache import ReviewCache
from .content_publications import digest


class ContentResults:
    def __init__(self, cfg, repository, client=None):
        key = getattr(getattr(client, 'cache', None), 'key', None)
        key = key.decode() if isinstance(key, bytes) else os.environ.get('TYPESAFE_API_KEY')
        self.cache = ReviewCache(key, cfg.api_url, cfg.cache_epoch, cfg.cache_max_age_seconds,
                                 repository=repository, namespace='content-unit-results') if key else None
        self.cfg = cfg
        self.reason = 'signing_credential_unavailable' if not key else 'not_checked'

    def body(self, state, rule):
        from .content_review import BOUNDARY, ROUTING_BOUNDARY, FIELDS
        return json.dumps({'revision': 'content-final-1', 'state': state,
            'rule': rule.id, 'rule_revision': rule.revision, 'statement': rule.statement,
            'model': self.cfg.model, 'endpoint': self.cfg.api_url,
            'boundary': BOUNDARY, 'routing_boundary': ROUTING_BOUNDARY,
            'scope': rule.scope, 'fields': FIELDS.get(rule.id, ('',))}, sort_keys=True).encode()

    def explanation_identity(self, rule):
        return digest({'revision': 'content-explanation-1', 'model': self.cfg.explainer_model,
            'effort': self.cfg.explainer_effort, 'system': explainer.CONTENT_SYSTEM,
            'instruction': explainer.CONTENT_INSTRUCTION, 'schema': explainer._schema(rule.id),
            'rubric': rule.rubric, 'rule_revision': rule.revision})

    def _explained_body(self, body, rule):
        return body + b'\0content-explanation:' + self.explanation_identity(rule).encode()

    def load(self, body, rule, unit, *, preserve_grade=False):
        if self.cache is None:
            return None
        reasons = []
        payload = self.cache.load(self._explained_body(body, rule), diagnostic=reasons.append)
        if payload is None:
            payload = self.cache.load(body, diagnostic=reasons.append)
        self.reason = reasons[-1] if reasons else 'record_absent'
        if payload is None:
            return self._load_checkpoint(body, rule, unit) if preserve_grade else None
        if not self._valid(payload, rule, unit):
            self.cache.reject(body)
            self.reason = 'invalid_completed_unit_result'
            return self._load_checkpoint(body, rule, unit) if preserve_grade else None
        if payload['findings'] and payload['explanation_identity'] != self.explanation_identity(rule):
            self.reason = 'explanation_inputs_changed'
            # Keep the authenticated grade and let the caller refresh only its explanation.
            return {**payload, 'findings': [{**f, 'details': []} for f in payload['findings']],
                    'explanation_stale': True}
        return payload

    @staticmethod
    def _valid(payload, rule, unit):
        from .content_review import _ground_details
        def probability(value):
            return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1
        if (not isinstance(payload, dict) or set(payload) != {'coverage', 'findings', 'explanation_identity'}
                or not isinstance(payload['coverage'], list) or not payload['coverage']
                or not isinstance(payload['findings'], list)
                or not isinstance(payload['explanation_identity'], str)):
            return False
        for row in payload['coverage']:
            if (not isinstance(row, dict) or row.get('rule') != rule.id
                    or not isinstance(row.get('status'), str) or row.get('status') not in {'evaluated', 'not_applicable', 'not_evaluated'}
                    or any(k in row for k in ('file', 'line', 'unit'))):
                return False
            if row['status'] == 'evaluated' and not probability(row.get('probability')):
                return False
            if 'applicability' in row and not probability(row['applicability']):
                return False
        for finding in payload['findings']:
            if (not isinstance(finding, dict) or set(finding) != {'rule', 'probability', 'message', 'details'}
                    or finding['rule'] != rule.id or not probability(finding['probability'])
                    or grade(finding['probability']) is None or not isinstance(finding['message'], str)
                    or not isinstance(finding['details'], list)
                    or not all(explainer._valid_detail(d) for d in finding['details'])):
                return False
            if _ground_details(finding['details'], unit['anchors']) != finding['details']:
                return False
            if not any(row['status'] == 'evaluated' and row['probability'] == finding['probability']
                       for row in payload['coverage']):
                return False
        # A valid signed result must not silently lose a completed Jev warning/failure.
        return sum(row['status'] == 'evaluated' and grade(row['probability']) is not None
                   for row in payload['coverage']) == len(payload['findings'])

    def _payload(self, rule, unit, coverage, findings):
        def relative(detail):
            return next(number for number, source in unit['line_map'].items()
                        if source == detail['line'] and detail['code'].strip() in unit['anchors'][number].strip())
        return {'coverage': [{k: v for k, v in row.items() if k not in {'file', 'line', 'unit'}} for row in coverage],
            'findings': [{'rule': f.rule, 'probability': f.probability, 'message': f.message,
                          'details': [{**d, 'line': relative(d)} for d in f.details or []]} for f in findings],
            'explanation_identity': self.explanation_identity(rule)}

    def save(self, body, rule, unit, coverage, findings):
        if self.cache is None or not coverage:
            return
        payload = self._payload(rule, unit, coverage, findings)
        if self._valid(payload, rule, unit):
            target = self._explained_body(body, rule) if findings else body
            self.cache.save(target, payload)

    def save_refreshed_explanations(self, body, rule, unit, payload):
        if self.cache is not None and self._valid(payload, rule, unit):
            self.cache.save(self._explained_body(body, rule), payload)

    def checkpoint(self, body, rule, unit, coverage, findings):
        """Persist completed Jev propositions before any explanation can fail."""
        from .content_review import FIELDS
        if self.cache is None or not any(row['status'] == 'evaluated' for row in coverage):
            return
        payload = self._payload(rule, unit, coverage, findings)
        rows = payload['coverage']
        finished = {row.get('instance') for row in rows}
        for instance in FIELDS.get(rule.id, ('',)):
            if instance not in finished:
                rows.append({'rule': rule.id, 'instance': instance, 'status': 'not_evaluated',
                             'reason': 'Required proposition was not completed before the previous evaluation stopped'})
        for row in rows:
            row['result_complete'] = False
            row['reuse_stage'] = 'jev_grade_checkpoint'
        if self._valid(payload, rule, unit):
            self.cache.save(self._checkpoint_body(body, self._checkpoint_stage(rows)), payload)

    @staticmethod
    def _checkpoint_stage(rows):
        # Each completed proposition advances an immutable snapshot. A completed
        # explanation advances it once more, without replacing a signed grade.
        return sum(2 if row['status'] == 'evaluated' else 0 for row in rows) + sum(
            row.get('explanation_status') == 'completed' for row in rows)

    @staticmethod
    def _checkpoint_body(body, stage):
        return json.dumps({'checkpoint_revision': 2, 'stage': stage,
                           'body': body.decode('utf-8')}, sort_keys=True).encode()

    def _load_checkpoint(self, body, rule, unit):
        from .content_review import FIELDS
        fields = set(FIELDS.get(rule.id, ('',)))
        # Highest progress wins; simultaneous writers cannot erase earlier stages.
        candidates = [(self._checkpoint_body(body, stage), stage)
                      for stage in range(3 * len(fields), 1, -1)]
        candidates.append((b'grade-checkpoint-1\0' + body, None))
        for checkpoint_body, stage in candidates:
            payload = self.cache.load(checkpoint_body)
            if payload is None:
                continue
            if (not self._valid(payload, rule, unit)
                    or {row.get('instance') for row in payload['coverage']} != fields
                    or len(payload['coverage']) != len(fields)
                    or any(row.get('result_complete') is not False for row in payload['coverage'])
                    or (stage is not None and self._checkpoint_stage(payload['coverage']) != stage)):
                self.cache.reject(checkpoint_body)
                self.reason = 'invalid_jev_grade_checkpoint'
                continue
            if payload['explanation_identity'] != self.explanation_identity(rule):
                payload = {**payload, 'findings': [{**f, 'details': []} for f in payload['findings']],
                           'explanation_stale': True}
            return {**payload, 'grade_checkpoint': True}
        return None

    @staticmethod
    def restore(payload, result, path, unit):
        if payload.get('grade_checkpoint'):
            result.grade_cache_hits += 1
            result.notes.append('Authenticated completed Jev propositions restored; unfinished propositions/explanations remain explicitly unverified.')
        else:
            result.result_cache_hits += 1
        explanation = ({'explanation_status': 'not_evaluated', 'explanation_reused': False,
                        'explanation_reason': 'Explanation inputs changed; authenticated Jev grade retained'}
                       if payload.get('explanation_stale') else {})
        if explanation:
            result.notes.append('Content finding retained from authenticated Jev result; changed explanation inputs require a refreshed explanation.')
        result.coverage.extend({**row, 'file': path, 'line': unit['line'], 'unit': unit['identity'], 'reused': True, **explanation}
                               for row in payload['coverage'])
        for f in payload['findings']:
            details = [{**d, 'line': unit['line_map'][d['line']]} for d in f['details']]
            result.findings.append(Finding(f['rule'], grade(f['probability']), f['message'], file=path,
                line=details[0]['line'] if details else None, probability=f['probability'], source='content', details=details))
