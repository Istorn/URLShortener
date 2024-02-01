def is_valid_url(url_to_check):
    if not isinstance(url_to_check, str):
        return False
    
    if (check_base_url(url_to_check)):
        # Check if the URL contains a GET parameters part
        if ((url_to_check.index("?"))>0) and (len(url_to_check.split("?")[1])):
            get_parameters=url_to_check.split("?")[1]
            if (check_get_parameters(get_parameters)):
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def check_base_url(url_to_check):
    url_compliant_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
     # Check if base URL is HTTP compliant for the protocol
    if (not url_to_check.startswith("http://")) or (not url_to_check.startswith("https://")):
        return False
    if url_to_check.index("https://")>0:
        base_url = url_to_check[len("http://"):]
    else:
        base_url = url_to_check[len("https://"):]
    
    # Check if base URL is HTTP compliant for the URL structure
    if not all(char in url_compliant_chars for char in base_url):
        return False
    if ".." in base_url:
        return False
    
    


def check_get_parameters(get_parameters):
    # check if the syntax of GET parameters is HTTP compliant
    if "??" in get_parameters or "==" in get_parameters or "&&" in get_parameters:
        return False
    
    # split by ampersand
    splitted_get_parameters=get_parameters.split("&")
    get_param_compliant_chars= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_~.")

    # check if GET parameters are HTTP compliant one by one: getParameterName=getParameterValue and characters compliant
    for current_get_parameter in splitted_get_parameters:
        current_get_name_value=current_get_parameter.split("=")
        if (len(current_get_name_value)!=2) or (not(all(char in get_param_compliant_chars for char in current_get_parameter))):
            return False
    
    return True

    
    
    