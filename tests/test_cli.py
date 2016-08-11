import unittest

from cli.github_token_cli import confirm_token


class TestCli(unittest.TestCase):
    def test_confirm_token(self):
        self.assertTrue(confirm_token('95fa8005a49d88436e2873dcd2aaab544fd8c699', False))
        self.assertTrue(confirm_token('62cef9714d6673576e38fc50fb532623b74f54cb', True))

        self.assertFalse(confirm_token('asg90asdi', False))
        self.assertFalse(confirm_token('sdfghsdhd', True))


if __name__ == '__main__':
    unittest.main()
