'''
test_quotes.py
Description: Unit tests for quotes module
'''

import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app.quotes import get_random_quote, MOTIVATIONAL_QUOTES

class QuotesTestCase(unittest.TestCase):
    def test_get_random_quote_returns_string(self):
        quote = get_random_quote()
        self.assertIsInstance(quote, str)

    def test_get_random_quote_from_list(self):
        quote = get_random_quote()
        self.assertIn(quote, MOTIVATIONAL_QUOTES)

    def test_motivational_quotes_not_empty(self):
        self.assertGreater(len(MOTIVATIONAL_QUOTES), 0)

    def test_motivational_quotes_contains_muhammad_ali(self):
        ali_quotes = [q for q in MOTIVATIONAL_QUOTES if 'Muhammad Ali' in q]
        self.assertGreater(len(ali_quotes), 0)


if __name__ == '__main__':
    unittest.main()
