import re
import functools
from io import BytesIO

from babel.messages.extract import extract_javascript
from babelvueextractor.lexer import (
    Lexer,
    Token,
    TOKEN_VAR,
    TOKEN_CONST,
    TOKEN_RAW_HTML,
    TOKEN_DOUBLE_WAY_BINDING,
    TOKEN_DIRECTIVE
)

TOKENS = [TOKEN_VAR, TOKEN_CONST, TOKEN_RAW_HTML, TOKEN_DOUBLE_WAY_BINDING, TOKEN_DIRECTIVE]


def extract_vue(fileobj, keywords, comment_tags, options):
    """Extract messages from Vue template files.

    :param fileobj: the file-like the messages should be extracted from
    :param keywords: a list of keywords (i.e. function names) that should be recognize as translation functions
    :param comment_tags: a list of translator tags to search for and include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
    :rtype: ``iterator``
    """
    encoding = options.get('encoding', 'utf-8')
    contents = fileobj.read().decode(encoding=encoding)
    lexer = Lexer(contents, None)
    for t in lexer.tokenize():  # type: Token
        if t.token_type in TOKENS:
            for i in extract_javascript(
                    BytesIO(t.contents.encode(encoding=encoding)),
                    keywords,
                    comment_tags,
                    options):
                if i:
                    yield (t.lineno, i[1], i[2], i[3])
    # Inline JS part
    matchjs = re.search(r'<script>(.+)</script>', contents, re.DOTALL)
    if not matchjs:
        return
    jscontent = matchjs.group(1)
    skipped_line_count = contents[:matchjs.start(1)].count('\n')
    for i in extract_javascript(BytesIO(jscontent.encode(encoding=encoding)),
                                keywords, comment_tags, options):
        yield (skipped_line_count + i[0], i[1], i[2], i[3])
