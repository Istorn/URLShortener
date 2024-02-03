import unittest
from pymongo import MongoClient
from database_manager import UrlDBHandler, MongoDBHandler
from datetime import datetime
import time


TEST_DATABASE_URL = "mongodb://localhost:27017/"
TEST_DATABASE_NAME = "unit_test_database"

class TestMongoDBHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a test MongoDB connection and database
        cls.client = MongoClient(TEST_DATABASE_URL)
        cls.db = cls.client[TEST_DATABASE_NAME]

    @classmethod
    def tearDownClass(cls):
        # Destroy the database after tests
        cls.client.drop_database(TEST_DATABASE_NAME)

    def setUp(self):
        # Set up a MongoDBHandler instance for each test
        self.mongo_handler = MongoDBHandler(TEST_DATABASE_URL, TEST_DATABASE_NAME)

    def tearDown(self):
        # Clean up after each test
        self.db.drop_collection("shortened")
        self.db.drop_collection("baseURL")
        self.db.drop_collection("path")
        self.db.drop_collection("getParams")

    def test_create_document(self):
        # Test the create_document method
        collection_name = "test_collection"
        document = {"key": "value"}
        inserted_id = self.mongo_handler.create_document(collection_name, document)
        self.assertIsNotNone(inserted_id)

        # Check if the document is present in the collection
        collection = self.db[collection_name]
        result = collection.find_one({"_id": inserted_id})
        self.assertIsNotNone(result)
        self.assertEqual(result, document)

class TestUrlDBHandler(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        cls.dummy_element_key="1"
        cls.base_url = "www.example.com"
        cls.path = "/path/test.html"
        cls.get_params = "param=value"
        

        cls.url_db_handler = UrlDBHandler(TEST_DATABASE_URL,TEST_DATABASE_NAME)
        
    @classmethod
    def tearDownClass(cls):
        # Destroy the database after tests
        cls.url_db_handler.delete_database()

    # Test the generation of complete, partial and check if original is the same as provided as input
    def test_create_shortened_complete_url(self):
    
        self.url_db_handler.delete_database()
        # Test complete URL

        shortened_base_url=self.url_db_handler.create_base_url(self.dummy_element_key,self.base_url).get("elementKey")
        shortened_path=self.url_db_handler.create_path(self.dummy_element_key,self.path).get("elementKey")
        shortened_get_params=self.url_db_handler.create_get_params(self.dummy_element_key,self.get_params).get("elementKey")
        result = self.url_db_handler.create_shortened_url(shortened_base_url, shortened_path, shortened_get_params)
        original_url=self.url_db_handler.get_original_url(result.get("elementKey"))

        

        assert result["elementKey"] == "111"
        assert result["baseURL_elementKey"] == self.dummy_element_key
        assert result["path_elementKey"] == self.dummy_element_key
        assert result["getParams_elementKey"] == self.dummy_element_key
        assert result["TTLDateTime"] < datetime.now()
        
        assert original_url["original_URL"] == "https://" + self.base_url + self.path + "?" + self.get_params
        assert result["TTLDateTime"] < datetime.now()
    
    def test_number_of_existing_documents_by_category(self):
        
        # Create one element
        self.url_db_handler.delete_database()
        shortened_base_url=self.url_db_handler.create_base_url(self.dummy_element_key,self.base_url).get("elementKey")
        shortened_path=self.url_db_handler.create_path(self.dummy_element_key,self.path).get("elementKey")
        shortened_get_params=self.url_db_handler.create_get_params(self.dummy_element_key,self.get_params).get("elementKey")
        result = self.url_db_handler.create_shortened_url(shortened_base_url, shortened_path, shortened_get_params)
    
        for document_type in ["baseURL","path","getParams"]:
            assert self.url_db_handler.get_num_documents_by_element_key_length(document_type,1) == 1
        
        assert self.url_db_handler.get_num_documents_by_element_key_length("shortened",3) == 1

    def test_garbage_collection_by_document(self):
        
        self.url_db_handler.delete_database()
        # Create one element
        
        shortened_base_url=self.url_db_handler.create_base_url(self.dummy_element_key,self.base_url).get("elementKey")
        shortened_path=self.url_db_handler.create_path(self.dummy_element_key,self.path).get("elementKey")
        shortened_get_params=self.url_db_handler.create_get_params(self.dummy_element_key,self.get_params).get("elementKey")
        result = self.url_db_handler.create_shortened_url(shortened_base_url, shortened_path, shortened_get_params)
    
        time.sleep(2)
        for document_type in ["baseURL","path","getParams","shortened"]:
            
            assert self.url_db_handler.garbage_collection_by_document_type(document_type,datetime.now()) == 1
if __name__ == '__main__':
    unittest.main()
