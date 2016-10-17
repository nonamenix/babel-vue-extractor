# -*- coding: utf-8 -*-
import unittest

from babel.messages.extract import DEFAULT_KEYWORDS, extract

from babelvueextractor.extract import extract_vue
from babelvueextractor.tests.utils import FileMock


class TestMessagesExtractor(unittest.TestCase):
    def test_empty_template(self):
        template = FileMock("")
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(), list(result))

    def test_no_messages(self):
        template = FileMock("""
        <div>
            <h1>Foo</h1>
            <p>Lore ipsum delore ...</p>
        </div>
        """)
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(), list(result))

    def test_gettext(self):
        template = FileMock("""
        <div>
            {{ gettext('Foo') }}
        </div>
        """)
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(result), [
            (3, u'gettext', u"Foo", [])
        ])

    def test_underscore(self):
        template = FileMock("""
        <div>
            {{ _("Bar") }}
        </div>
        """)
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(result), [
            (3, '_', u'Bar', [])
        ])

    def test_token_without_content(self):
        template = FileMock("""
            {{  }}
        """)
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(result), [])

    def test_commas(self):
        template = FileMock("""
            {{ gettext('Hello, User') }}
            {{ gettext("You're") }}
        """)

        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(result), [
            (2, 'gettext', u'Hello, User', []),
            (3, 'gettext', u"You're", [])
        ])

    def test_babel(self):
        method = 'babelvueextractor.extract.extract_vue'
        fileobj = open('babelvueextractor/tests/templates/for_babel.vhtml')
        result = extract(method, fileobj)

        self.assertListEqual(list(result), [
            (1, u'Привет, User', [], None),
            (2, u'привет123', [], None)
        ])

    def test_gettext_with_parameter(self):
        template = FileMock("""
        <li class="select__option"
            v-for="season in rankSeasons"
            @click="toggleSeasonAction(season)">
            {{ gettext('{number} season').replace("{number}", season) }}
        </li>
        """)
        result = extract_vue(template, DEFAULT_KEYWORDS.keys(), [], {})
        self.assertEqual(list(result), [
            (5, u'gettext', u'{number} season', [])
        ])
