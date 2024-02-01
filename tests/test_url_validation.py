import unittest
from url_validation import is_valid_url  

class TestIsValidUrlFunction(unittest.TestCase):

    def test_valid_https_url_with_parameters(self):
        url_to_check = "https://www.example.com/path?param1=value1&param2=value2"
        expected_result = {"baseURL": "www.example.com", "path": "/path", "getParams": "param1=value1&param2=value2"}
        print(is_valid_url(url_to_check))
        self.assertEqual(is_valid_url(url_to_check), expected_result)

    def test_valid_https_url_without_parameters(self):
        url_to_check = "https://www.example.com/path"
        expected_result = {"baseURL": "www.example.com", "path": "/path", "getParams": ""}
        print(is_valid_url(url_to_check))
        self.assertEqual(is_valid_url(url_to_check), expected_result)

    def test_invalid_url_missing_scheme(self):
        invalid_url = "www.example.com"
        self.assertFalse(is_valid_url(invalid_url))

    def test_invalid_url_missing_netloc(self):
        invalid_url = "https://"
        self.assertFalse(is_valid_url(invalid_url))

    def test_invalid_url_http_scheme(self):
        invalid_url = "http://www.example.com"
        self.assertFalse(is_valid_url(invalid_url))

    def test_invalid_url_empty_string(self):
        invalid_url = ""
        self.assertFalse(is_valid_url(invalid_url))

    def test_invalid_url_none(self):
        invalid_url = None
        self.assertFalse(is_valid_url(invalid_url))


    def test_valid_urls(self):
            valid_urls = [
                ("https://www.softwaretestingo.in", {
                    "baseURL": "www.softwaretestingo.in",
                    "path": "",
                    "getParams": ""
                }),
                
                ("https://www.softwaretestingo", {
                    "baseURL": "www.softwaretestingo",
                    "path": "",
                    "getParams": ""
                }),
                
                ("https://192.168.0.1", {
                    "baseURL": "192.168.0.1",
                    "path": "",
                    "getParams": ""
                }),  # IP address
                ("https://www.com", {
                    "baseURL": "www.com",
                    "path": "",
                    "getParams": ""
                }),  # Only extension
                ("https://www.softwaretesingo2022.com", {
                    "baseURL": "www.softwaretesingo2022.com",
                    "path": "",
                    "getParams": ""
                }),
                ("https://www.example.com%20encoded", {
                    "baseURL": "www.example.com%20encoded",
                    "path": "",
                    "getParams": ""
                }),
                    # Encoded URL
                ("https://www.example.com/", {
                    "baseURL": "www.example.com",
                    "path": "/",
                    "getParams": ""
                }),
                ("https://www.softwaretestingo.in ", {
                    "baseURL": "www.softwaretestingo.in",
                    "path": "",
                    "getParams": ""
                }),
                ("https://www.example.com/$pecial", {
                    "baseURL": "www.example.com",
                    "path": "/$pecial",
                    "getParams":""
                })
            ]

            for url, expected_result in valid_urls:
                with self.subTest(url=url, expected_result=expected_result):
                    self.assertEqual(is_valid_url(url), expected_result)

    def test_invalid_urls(self):
        invalid_urls = [
            
            
            ("http://www.softwaretestingo", False),
            ("http://www.softwaretestingo.in", False),
            ("www.softwaretestingo.in", False),  # Invalid without protocol
            ("", False),  # Empty URL
            ("www.softwaretestingo", False),  # Missing TLD
            ("https://wwwsoftwaretestingocom", False),  # Missing dots
            ("https://www.softwaretestingo@.in", False),  # Special character other than dot
            
            ("<a href=\"https://www.softwaretestingo.in\">Click here</a>", False),  # Anchor text
            ("https://www.software testing. in", False),  # Spaces between URLs
            (" https://www.softwaretestingo.in", False)  # Leading space
        ]

        for url, expected_result in invalid_urls:
            with self.subTest(url=url, expected_result=expected_result):
                self.assertEqual(is_valid_url(url), expected_result)
if __name__ == "__main__":
    unittest.main()
