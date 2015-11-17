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

    def test_str(self):
        t = Token(token_type=TOKEN_RAW_HTML, contents='<!DOCTYPE html>' +
              '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' +
              '<title>HTML Document</title></head><body><p><b></b></p></body></html>')
        self.assertEqual('<Raw token: "<!DOCTYPE html><html...">', t.__str__())

    def test_repr(self):
        t = Token(token_type=TOKEN_RAW_HTML, contents='<body><p><b></b></p></body></html>')
        self.assertEqual('Token(token_type=4, contents="<body><p><b></b></p></body></html>")', t.__repr__())

    def test_token_name(self):
        self.assertEqual(Token(token_type=0, contents='').token_name, 'Text')
        self.assertEqual(Token(token_type=1, contents='').token_name, 'Var')
        self.assertEqual(Token(token_type=2, contents='').token_name, 'Const')
        self.assertEqual(Token(token_type=3, contents='').token_name, 'Comment')
        self.assertEqual(Token(token_type=4, contents='').token_name, 'Raw')
        self.assertEqual(Token(token_type=5, contents='').token_name, 'Binding')