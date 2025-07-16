
"""
In this task you will write the first unit test for utils.access_nested_map.
Create a TestAccessNestedMap class that inherits from unittest.TestCase.
Implement the TestAccessNestedMap.test_access_nested_map method
Decorate the method with @parameterized.expand
The body of the test method should not be longer than 2 lines.
Implement TestAccessNestedMap.test_access_nested_map_exception.
"""
#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for bad path"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload and calls requests.get"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize"""

    def test_memoize(self):
        """Test that memoize caches the result of a method"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', 
                          return_value=42) as mock_method:
            obj = TestClass()
            # Call twice
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            # Ensure a_method is only called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
