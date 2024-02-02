from database_manager import UrlDBHandler
from datetime import datetime, timedelta

# Get the original URL from the database
def compose_original_url(shortened_url:str, db_connection:UrlDBHandler,garbage_TTL):
    result=db_connection.get_original_url(shortened_url)

    # It means that exists in the DB
    if result != "not_found":
        expiration_datetime = result["TTLDateTime"] + timedelta(seconds=garbage_TTL)

        # If the link is still valid return the orginal one otherwise communicate the expiration happened
        if expiration_datetime > datetime.now():
            return result["original_URL"]
        else:
            return "link_expired"
    
    return "link_not_found"

def shorten_url(decomposed_url, db_connection:UrlDBHandler):
    # Check if the decomposed_url is already existing on the DB

    # Check if the baseURL is already existing

    # Check if the path is already existing

    # Check if the GET parameter are already existing



# Generate the equivalent alphanumerical string by the given numeric key
def translatorKey(elementKey):
    
    translatingCharacters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    translatedKey=""
    for element in elementKey:
        equivalentElement+=translatingCharacters[element]
    
    return translatedKey
