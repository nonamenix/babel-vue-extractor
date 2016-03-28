import re
from ast import literal_eval

from babelvueextractor.lexer import Lexer, TOKEN_VAR, TOKEN_CONST, TOKEN_COMMENT, TOKEN_RAW_HTML, \
    TOKEN_DOUBLE_WAY_BINDING
from babelvueextractor.utils import force_text

TOKENS = [TOKEN_VAR, TOKEN_CONST, TOKEN_COMMENT, TOKEN_RAW_HTML, TOKEN_DOUBLE_WAY_BINDING]

func_re = re.compile('(?P<funcname>\w+)\((?P<messages>\s*[\'"].*)\)')


def _get_messages(raw_messages_string):
    try:
        messages = literal_eval(u'[%s]' % raw_messages_string)
    except ValueError:

        raise RuntimeError("Error in %s" % raw_messages_string)
    messages = map(force_text, messages)

    if len(messages) == 1:
        return messages[0]

    return messages


def _get_n_messages(raw_messages_string):
    str_input = raw_messages_string.rsplit(',', 1)  # ngettext: remove 3rd argument
    return _get_messages(str_input[0])


def extract_vue(fileobj, keywords, comment_tags, options):
    """Extract messages from Vue template files.

    :param fileobj: the file-like the messages should be extracted from
    :param keywords: a list of keywords (i.e. function names) that should be recognize as translation functions
    :param comment_tags: a list of translator tags to search for and include in the results
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
    :rtype: ``iterator``
    """

    for t in Lexer(unicode(fileobj.read(), encoding=options.get('encoding', 'utf-8')), None).tokenize():
        if t.token_type in TOKENS:
            try:
                matched = func_re.match(t.contents).groupdict()
            except AttributeError:
                pass
            else:
                fn = matched['funcname']
                text = matched['messages']
                if fn == 'ngettext':
                    messages = _get_n_messages(text)
                else:
                    messages = _get_messages(text)

                yield t.lineno, fn, messages, []
