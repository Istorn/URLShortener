import pytest
from main import is_valid_url, split_url

# Replace 'your_script_name' with the actual name of your script

# Test cases for is_valid_url
@pytest.mark.parametrize("url, expected_result", [
    ("https://www.softwaretestingo.in", True),
    ("http://www.softwaretestingo.in", True),
    ("https://www.softwaretestingo", True),
    ("http://www.softwaretestingo", True),
    ("www.softwaretestingo.in", False),  # Invalid without protocol
    ("https://www.softwaretestingo.in ", False),  # Trailing space
    (" https://www.softwaretestingo.in", False),  # Leading space
    ("", False),  # Empty URL
    ("192.168.0.1", True),  # IP address
    ("www.softwaretestingo", False),  # Missing TLD
    ("https://wwwsoftwaretestingocom", False),  # Missing dots
    ("https://www.com", True),  # Only extension
    ("https://www.softwaretesingo2022.com", True),  # Alphanumeric
    ("https://www.softwaretestingo@.in", False),  # Special character other than dot
    ("https://www.example.com%20encoded", True),  # Encoded URL
    ("https://www.example.com/", True),  # Slash at the end
    ("https://www.example.com/$pecial", False),  # Special characters
    ("<a href='https://www.softwaretestingo.in'>Click here</a>", False),  # Anchor text
    ("https://www.software testing. in", False),  # Spaces between URLs
])
def test_is_valid_url(url, expected_result):
    assert is_valid_url(url) == expected_result

# Additional test cases for split_url
def test_split_url():
    url = "https://www.example.com/path/to/page?param1=value1&param2=value2"
    base_url, subroot, query_params = split_url(url)
    assert base_url == "https://www.example.com"
    assert subroot == "/path/to/page"
    assert query_params == {'param1': 'value1', 'param2': 'value2'}
