import unittest
from unittest.mock import MagicMock
from .core import log_splitter


class TestParser(unittest.TestCase):
    def test(self):
        """
        A test test
        """
        self.assertEqual(6, 6)

    def test_log_splitter(self):
        """
        A test test
        """
        log_splitter("blah")
        self.assertEqual(6, 6)

if __name__ == '__main__':
    unittest.main()
