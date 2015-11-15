import unittest

from babelvueextractor.lexer import Lexer, Token, TOKEN_TEXT, TOKEN_VAR, TOKEN_COMMENT, TOKEN_RAW_HTML, TOKEN_CONST, \
    TOKEN_DOUBLE_WAY_BINDING


class TestLexer(unittest.TestCase):
    def assertTokensEqual(self, t_a, t_b):
        for t1, t2 in zip(t_a, t_b):
            self.assertEqual(t1, t2)

    def test_text(self):
        content = "<div></div>"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_TEXT, '<div></div>')
            ])

    def test_var(self):
        content = "<div>{{ bar }}</div>"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_TEXT, '<div>'),
                Token(TOKEN_VAR, "bar"),
                Token(TOKEN_TEXT, '</div>')
            ])

    def test_comments(self):
        content = "<!-- comments -->"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_COMMENT, "comments")
            ])

    def test_raw_html(self):
        content = "{{{ <div></div> }}}"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_RAW_HTML, "<div></div>")
            ])

    def test_const(self):
        content = "{{* bar }}"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_CONST, "bar")
            ])

    def test_double_way_binding(self):
        content = "{{@ foo }}"
        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(TOKEN_DOUBLE_WAY_BINDING, "foo")
            ])

    def test_combine(self):
        content = "<div>{{ gettext('Hello') }}</div>" \
                  "<div>{{* gettext('Hello') }}</div>" \
                  "<div><!-- Hello -->" \
                  "<span>{{{ Blablabla }}}</span></div>"

        self.assertTokensEqual(
            Lexer(content).tokenize(), [
                Token(token_type=0, contents="<div>"),
                Token(token_type=1, contents="gettext('Hello')"),
                Token(token_type=0, contents="</div><div>"),
                Token(token_type=2, contents="gettext('Hello')"),
                Token(token_type=0, contents="</div><div>"),
                Token(token_type=3, contents="Hello"),
                Token(token_type=0, contents="<span>"),
                Token(token_type=4, contents="Blablabla"),
                Token(token_type=0, contents="</span></div>")
            ])
