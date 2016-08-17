import unittest

from migration.github import GitHubToken, InvalidTokenError


class TestToken(unittest.TestCase):
    test_token_file_names = [fn + '.backup' for fn in GitHubToken.token_file_names]
    valid_tokens = list()
    invalid_token = 'This is a invalid token'

    # read token from backup token files
    for fn in test_token_file_names:
        with open(fn) as test_token_file:
            valid_tokens.append(test_token_file.read())

    def test_token_save(self):
        for enterprise in range(len(self.valid_tokens)):
            token = GitHubToken(enterprise=enterprise, token=self.valid_tokens[enterprise])

            with open(token.path) as token_file:
                self.assertTrue(token_file.read(), self.valid_tokens[False])

    def test_confirm_token(self):
        enterprise = False
        # if pass invalid token , it raises InvalidTokenError
        with self.assertRaises(InvalidTokenError):
            token = GitHubToken(enterprise=enterprise, token=self.invalid_token)
            self.assertTrue(token is None)

        token2 = GitHubToken(enterprise=enterprise, token=self.valid_tokens[enterprise])
        self.assertTrue(token2 is not None)

if __name__ == '__main__':
    unittest.main()
