"""Local publication manifest and conservative reader-unit extraction from Git blobs.

This module never executes branch code or opens working-tree files. Source coordinates
are presentation metadata; semantic identities contain only extracted reader content.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from html.parser import HTMLParser
from html import unescape
from pathlib import PurePosixPath
from urllib.parse import urljoin, urlsplit

from . import gitops, globs
from .config import DEFAULT_CONTENT_EXCLUDE, content_path_excluded
from .content_evidence import _safe_path, _safe

EXTRACTOR_REVISION = 'public-units-4'
_READER_FIELDS = {'title', 'description', 'summary', 'heading', 'text', 'label', 'caption',
                  'alt', 'placeholder', 'aria-label', 'href', 'url', 'canonical', 'robots'}
_DYNAMIC = re.compile(r'[{}]|<%|\$\{|\bv-(?:if|for|bind)\b|\b(?:export|import)\s')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                     separators=(',', ':')).encode()).hexdigest()


def safe_source(path, cfg, *, evidence=False):
    # Required denials cannot be removed with exclude=[] or broad declarations.
    from .config import DEFAULT_CONTENT_EVIDENCE_EXCLUDE
    required = DEFAULT_CONTENT_EVIDENCE_EXCLUDE if evidence else DEFAULT_CONTENT_EXCLUDE
    additional = cfg.content.evidence_exclude if evidence else cfg.content.exclude
    return _safe_path(path) and not content_path_excluded(path, [*required, *additional])


def tree(repo, revision):
    resolved = gitops.git(repo, 'rev-parse', '--verify', '--end-of-options', f'{revision}^{{commit}}').stdout.strip()
    entries = {}
    for entry in gitops.git(repo, 'ls-tree', '-rz', resolved).stdout.split('\0'):
        if entry:
            meta, name = entry.split('\t', 1)
            mode, kind, oid = meta.split()
            entries[name] = (mode, kind, oid)
    return resolved, entries


def read_blob(repo, entry):
    mode, kind, oid = entry
    if kind != 'blob' or mode not in {'100644', '100755'}:
        return None, 'Nonregular Git object (including symlink)'
    if int(gitops.git(repo, 'cat-file', '-s', oid).stdout.strip()) > 160000:
        return None, 'Blob exceeds 160000 byte extraction limit'
    raw = gitops.git(repo, 'cat-file', 'blob', oid).stdout
    if '\0' in raw or '\ufffd' in raw:
        return None, 'Binary or undecodable blob'
    return _safe(raw), None


def publication_for(path, cfg):
    if not safe_source(path, cfg):
        return None, 'Required or configured path exclusion'
    mappings = [p for p in cfg.content.publications if globs.match(path, p.sources)]
    if len(mappings) != 1:
        return None, 'Ambiguous publication mapping' if mappings else 'No trusted publication mapping'
    p = mappings[0]
    if not p.published:
        return None, 'Publication is disabled'
    if not p.drafts and any(part.casefold() in {'draft', 'drafts', '_drafts'} for part in PurePosixPath(path).parts):
        return None, 'Draft publication requires explicit opt-in'
    if not globs.match(path, [*cfg.content.include, *cfg.content.source_include]):
        return None, 'Outside narrowing include/source_include patterns'
    return p, None


def _unit(kind, text, line, *, context='', field='', anchors=None, line_map=None):
    if anchors is None:
        line += text[:len(text) - len(text.lstrip())].count('\n')
    text = text.strip()
    if not text:
        return None
    anchor_text = text.splitlines() if anchors is None else anchors
    return {'kind': kind, 'text': text, 'context': context, 'field': field,
            'identity': digest([EXTRACTOR_REVISION, kind, field, context, text]),
            'line': line, 'anchors': {i + 1: v for i, v in enumerate(anchor_text)},
            'line_map': {i + 1: n for i, n in enumerate(line_map or range(line, line + len(anchor_text)))}}


def _limit(line, reason):
    return {'line': line, 'status': 'not_evaluated', 'reason': reason}


class _HTML(HTMLParser):
    def __init__(self, *, template=False):
        super().__init__(convert_charrefs=False)
        self.units, self.limits, self.stack = [], [], []
        self.template = template
        self.heading = ''
        self.script_type = None
        self.fragments = []
        self.fragment_kind = 'copy'
        self.incomplete = False

    def flush(self):
        if self.fragments and not self.incomplete:
            raw = ''.join(text for text, _ in self.fragments)
            anchors, locations = [], []
            for text, line in self.fragments:
                for offset, fragment in enumerate(text.splitlines()):
                    if fragment.strip():
                        anchors.append(fragment.strip()); locations.append(line + offset)
            unit = _unit(self.fragment_kind, unescape(raw), locations[0] if locations else 1,
                         context='' if self.fragment_kind == 'heading' else self.heading,
                         anchors=anchors, line_map=locations)
            if unit:
                self.units.append(unit)
                if self.fragment_kind == 'heading':
                    self.heading = unit['text']
        self.fragments.clear()
        self.incomplete = False

    def add(self, kind, text, line, **kwargs):
        unit = _unit(kind, text, line, context=self.heading, **kwargs)
        if unit:
            self.units.append(unit)

    def handle_starttag(self, tag, attrs):
        if tag in _BLOCK_TAGS:
            self.flush()
        line = self.getpos()[0]
        attrs = dict(attrs)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)
        if tag == 'script':
            self.script_type = attrs.get('type')
        if any(x in self.stack for x in ('style', 'script', 'noscript')):
            return
        raw = self.get_starttag_text()
        if _DYNAMIC.search(raw) or tag[:1].isupper() or tag not in _HTML_TAGS:
            self.limits.append(_limit(line, 'Dynamic attributes or custom component require resolved output'))
        for name, value in attrs.items():
            if name not in {'alt', 'title', 'aria-label', 'placeholder', 'href', 'src', 'content', 'lang', 'value'} or value is None:
                continue
            if _DYNAMIC.search(value) or value not in raw:
                self.limits.append(_limit(line, 'Dynamic or encoded attribute requires resolved output'))
                continue
            if name == 'value' and tag not in {'button', 'input', 'option'}:
                continue
            kind = 'link' if name in {'href', 'src'} else 'metadata' if tag in {'meta', 'link', 'html'} else 'alt' if name == 'alt' else 'copy'
            field = (attrs.get('name') or attrs.get('property') or name) if tag == 'meta' else name
            self.add(kind, value, line + raw[:raw.find(value)].count('\n'), field=field)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in _BLOCK_TAGS:
            self.flush()
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]
        if tag == 'script':
            self.script_type = None

    def handle_data(self, data):
        line = self.getpos()[0]
        if 'script' in self.stack:
            if self.script_type == 'application/ld+json':
                try:
                    json.loads(data)
                except (ValueError, RecursionError):
                    self.limits.append(_limit(line, 'Unresolved or invalid structured data'))
                else:
                    self.add('schema', data, line)
            return
        if any(x in self.stack for x in ('style', 'noscript')) or not data:
            return
        if self.template and not self.stack:
            return  # JS outside markup is never reader copy.
        if _DYNAMIC.search(data):
            self.limits.append(_limit(line, 'Dynamic text requires resolved output'))
            self.incomplete = True
            return
        enclosing = next((tag for tag in reversed(self.stack) if tag in _BLOCK_TAGS), '')
        self.fragment_kind = ('heading' if enclosing in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
                              else 'metadata' if enclosing == 'title' else 'copy')
        self.fragments.append((data, line))

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')


_BLOCK_TAGS = set('html head body title main article section header footer nav div p h1 h2 h3 h4 h5 h6 ul ol li dl dt dd blockquote form button select option textarea table thead tbody tr th td details summary figure figcaption script style noscript pre'.split())


_HTML_TAGS = set('html head body title meta link main article section header footer nav div span p a img picture source h1 h2 h3 h4 h5 h6 ul ol li dl dt dd blockquote strong em b i small br hr form input label button select option textarea table thead tbody tr th td details summary figure figcaption video audio track template script style noscript pre code time address'.split())


def _mask_expressions(text):
    """Remove complete template expressions using the same conservative JS lexer."""
    from .content_syntax import group_end, UnsupportedSyntax
    out, limits, i = [], [], 0
    while i < len(text):
        if text[i] != '{':
            out.append(text[i]); i += 1; continue
        start = i
        try:
            i = group_end(text, start)
        except UnsupportedSyntax:
            i = len(text)
        limits.append(_limit(text.count('\n', 0, start) + 1, 'Dynamic expression requires resolved output'))
        out.append('{}' + '\n' * text[start:i].count('\n'))
    return ''.join(out), limits


def extract(path, text, publication):
    suffix = PurePosixPath(path).suffix.lower()
    units, limits = [], []
    if suffix in {'.html', '.htm', '.astro', '.svelte', '.vue', '.jsx', '.tsx'}:
        parser = _HTML(template=suffix not in {'.html', '.htm'})
        # Astro frontmatter is code, never feed its markup-looking string literals.
        if suffix == '.astro' and text.startswith('---'):
            match = re.match(r'---[^\n]*\n.*?\n---[^\n]*(?:\n|$)', text, re.S)
            if match:
                text = '\n' * match.group().count('\n') + text[match.end():]
        if suffix in {'.jsx', '.tsx'}:
            from .content_syntax import jsx_expression, UnsupportedSyntax
            try:
                text = jsx_expression(text)
            except UnsupportedSyntax as exc:
                return [], [_limit(1, str(exc))]
        expression_limits = []
        if parser.template:
            # Script blocks are suppressed by the parser except static JSON-LD.
            parts = re.split(r'(<script\b[^>]*>.*?</script\s*>)', text, flags=re.I | re.S)
            offset = 0
            for index, part in enumerate(parts):
                if not part.lower().startswith('<script'):
                    parts[index], omitted = _mask_expressions(part)
                    expression_limits.extend({**limit, 'line': limit['line'] + offset} for limit in omitted)
                offset += part.count('\n')
            text = ''.join(parts)
        parser.feed(text)
        parser.flush()
        units, limits = parser.units, parser.limits + expression_limits
        if parser.template and not units:
            limits.append(_limit(1, 'No supported static reader-facing template units'))
    elif suffix in {'.md', '.mdx'}:
        if suffix == '.mdx':
            from .content_syntax import omit_mdx_regions
            text, omitted = omit_mdx_regions(text)
            limits.extend(omitted)
        lines = text.splitlines()
        i, heading, fenced, comment = 0, '', False, False
        if lines and lines[0].strip() == '---':
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                match = re.match(r'^([\w-]+):\s*(.*?)\s*$', lines[i])
                if match and match[1].lower() in _READER_FIELDS:
                    value = match[2].strip('"\'')
                    if value and value not in {'|', '>'} and not _DYNAMIC.search(value):
                        units.append(_unit('metadata', value, i + 1, field=match[1]))
                    else:
                        limits.append(_limit(i + 1, 'Unsupported frontmatter value'))
                i += 1
            i += 1
        paragraph, first = [], i + 1
        def flush():
            if paragraph:
                units.append(_unit('copy', '\n'.join(paragraph), first, context=heading))
                paragraph.clear()
        while i < len(lines):
            line, number = lines[i], i + 1
            if comment or '<!--' in line:
                flush()
                comment = '-->' not in line
                limits.append(_limit(number, 'HTML comment omitted'))
            elif re.match(r'^\s*(```|~~~)', line):
                flush(); fenced = not fenced
                if fenced:
                    limits.append(_limit(number, 'Code fence is outside reader-copy extraction'))
            elif fenced:
                pass
            elif not line.strip():
                flush()
            elif re.match(r'^#{1,6}\s', line):
                flush(); heading = re.sub(r'^#{1,6}\s+', '', line).strip()
                units.append(_unit('heading', line, number))
            elif re.search(r'<!--|-->|<[^>]*>|[{}]|^\s*(?:import|export)\b', line):
                flush()
                limits.append(_limit(number, 'MDX/HTML/dynamic Markdown requires resolved output'))
            else:
                if not paragraph:
                    first = number
                paragraph.append(line)
                for match in re.finditer(r'(!?)\[([^\]]*)\]\(([^\s)]+)(?:\s+"[^"]*")?\)', line):
                    units.append(_unit('link', match[3], number, context=heading, field='href'))
                    if match[1]:
                        units.append(_unit('alt', match[2], number, context=heading, field='alt'))
            i += 1
        flush()
    elif suffix == '.json':
        try:
            record = json.loads(text)
        except (ValueError, RecursionError):
            return [], [_limit(1, 'Invalid JSON copy record')]
        if not publication.fields:
            return [], [_limit(1, 'JSON reader fields must be explicitly declared')]
        def walk(value, parts):
            key = '.'.join(parts)
            if isinstance(value, dict):
                for k, v in value.items(): walk(v, [*parts, k])
            elif isinstance(value, list):
                for i, v in enumerate(value): walk(v, [*parts, str(i)])
            elif isinstance(value, str) and any(globs.match(key.replace('.', '/'), [f.replace('.', '/')]) for f in publication.fields):
                literal = json.dumps(value, ensure_ascii=False)[1:-1]
                at = text.find(literal)
                if at < 0 or literal != value or text.count(literal) != 1:
                    limits.append(_limit(1, 'Escaped or repeated JSON field needs an unambiguous exact source anchor'))
                else:
                    kind = 'link' if parts[-1] in {'href', 'url'} else 'metadata' if parts[-1] in {'title', 'description'} else 'copy'
                    units.append(_unit(kind, value, text.count('\n', 0, at) + 1, field=key))
        walk(record, [])
    else:
        limits.append(_limit(1, 'Unsupported source format; no implementation-source fallback'))
    kept = []
    for unit in units:
        if unit and '[credential redacted]' in unit['text']:
            limits.append(_limit(unit['line'], 'Credential-bearing source omitted; redaction is not a source anchor'))
        elif unit:
            kept.append(unit)
    return kept, limits


def _artifacts(repo, revision, cfg):
    resolved, entries = tree(repo, revision)
    artifacts, exclusions = [], []
    for path, entry in sorted(entries.items()):
        publication, reason = publication_for(path, cfg)
        if publication is None:
            exclusions.append({'path': path, 'reason': reason})
            continue
        text, reason = read_blob(repo, entry)
        if text is None:
            exclusions.append({'path': path, 'reason': reason})
            continue
        if not publication.drafts and re.search(r'(?im)^\s*(?:draft\s*:\s*true|published\s*:\s*false)\s*$', text):
            exclusions.append({'path': path, 'reason': 'Draft metadata requires explicit opt-in'})
            continue
        units, limits = extract(path, text, publication)
        route = publication.route.replace('{stem}', PurePosixPath(path).stem).replace('{path}', str(PurePosixPath(path).with_suffix('')))
        artifacts.append({'id': publication.id, 'path': path, 'type': publication.type, 'route': route,
                          'source_format': PurePosixPath(path).suffix.lower(),
                          'units': units, 'limitations': limits, 'dependencies': list(publication.dependencies),
                          'evidence': list(publication.evidence), 'source_digest': entry[2],
                          'semantic_digest': digest([publication.type, route, [(u['kind'], u['identity']) for u in units], [limit['reason'] for limit in limits]])})
    return resolved, artifacts, exclusions


def referenced_routes(artifact):
    """Resolve literal relative links against the declared route, never filesystem paths."""
    targets = set()
    for unit in artifact['units']:
        if unit['kind'] != 'link':
            continue
        try:
            parsed = urlsplit(unit['text'])
            if parsed.scheme or parsed.netloc:
                continue
            targets.add(urlsplit(urljoin(artifact['route'], unit['text'])).path)
        except ValueError:
            continue  # Invalid URL remains a literal unit, not a guessed dependency.
    return targets


def manifest(repo, base, head, cfg, changed=None):
    """Return a JSON-compatible, credential-free plan; no cache/provider construction.

    All currently declared artifacts are listed. `affected` schedules current PR
    artifacts plus only transitive declared dependants and explicit route references.
    Immutable cache records are resolved at request time with the signing credential;
    this API reports configuration, never guesses a cache hit from file existence.
    """
    old_revision, old, _ = _artifacts(repo, base, cfg)
    revision, current, exclusions = _artifacts(repo, head, cfg)
    changed = changed if changed is not None else gitops.changed_files(repo, old_revision, revision)
    renames = {cf.path: cf.old_path for cf in changed if cf.old_path}
    old_by_path = {a['path']: a for a in old}
    current_by_path = {a['path']: a for a in current}
    affected_ids, changed_routes = set(), set()
    for a in current:
        previous = old_by_path.get(a['path']) or old_by_path.get(renames.get(a['path']))
        if previous is None:
            # Git similarity thresholds can hide moves after an earlier PR edit.
            # A unique vanished source in the same stable mapping is unambiguous.
            moved_from = [old_a for old_a in old if old_a['id'] == a['id'] and old_a['path'] not in current_by_path]
            if len(moved_from) == 1:
                previous = moved_from[0]
        a['baseline_units'] = previous['units'] if previous else []
        a['affected'] = previous is None or previous['path'] != a['path'] or previous['source_digest'] != a['source_digest'] or previous['semantic_digest'] != a['semantic_digest']
        a['semantic_changed'] = previous is None or previous['semantic_digest'] != a['semantic_digest']
        a['cache_only'] = not a['semantic_changed']
        a['reasons'] = ['Public source changed' if a['semantic_changed'] else 'Source locations or implementation changed; reader inputs unchanged'] if a['affected'] else []
        previous_units = {u['identity'] for u in previous['units']} if previous else set()
        for unit in a['units']:
            unit['changed'] = unit['identity'] not in previous_units
        if a['semantic_changed']:
            affected_ids.add(a['id'])
            if previous is None or previous['route'] != a['route']:
                changed_routes.add(a['route'])
    deleted = [a for a in old if a['path'] not in current_by_path]
    affected_ids.update(a['id'] for a in deleted)
    changed_routes.update(a['route'] for a in deleted)
    changed_paths = {cf.path for cf in changed}
    for a in current:
        bound = {p for code in a['evidence'] for p in cfg.content.context.get(code, [])}
        if bound & changed_paths:
            a['affected'] = True; a['reasons'].append('Bound evidence changed (trusted-base version still governs)')
        if referenced_routes(a) & changed_routes:
            a['affected'] = True; a['cache_only'] = False; a['reasons'].append('Referenced public route changed')
    while True:
        new = {a['id'] for a in current if set(a['dependencies']) & affected_ids} - affected_ids
        if not new: break
        affected_ids.update(new)
    declarations = {p.id: p for p in cfg.content.publications}
    def dependencies(identity):
        direct = set(declarations[identity].dependencies)
        return direct | {nested for dep in direct for nested in dependencies(dep)}
    for a in current:
        a['resolved_dependencies'] = sorted(dependencies(a['id']))
        a['missing_dependencies'] = sorted(set(a['resolved_dependencies']) - {item['id'] for item in current})
        if set(a['dependencies']) & affected_ids:
            a['affected'] = True; a['cache_only'] = False; a['reasons'].append('Declared public dependency changed')
    return {'schema_version': 1, 'extractor_revision': EXTRACTOR_REVISION,
            'base': old_revision, 'head': revision, 'artifacts': current, 'exclusions': exclusions,
            'deleted': [{'id': a['id'], 'path': a['path'], 'route': a['route']} for a in deleted],
            'cache': {'availability': 'configured' if os.environ.get('REWARDGUARD_CACHE_DIR') else 'disabled',
                      'reason': 'Authenticated request records checked during review; no credentials or provider calls in plan'}}
