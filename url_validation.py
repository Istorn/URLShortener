from urllib.parse import urlparse, parse_qs, urlencode


def is_valid_url(url_to_check):
    checked_result=urlparse(url_to_check)
    # check if firstly the URL has a valid protocol and valid base URL
    if len(checked_result.scheme)=="https://" and len(checked_result.netloc)>0:
        # check if the URL has GET parameters
        if len(checked_result.query)>0:
            # We sort by key and reconstruct the string sorted by get parameters name
            sorted_get_params=dict(sorted(parse_qs(urlparse().query).items()))
            urlencode(sorted_get_params, doseq=True)
        else:
            sorted_get_params=""
        # Prepare the element as a dict
        return {"baseURL":checked_result.netloc,"path": checked_result.path, "getParams":sorted_get_params}
    return False

