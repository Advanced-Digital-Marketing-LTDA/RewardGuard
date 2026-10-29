"""Conservative lexical boundaries, never a JavaScript/MDX interpreter.

Only unambiguous literal tokens and balanced groups are recognized. Regex literals,
interpolated JS template literals, malformed groups and compound JSX return values
are unsupported rather than candidates for reader extraction.
"""
import re


_RETURN = re.compile(r'(?:\breturn\b|=>)\s*(\(*\s*)')


class UnsupportedSyntax(ValueError):
    pass


def _atom_end(text, start):
    """Skip a quoted literal/comment; otherwise return the unchanged offset."""
    if text.startswith('//', start):
        end = text.find('\n', start + 2)
        return len(text) if end < 0 else end
    if text.startswith('/*', start):
        end = text.find('*/', start + 2)
        if end < 0:
            raise UnsupportedSyntax('Unterminated JavaScript comment')
        return end + 2
    quote = text[start]
    if quote in ('"', "'", '`'):
        i = start + 1
        while i < len(text):
            if text[i] == '\\':
                i += 2
            elif text[i] == quote:
                return i + 1
            elif quote == '`' and text.startswith('${', i):
                raise UnsupportedSyntax('Interpolated JavaScript template literal')
            else:
                i += 1
        raise UnsupportedSyntax('Unterminated JavaScript string')
    if quote == '/':
        raise UnsupportedSyntax('Ambiguous JavaScript slash/regex syntax')
    return start


def group_end(text, start):
    pairs = {'{': '}', '(': ')', '[': ']'}
    stack, i = [pairs[text[start]]], start + 1
    while i < len(text):
        end = _atom_end(text, i)
        if end != i:
            i = end
            continue
        char = text[i]
        if char in pairs:
            stack.append(pairs[char])
        elif char in '})]':
            if char != stack.pop():
                raise UnsupportedSyntax('Mismatched JavaScript group')
            if not stack:
                return i + 1
        i += 1
    raise UnsupportedSyntax('Unterminated JavaScript group')


def _jsx_end(text, start):
    stack, i = [], start
    while i < len(text):
        if text[i] == '{':
            i = group_end(text, i)
            continue
        if text[i] != '<':
            i += 1
            continue
        tag = re.match(r'<(/?)([A-Za-z][\w.:-]*)\b', text[i:])
        if not tag:
            raise UnsupportedSyntax('Unsupported JSX tag/fragment')
        closing, name = tag.groups()
        j = i + tag.end()
        while j < len(text) and text[j] != '>':
            if text[j] in ('"', "'"):
                j = _atom_end(text, j)
            elif text[j] == '{':
                j = group_end(text, j)
            else:
                j += 1
        if j >= len(text):
            raise UnsupportedSyntax('Unterminated JSX tag')
        if closing:
            if not stack or stack.pop() != name:
                raise UnsupportedSyntax('Mismatched JSX element')
        elif text[i:j].rstrip().endswith('/'):
            pass
        else:
            stack.append(name)
        i = j + 1
        if not stack:
            return i
    raise UnsupportedSyntax('Unterminated JSX element')


def jsx_expression(text):
    """Return the one bounded direct JSX expression, retaining source line offsets."""
    spans, i = [], 0
    while i < len(text):
        end = _atom_end(text, i)
        if end != i:
            i = end
            continue
        token = _RETURN.match(text, i)
        if token:
            start = token.end()
            if start < len(text) and text[start] == '<':
                end = _jsx_end(text, start)
                tail = end
                for _ in range(token[1].count('(')):
                    while tail < len(text) and text[tail].isspace(): tail += 1
                    if tail >= len(text) or text[tail] != ')':
                        raise UnsupportedSyntax('Unsupported compound JSX return')
                    tail += 1
                while tail < len(text) and text[tail].isspace(): tail += 1
                if tail < len(text) and text[tail] not in ';},':
                    raise UnsupportedSyntax('Unsupported compound JSX return')
                spans.append((start, end))
                i = tail
                continue
        i += 1
    if len(spans) != 1:
        raise UnsupportedSyntax('No unique supported static JSX return expression')
    start, end = spans[0]
    return '\n' * text[:start].count('\n') + text[start:end]


def _esm_end(text, start):
    """Require a terminated statement and a fully examined whitespace-only tail.

    Whitespace never proves completion: assignments, operators and declarations
    can continue after blank lines. Automatic semicolon insertion and declarations
    without a terminator are deliberately unsupported here. Chained statements
    are also unsupported: only a blank-line separator or EOF after the terminator
    establishes a safe boundary; never discard an unexamined physical-line tail.
    """
    i = start
    while i < len(text):
        if text[i] == ';':
            tail = text[i + 1:]
            if re.fullmatch(r'[ \t\r\n]*', tail):
                return len(text)
            separator = re.match(r'[ \t]*\r?\n[ \t]*\r?\n', tail)
            if separator:
                return i + 1 + separator.end()
            raise UnsupportedSyntax('Unexamined MDX ESM statement tail')
        end = _atom_end(text, i)
        if end != i:
            i = end
        elif text[i] in '{([':
            i = group_end(text, i)
        else:
            i += 1
    raise UnsupportedSyntax('No explicit MDX ESM statement boundary')


def omit_mdx_regions(text):
    """Blank whole unsupported ESM/expression regions, preserving source lines."""
    out, limits, offset, fenced = [], [], 0, False
    while offset < len(text):
        line_end = text.find('\n', offset)
        line_end = len(text) if line_end < 0 else line_end + 1
        line = text[offset:line_end]
        if re.match(r'^\s*(```|~~~)', line):
            fenced = not fenced
        esm = not fenced and re.match(r'^\s*(?:import|export)\b', line)
        brace = line.find('{') if not fenced else -1
        if esm or brace >= 0:
            reason = 'Unsupported MDX ESM/expression region omitted without executing it'
            omitted_to_end = False
            try:
                end = _esm_end(text, offset) if esm else group_end(text, offset + brace)
                if not esm and end < len(text) and text[end] != '\n':
                    end = text.find('\n', end)
                    end = len(text) if end < 0 else end
            except UnsupportedSyntax as error:
                end = len(text)  # No trustworthy closing boundary: omit the remaining region.
                omitted_to_end = True
                # UnsupportedSyntax carries only fixed lexer reasons, never source text.
                reason = 'Unsupported MDX ESM/expression region: ' + str(error)
            limits.append({'line': text.count('\n', 0, offset) + 1,
                           'end_line': text.count('\n', 0, end) + (0 if end and text[end - 1] == '\n' else 1),
                           'status': 'not_evaluated', 'reason': reason, 'omitted_to_end': omitted_to_end})
            out.append('\n' * text[offset:end].count('\n'))
            offset = end
        else:
            out.append(line)
            offset = line_end
    return ''.join(out), limits
