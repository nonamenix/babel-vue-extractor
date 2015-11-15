import unittest

from babelvueextractor.extract import func_re


class TestFuncRegExp(unittest.TestCase):
    def test_gettext(self):
        content = 'gettext("Hello")'
        self.assertDictEqual(func_re.match(content).groupdict(), {
            'funcname': 'gettext',
            'messages': '"Hello"'
        })

    def test_undersoce(self):
        content = '_("Hello")'
        self.assertDictEqual(func_re.match(content).groupdict(), {
            'funcname': '_',
            'messages': '"Hello"'
        })

    def test_funct_without_on_brace(self):
        content = ' gettext("Hello"'
        assert func_re.match(content) is None

