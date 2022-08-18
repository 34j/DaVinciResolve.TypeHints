from unittest import TestCase
from drtypehints.parse_scripting import *
class ParseScriptingTest(TestCase):
    def test_parse_type(self):
        expected = 'Apple[]'
        self.assertEqual(parse_type('[apples]'), expected)
        self.assertEqual(parse_type('[apple]'), expected)
        self.assertEqual(parse_type('[apples...]'), expected)
        self.assertEqual(parse_type('[apple...]'), expected)
        self.assertEqual(parse_type('[Apples]'), expected)
        self.assertEqual(parse_type('[Apple]'), expected)