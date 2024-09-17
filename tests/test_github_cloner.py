import unittest
from src.github_cloner import GitHubCloner

class TestGitHubCloner(unittest.TestCase):
    def test_get_repos(self):
        cloner = GitHubCloner()
        repos = cloner.get_repos()
        self.assertIsInstance(repos, list)

if __name__ == '__main__':
    unittest.main()
