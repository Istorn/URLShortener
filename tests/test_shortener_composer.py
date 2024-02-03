import unittest
from datetime import datetime, timedelta
import time
from database_manager import UrlDBHandler
from shorten_composer import Shortener
from url_validation import is_valid_url

class TestShortener(unittest.TestCase):

    
    def setUp(self):
        
        self.mock_db_handler = UrlDBHandler("127.0.0.1:27017","test_shortener_composer_db")
        self.shortener = Shortener(self.mock_db_handler, garbage_TTL=5, key_size=1)

    def test_shorten_and_generate_original_url(self):
        self.mock_db_handler.delete_database()
        test_url="https://my_first_test.com/path/to/my/file.php?attempt=one"
        decomposed_url=is_valid_url(test_url)
        shortened_url=self.shortener.shorten_url(decomposed_url)
        original_generated_url=self.shortener.compose_original_url(shortened_url)

        assert original_generated_url == test_url
        assert shortened_url == "aab"
        
    def test_verify_url_expiration(self):
        self.mock_db_handler.delete_database()
        test_url="https://www.i_am_gonna_expire.com"
        decomposed_url=is_valid_url(test_url)
        shortened_url=self.shortener.shorten_url(decomposed_url)
        
        time.sleep(self.shortener.garbage_TTL)

        assert self.shortener.compose_original_url(shortened_url) == "link_expired"
            
    def test_compose_original_url_link_not_found(self):
        self.mock_db_handler.delete_database()
        assert self.mock_db_handler.get_original_url("123") == "not_found"

    def test_reach_max_shorten_url_generated(self):
        self.mock_db_handler.delete_database()
        for element in range(0,62):
            comlpete_url=f"https://{element}.com"
            decomposed_url=is_valid_url(comlpete_url)
            self.shortener.shorten_url(decomposed_url)
        
        final_decomposed_url=is_valid_url("https://final.com")
        final_shortened=self.shortener.shorten_url(final_decomposed_url)

        assert final_shortened == "MAX_GENERATED_KEY_FOR_SHORTEN_LINK"
        
    def test_get_most_near_free_key_by_document_type(self):
        self.mock_db_handler.delete_database()
        decomposed_url=is_valid_url("https://test_key_website.com/path/key.html?test=value")
        self.shortener.shorten_url(decomposed_url)
        
        
        
        for document in ["baseURL","path","getParams"]:
            assert self.shortener.get_most_near_free_key_by_document_type(document,"")["elementKey"] == str(self.shortener.url_db_handler.get_num_documents_by_element_key_length(document,1))
        
        assert self.shortener.get_most_near_free_key_by_document_type("shortened","")["elementKey"] == str(self.shortener.url_db_handler.get_num_documents_by_element_key_length("shortened",3))
        
    def test_alphanumerical_to_number(self):
        assert self.shortener.alphanumerical_to_element_key("abc") == "123"
    
    def test_numerical_to_alphanumerical(self):
        assert self.shortener.element_key_to_alphanumerical("123") == "abc"

    def test_already_existing_shortened(self):
        self.mock_db_handler.delete_database()
        decomposed_url=is_valid_url("https://this_web_site.com/is?already=existing")
        shortened=self.shortener.shorten_url(decomposed_url)

        shortened2=self.shortener.shorten_url(decomposed_url)

        assert shortened == shortened2
    
    def test_renew_link_before_its_expiration(self):
        self.mock_db_handler.delete_database()
        decomposed_url=is_valid_url("https://renew.com/before?my=expiration")
        self.shortener.shorten_url(decomposed_url)

        time.sleep(self.shortener.garbage_TTL-1)

        shortened_twice=self.shortener.shorten_url(decomposed_url)

        assert shortened_twice is not "link_expired"


    def test_renew_link_after_its_expiration(self):
        self.mock_db_handler.delete_database()
        decomposed_url=is_valid_url("https://renew_twice.com/after?its=expiration")
        shortened_first=self.shortener.shorten_url(decomposed_url)  

        assert shortened_first is not "link_expired"

        time.sleep(self.shortener.garbage_TTL+1)

        shortened_twice=self.shortener.shorten_url(decomposed_url)

        assert shortened_twice == "link_expired"

if __name__ == '__main__':
    unittest.main()
