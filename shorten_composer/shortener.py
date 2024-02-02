from database_manager import UrlDBHandler
from datetime import datetime, timedelta


class Shortener:
    def __init__(self, url_db_handler: UrlDBHandler, garbage_TTL):
        self.url_db_handler = url_db_handler
        self.garbage_TTL = garbage_TTL

    # Get the original URL from the database
    def compose_original_url(self, shortened_url: str):
        numerical_shortened_url=self.alphanumerical_to_element_key(shortened_url)
        result = self.url_db_handler.get_original_url(numerical_shortened_url)

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

        # Check if baseURL already exists and in case renew its TTL
        base_url=self.url_db_handler.check_existing_baseURL(decomposed_url["baseURL"])

        if base_url is None:
            base_url=self.get_most_near_free_key_by_document_type("baseURL",decomposed_url["baseURL"])
            if base_url == False:
                return "MAX_GENERATED_KEY_FOR_BASE_URL"
            else:
                base_url=base_url.get("elementKey")
        else:
            base_url=self.url_db_handler.renew_TTLDateTime_document("baseURL",base_url.get("elementKey")).get("elementKey")
        
        # Check if we need to create a path element
            
        if decomposed_url["path"] != "":
            path=self.url_db_handler.check_existing_path(decomposed_url["path"])

            if path is None:
                path=self.get_most_near_free_key_by_document_type("path",decomposed_url["path"])
                if path == False:
                    return "MAX_GENERATED_KEY_FOR_PATH"
                else:
                    path=path.get("elementKey")
            else:
                path=self.url_db_handler.renew_TTLDateTime_document("path",path.get("elementKey")).get("elementKey")
        else:
            path=""

        # Same for getParams

        if decomposed_url["getParams"] != "":
            get_params=self.url_db_handler.check_existing_getParams(decomposed_url["getParams"])

            if get_params is None:
                get_params=self.get_most_near_free_key_by_document_type("getParams",decomposed_url["getParams"])
                if get_params == False:
                    return "MAX_GENERATED_KEY_FOR_QUERY_PARAMS"
                else:
                    get_params=get_params.get("elementKey")
            else:
                get_params=self.url_db_handler.renew_TTLDateTime_document("getParams",get_params.get("elementKey")).get("elementKey")
        else:
            get_params=""

        # Generate the shorten
            
        shorten=self.url_db_handler.create_shortened_url(base_url,path,get_params)

        # Return the shortened link

        return self.element_key_to_alphanumerical(shorten.get("elementKey")) 
        





    # Generate the equivalent alphanumerical string by the given numeric key
    def element_key_to_alphanumerical(self, element_key):
        translating_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        translated_key = ""

        for element in element_key:
            translated_key += translating_characters[int(element)-1]

        return translated_key

    # Opposite function
    def alphanumerical_to_element_key(self, alphanumerical_element):
        translating_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        splitted_alphanumerical = list(alphanumerical_element)
        element_key = ""

        for splitted in splitted_alphanumerical:
            element_key += str(translating_characters.index(splitted)+1)

        return element_key


    # Algorithm to get the most near free key
    def get_most_near_free_key_by_document_type(self,document_type,string_to_store):
        limit=1
        key_free=""
        while limit<5 and key_free=="":
            new_element_key=self.url_db_handler.return_lowest_free_element_key_by_length(document_type,limit)
            if new_element_key is None:
                limit+=1
            else:
                key_free=new_element_key

        # If we have a free key for the base URL we keep going otherwise we interrupt
        if key_free!="":
            if document_type == "baseURL":
                return self.url_db_handler.create_base_url(key_free,string_to_store)
            elif document_type == "path":
                return self.url_db_handler.create_path(key_free,string_to_store)
            else:
                return self.url_db_handler.create_get_params(key_free,string_to_store)
        else:
            return False