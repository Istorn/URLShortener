from database_manager import UrlDBHandler
from datetime import datetime, timedelta


class Shortener:
    def __init__(self, db_connection: UrlDBHandler, garbage_TTL):
        self.db_connection = db_connection
        self.garbage_TTL = garbage_TTL

    # Get the original URL from the database
    def compose_original_url(self, shortened_url: str):
        result = self.db_connection.get_original_url(shortened_url)

        # It means that exists in the DB
        if result != "not_found":
            expiration_datetime = result["TTLDateTime"] + timedelta(seconds=self.garbage_TTL)

            # If the link is still valid return the original one otherwise communicate the expiration happened
            if expiration_datetime > datetime.now():
                return result["original_URL"]
            else:
                return "link_expired"

        return "link_not_found"

    # Shorten the URL
    def shorten_url(self, decomposed_url):
       ''' Check if the decomposed_url is already existing on the DB
        element_key=self.alphanumerical_to_element_key(decomposed_url)
        existing_shortened = self.db_connection.check_existing_shortened(element_key)
        if existing_shortened is not None:
             # It means that exists in the DB
            if existing_shortened != "not_found":
                expiration_datetime = existing_shortened["TTLDateTime"] + timedelta(seconds=self.garbage_TTL)

                # In this case, we renew its own TTL
                if expiration_datetime > datetime.now():
                    self.db_connection.renew_TTLDateTime_document("shortened",element_key)ù
                
                # Return the result
                existing_shortened["original_URL"]
        else:
        '''
        
        # Check if the baseURL, path and getParams are already existing into the DB
        existing_base_url=self.db_connection.check_existing_baseURL(decomposed_url["baseURL"])
        existing_path=self.db_connection.check_existing_path(decomposed_url["path"])
        existing_get_params=self.db_connection.check_existing_getParams(decomposed_url["getParams"])
       
       # If all of them are not None, it means that the shorten URL may already exist
       

        
    # Generate the equivalent alphanumerical string by the given numeric key
    def element_key_to_alphanumerical(self, element_key):
        translating_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        translated_key = ""

        for element in element_key:
            translated_key += translating_characters[element]

        return translated_key

    # Opposite function
    def alphanumerical_to_element_key(self, alphanumerical_element):
        translating_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        splitted_alphanumerical = list(alphanumerical_element)
        element_key = ""

        for splitted in splitted_alphanumerical:
            element_key += translating_characters.index(splitted)

        return element_key
