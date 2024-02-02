import unittest
from datetime import datetime, timedelta
from pymongo import MongoClient
from database_manager import MongoDBHandler, UrlHandler

# Set up a test MongoDB connection
test_database_url = "mongodb://localhost:27017/"
test_database_name = "test_database"

class TestMongoDBHandler(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(test_database_url)
        self.db_handler = MongoDBHandler(test_database_url, test_database_name)
        self.collection_name = "test_collection"

    def tearDown(self):
        self.client.drop_database(test_database_name)

    def test_create_document(self):
        document = {"elementKey": "123", "field1": "value1"}
        inserted_id = self.db_handler.create_document(self.collection_name, document)
        self.assertIsNotNone(inserted_id)

    def test_delete_document(self):
        document = {"elementKey": "456", "field1": "value2"}
        self.db_handler.create_document(self.collection_name, document)
        deleted_count = self.db_handler.delete_document(self.collection_name, "456")
        self.assertEqual(deleted_count, 1)

    def test_retrieve_document_by_element_key(self):
        document = {"elementKey": "789", "field1": "value3"}
        self.db_handler.create_document(self.collection_name, document)
        retrieved_document = self.db_handler.retrieve_document_by_element_key(self.collection_name, "789")
        self.assertIsNotNone(retrieved_document)

    def test_count_documents_by_query(self):
        document1 = {"elementKey": "111", "field1": "value4"}
        document2 = {"elementKey": "222", "field1": "value5"}
        self.db_handler.create_document(self.collection_name, document1)
        self.db_handler.create_document(self.collection_name, document2)
        query = {"field1": "value4"}
        count = self.db_handler.count_documents_by_query(self.collection_name, query)
        self.assertEqual(count, 1)

    def test_check_document_existance(self):
        document = {"elementKey": "333", "field1": "value6"}
        self.db_handler.create_document(self.collection_name, document)
        existance = self.db_handler.check_document_existance(self.collection_name, "333")
        self.assertFalse(existance)

    def test_update_document(self):
        document = {"elementKey": "444", "field1": "value7", "TTLDateTime": datetime.now()}
        self.db_handler.create_document(self.collection_name, document)
        new_TTL_date_time = datetime.now() + timedelta(days=1)
        modified_count = self.db_handler.update_document(self.collection_name, "444", new_TTL_date_time)
        self.assertEqual(modified_count, 1)

    def test_search_free_key(self):
        self.db_handler.create_document(self.collection_name, {"elementKey": "1"})
        self.db_handler.create_document(self.collection_name, {"elementKey": "2"})
        free_key = self.db_handler.search_free_key(self.collection_name, 3)
        self.assertEqual(free_key, 3)

    def test_delete_expired_documents(self):
        current_date_time = datetime.now()
        past_date_time = current_date_time - timedelta(days=1)
        document = {"elementKey": "555", "field1": "value8", "TTLDateTime": past_date_time}
        self.db_handler.create_document(self.collection_name, document)
        deleted_count = self.db_handler.delete_expired_documents(self.collection_name, current_date_time)
        self.assertEqual(deleted_count, 1)

class TestUrlHandler(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(test_database_url)
        self.url_handler = UrlHandler(test_database_url, test_database_name)

    def tearDown(self):
        self.client.drop_database(test_database_name)

    def test_create_shortened_url(self):
        inserted_id = self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        self.assertIsNotNone(inserted_id)

    def test_create_base_url(self):
        inserted_id = self.url_handler.create_base_url("123", "https://example.com")
        self.assertIsNotNone(inserted_id)

    def test_create_path(self):
        inserted_id = self.url_handler.create_path("456", "/path")
        self.assertIsNotNone(inserted_id)

    def test_create_get_params(self):
        inserted_id = self.url_handler.create_get_params("789", "param1=value1")
        self.assertIsNotNone(inserted_id)

    def test_get_original_url(self):
        element_key = self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        original_url = self.url_handler.get_original_url(element_key)
        expected_url = "https://example.com/path?param1=value1"
        self.assertEqual(original_url, expected_url)

    def test_renew_TTLDateTime_document(self):
        element_key = self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        renewed = self.url_handler.renew_TTLDateTime_document("shortened", element_key)
        self.assertEqual(renewed, 1)

    def test_get_num_documents_by_element_key_length(self):
        self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        count = self.url_handler.get_num_documents_by_element_key_length("shortened", 3)
        self.assertEqual(count, 1)

    def test_return_lowest_free_element_key_by_length(self):
        self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        free_key = self.url_handler.return_lowest_free_element_key_by_length("shortened", 3)
        self.assertEqual(free_key, 2)

    def test_garbage_collection_by_document_type(self):
        self.url_handler.create_shortened_url("https://example.com", "/path", "param1=value1")
        deleted_count = self.url_handler.garbage_collection_by_document_type("shortened", 0)
        self.assertEqual(deleted_count, 0)

if __name__ == '__main__':
    unittest.main()
