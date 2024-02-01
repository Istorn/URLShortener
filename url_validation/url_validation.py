from urllib.parse import urlparse, parse_qs, urlencode

# Function which returns the URL composed as a dict in case of a valid https URL otherwise it returns false
def is_valid_url(url_to_check):
    
    checked_result=urlparse(url_to_check)
    
    # Check if firstly the URL has a valid protocol and valid base URL
    if checked_result.scheme=="https" and len(checked_result.netloc)>0:
        
        # Check if it's at least TLD
        if "." in checked_result.netloc:

            # Check if it has special characters
            reserved_characters = '!#$&\'()*+,/:;=?@[] '
            if not(any(char in reserved_characters for char in checked_result.netloc.strip())):

                # Check if the URL has GET parameters
                if len(checked_result.query)>0:
                    
                    # We sort by key and reconstruct the string sorted by get parameters name
                    sorted_get_params=dict(sorted(parse_qs(checked_result.query).items()))
                    
                    # Rendered as string
                    sorted_get_params=urlencode(sorted_get_params, doseq=True)
                else:
                    sorted_get_params=""

                # Prepare the element as a dict
                return {"baseURL":checked_result.netloc.strip(),"path": checked_result.path, "getParams":sorted_get_params}
    
    return False