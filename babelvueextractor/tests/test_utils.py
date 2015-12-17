# -*- coding: utf-8 -*-

import unittest

from babelvueextractor.extract import _get_messages
from babelvueextractor.utils import is_protected_type, force_text, smart_split
import datetime


class TestUtils(unittest.TestCase):
    def test_get_messages(self):
        self.assertEqual(
            _get_messages('"foo, bar", "bar"'),
            [u'foo, bar', u'bar']
        )
        self.assertRaises(
            ValueError,
            _get_messages,
            "a + b"
        )

    def test_is_protected_type_numeric(self):
        assert is_protected_type(5)
        assert is_protected_type(5L)
        assert is_protected_type(5.0)

    def test_is_protected_type_date(self):
        assert is_protected_type(datetime.datetime.now())
        assert is_protected_type(datetime.date.today())
        assert is_protected_type(datetime.datetime.now().time())

    def test_is_protected_type_sequences(self):
        assert not is_protected_type(tuple())
        assert not is_protected_type(dict())
        assert not is_protected_type(set())

    def test_is_protected_type_func(self):
        assert not is_protected_type(lambda x: x)

    def test_force_text_list(self):
        self.assertEqual(force_text(['a', 'b']), u"['a', 'b']")

    def test_force_text_datetime(self):
        self.assertEqual(u'2015-11-21 11:05:05',
                         force_text(datetime.datetime(year=2015, day=21, month=11, hour=11, minute=5, second=5)))

    def test_force_text_datetime_strings_only(self):
        t = datetime.datetime(2015, 11, 21, 11, 5, 5)
        self.assertEqual(
            t,
            force_text(t, strings_only=True))

    def test_force_text_str(self):
        self.assertEqual(force_text('hello'), u"hello")

    def test_force_text_unicode(self):
        self.assertEqual(force_text(u'привет'), u'привет')

    def test_smart_split(self):
        self.assertEqual(
            list(smart_split(r'This is "a person\'s" test.')),
            ['This', 'is', '"a person\\\'s"', 'test.'])

        self.assertEqual(
            list(smart_split(r"Another 'person\'s' test.")),
            ['Another', "'person\\'s'", 'test.'])

        self.assertEqual(
            list(smart_split(r'A "\"funky\" style" test.')),
            ['A', '"\\"funky\\" style"', 'test.'])
