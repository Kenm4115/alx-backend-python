#!/usr/bin/env python3
"""
test_client.py
--------------
This module contains unit tests and integration tests for the GithubOrgClient
class (from client.py).

The tests use:
- unittest: Python’s built-in testing framework
- unittest.mock: for mocking external calls and properties
- parameterized: for running the same test logic with multiple inputs
- parameterized_class: for integration tests with fixtures

Tests included:
1. Unit tests for:
   - org property
   - _public_repos_url property
   - public_repos method
   - has_license static method
2. Integration tests for public_repos with actual fixture data.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
#from fixtures import org_payload, repos_payload
from fixtures import expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods and properties."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org:
        - Returns the expected payload from get_json
        - Calls get_json exactly once with the correct URL
        """
        # Arrange
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test that _public_repos_url:
        - Reads 'repos_url' from the mocked org payload
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "http://some_url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos:
        - Returns the expected list of repo names
        - Calls get_json with the correct URL
        - Reads the _public_repos_url property exactly once
        """
        # Arrange: mock JSON response from get_json
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]

        # Patch the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://fake.url"

            # Act
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Assert
            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://fake.url")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license:
        - Returns True if repo has the given license key
        - Returns False otherwise
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        # These values come from fixtures.py
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos.

    These tests:
    - Mock only external requests (requests.get)
    - Use actual fixture data to simulate GitHub API responses
    """

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and set side_effects for
        different URLs."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            # Simulate different responses depending on the URL
            if url == "https://api.github.com/orgs/google":
                return Mock(json=lambda: cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all integration tests are done."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test: public_repos should return expected_repos list."""
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test: public_repos should filter repos by license."""
        client = GithubOrgClient("google")
        result = client.public_repos("apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
