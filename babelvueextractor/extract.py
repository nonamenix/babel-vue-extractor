from __future__ import unicode_literals
import ast
import functools

import six

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
    contents = fileobj.read()
    u = six.text_type
    if not isinstance(contents, u):
        contents = u(contents, encoding=options.get('encoding', 'utf-8'))
    lexer = Lexer(contents, None)
    u = functools.partial(u, encoding='utf-8')
    for t in lexer.tokenize():  # type: Token
        if t.token_type in TOKENS:
            try:
                tree = ast.parse(t.contents).body[0]
            except (SyntaxError, IndexError, AttributeError):
                pass
            else:
                for node in ast.walk(tree):  # type: ast.Call
                    if (isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)):
                        func_name = node.func.id
                        args = node.args
                        messages = None
                        if func_name == "gettext":
                            if len(args) != 1:
                                raise TypeError("Error at line %s: Function gettext()"
                                                " requires exactly one argument" % t.lineno)
                            if isinstance(args[0], ast.Str):  # ignore other argument types such as variables
                                messages = u(args[0].s)
                        elif func_name == "ngettext":
                            if len(node.args) != 3:
                                raise TypeError("Error at line %s: Function ngettext()"
                                                " requires exactly 3 arguments" % t.lineno)
                            if isinstance(args[0], ast.Str) and isinstance(args[1], ast.Str):
                                messages = u(args[0].s), u(args[1].s)

                        if messages:
                            yield t.lineno, func_name, messages, []
