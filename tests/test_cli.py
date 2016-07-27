import unittest

from cli.input_token import confirm_token


class TestCli(unittest.TestCase):
    def test_confirm_token(self):
        self.assertTrue(confirm_token('fd7afb7372aef5c3a05f9f5a32aa5f115588364c', False))
        self.assertTrue(confirm_token('a16bfcb042036d803058519a86497a5a3f976f80', True))

        self.assertFalse(confirm_token('asg90asdi', False))
        self.assertFalse(confirm_token('sdfghsdhd', True))


if __name__ == '__main__':
    unittest.main()
