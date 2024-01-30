import sys
import re

def is_valid_url(url):
    # Check if the URL has a valid protocol
    valid_protocols = ['http', 'https', 'ftp', 'ftps', 'sftp', 'ssh', 'telnet', 'ldap', 'ldaps','mms']
    if not any(url.startswith(protocol + '://') for protocol in valid_protocols):
        return False


    # Check if the URL length does not exceed 2000 characters
    if len(url) > 2000:
        return False

    # Check if the URL follows query parameters and path rules
    if not re.match(r'^[a-zA-Z0-9-._~:/?#\[\]@!$&\'()*+,;=%]*$', url):
        return False

    return True
5
def split_url(url):
    # Check if the URL is valid
    if not is_valid_url(url):
        print("Invalid URL.")
        sys.exit(1)

    # Find the position of '?' to split base URL and query parameters
    query_start = url.find('?')

    # Extract base URL
    base_url = (url if query_start == -1 else url[:query_start]).split('://')[-1].split('/')[0]

    # Extract subroot
    subroot = url.split('://')[-1].split('/', 1)[-1]

    # Extract query parameters
    query_params = {}
    if query_start != -1:
        query_string = url[query_start + 1:]
        for param in query_string.split('&'):
            key, value = param.split('=')
            query_params[key] = value

    return base_url, subroot, query_params

def main():
    # Check if a URL is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    
    url = 'https://chat.openai.com/c/2e381e33-e53d-4392-9aa7-1efe4acea2ef'

    # Check and split the URL
    base_url, subroot, query_params = split_url(url)

    print("Base URL:", base_url)
    print("Subroot:", subroot)
    print("Query Parameters:", query_params)

if __name__ == "__main__":
    main()
