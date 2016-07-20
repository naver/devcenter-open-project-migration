import sys
import unittest

from migration.helper import set_encoding


class TestHelper(unittest.TestCase):
    def test_set_encoding(self):
        set_encoding()
        self.assertEqual(sys.getdefaultencoding(), 'utf-8')


if __name__ == '__main__':
    unittest.main()
