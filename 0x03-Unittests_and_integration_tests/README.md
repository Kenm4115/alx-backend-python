
# Unit Tests for `utils.py`

This module contains unit tests for helper functions defined in `utils.py`.

## 📂 Location
`0x03-Unittests_and_integration_tests/test_utils.py`

## ✅ What is tested?

1. **`access_nested_map`**
   - Tests that it correctly retrieves values from nested dictionaries.
   - Uses `@parameterized.expand` to cover multiple input/output cases.
   - Tests both valid paths (returns expected value) and invalid paths (raises `KeyError` with the right message).

2. **`get_json`**
   - Tests that it retrieves JSON data from a URL.
   - Uses `unittest.mock.patch` to mock `requests.get` so no real HTTP calls are made.
   - Verifies the returned JSON and that `requests.get` was called with the expected URL.

3. **`memoize`**
   - Tests that the `@memoize` decorator caches the method result.
   - Uses `patch.object` to track how many times the method is actually called.
   - Verifies the method is called once even when accessed multiple times.

## 🚀 How to run
From the root of the project:
```bash
cd 0x03-Unittests_and_integration_tests
python3 -m unittest test_utils.py


---

# Unit & Integration Tests for `client.py`

This module contains both unit tests and integration tests for the `GithubOrgClient` class defined in `client.py`.

## 📂 Location
`0x03-Unittests_and_integration_tests/test_client.py`

## ✅ What is tested?

### 🔹 **Unit tests**
- **`GithubOrgClient.org`**
  - Verifies that it calls `get_json` with the correct GitHub API URL.
  - Uses `@parameterized.expand` to test multiple organizations.

- **`GithubOrgClient._public_repos_url`**
  - Mocks the `org` property and checks that `_public_repos_url` returns the `repos_url`.

- **`GithubOrgClient.public_repos`**
  - Mocks both `_public_repos_url` and `get_json`.
  - Verifies that it returns the expected list of repository names.
  - Ensures mocks are called exactly once.

- **`GithubOrgClient.has_license`**
  - Parametrized tests that check if a repository has a given license key.

### 🔹 **Integration tests**
- Uses `fixtures.py` to load sample payloads.
- `TestIntegrationGithubOrgClient`:
  - Patches `requests.get` to return different fixture data depending on the URL.
  - Tests the `public_repos` method end-to-end (but without actual network calls).
  - Tests filtering repos by license.

## 🚀 How to run
From the root of the project:
```bash
cd 0x03-Unittests_and_integration_tests
python3 -m unittest test_client.py
