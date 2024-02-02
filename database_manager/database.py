from pymongo import MongoClient
from datetime import datetime, timedelta

class MongoDBHandler:
    def __init__(self, database_url, database_name):
        self.client=MongoClient(database_url)
        self.db=self.client[database_name]

    def create_document(self, collection_name, document):
        collection=self.db[collection_name]
        result=collection.insert_one(document)
        return result.inserted_id

    def delete_document(self, collection_name, element_key):
        collection=self.db[collection_name]
        result=collection.delete_one({"elementKey":str(element_key) })
        return result.deleted_count
    
    def retrieve_shortened_by_its_elements(self,base_url_element_key,path_element_key,get_params_element_key):
        collection=self.db["shortened"]
        result=collection.find({"baseURL_elementKey": base_url_element_key, "path_elementKey": path_element_key, "getParams_elementKey": get_params_element_key})
        return result if result is not None else None

    def retrieve_base_url(self,base_url):
        collection=self.db["baseURL"]
        result=collection.find_one({"baseURL": base_url})
        return result if result is not None else None
    
    def retrieve_path(self,path):
        collection=self.db["path"]
        result=collection.find_one({"path": path})
        return result if result is not None else None
    
    def retrieve_getParams(self,getParams):
        collection=self.db["getParams"]
        result=collection.find_one({"getParams": getParams})
        return result if result is not None else None

    def retrieve_document_by_element_key(self, collection_name, element_key):
        collection=self.db[collection_name]
        result=collection.find_one({"elementKey": element_key})
        return result if result is not None else None
    
    def count_documents_by_query(self,collection_name, query=None):
        collection=self.db[collection_name]
        return collection.count_documents(query)
    
    def check_document_existance(self, collection_name, element_key):
        collection=self.db[collection_name]
        result=collection.find_one({"elementKey": element_key})
        return result if result is not None else None

    def get_document_by_id(self,collection_name,id):
        collection=self.db[collection_name]
        result=collection.find_one({"_id":id})
        return result if result is not None else None

    # Update mostly limited to renew the TTLDateTime
    def update_document(self, collection_name, element_key, new_TTL_date_time):
        collection=self.db[collection_name]
        result=collection.update_one({"elementKey": str(element_key)},{"$set": {"TTLDateTime": new_TTL_date_time}})
        return result

    # Apply binary search according to the elementKeyLength: 62 elements to the power of elementKeyLength. In case of full sequence it returns None

    def search_free_key(self,collection_name, element_key_length):
        
        start, end=1,element_key_length
        while start<=end:
            
            middle=(start + end) // 2
            if (self.check_document_existance(collection_name,str(middle)) is not None):
                start=middle +1
            else:
                end=middle-1

        return start if start <= element_key_length else None

    # Delete all of the document of a certain collection having expired TTL
    def delete_expired_documents(self, collection_name, time_passed):
        collection=self.db[collection_name]
        result=collection.delete_many({"TTLDateTime": {"$lt": time_passed}}).deleted_count
        return result

class UrlDBHandler:

    _single_instance=None

    def __new__(cls, *args, **kwargs):
        if not cls._single_instance:
            cls._single_instance=super(UrlDBHandler, cls).__new__(UrlDBHandler)
        return cls._single_instance
    
    def __init__(self, database_url, database_name):
        if not hasattr(self, 'initialized'):
            self.db_handler=MongoDBHandler(database_url, database_name)
            self.initialized=True
        

    # Creator for the for document entities
    def create_shortened_url(self, base_url, path, get_params):
        current_date_time=datetime.now()
        document={"elementKey": (str(base_url) + str(path) + str(get_params)), "baseURL_elementKey": str(base_url), "path_elementKey": str(path), "getParams_elementKey": str(get_params), "TTLDateTime": current_date_time}
        created_id=self.db_handler.create_document("shortened", document)
        return self.db_handler.get_document_by_id("shortened",created_id)
    
    def create_base_url(self, element_key, base_url):
        current_date_time=datetime.now()
        document={"elementKey": str(element_key), "baseURL": base_url, "TTLDateTime":current_date_time}
        created_id=self.db_handler.create_document("baseURL", document)
        return self.db_handler.get_document_by_id("baseURL",created_id)

    def create_path(self, element_key, path):
        current_date_time=datetime.now()
        document={"elementKey": str(element_key), "path": path, "TTLDateTime": current_date_time}
        created_id=self.db_handler.create_document("path", document)
        return self.db_handler.get_document_by_id("path",created_id)

    def create_get_params(self, element_key, get_params):
        current_date_time=datetime.now()
        document={"elementKey": str(element_key), "getParams": get_params, "TTLDateTime": current_date_time}
        created_id=self.db_handler.create_document("getParams", document)
        return self.db_handler.get_document_by_id("getParams",created_id)

    # Method to return the base URL, the path and the GET parameters by a given elementKey for the URL
    def get_original_url(self,element_key):
        shorten_url=self.db_handler.retrieve_document_by_element_key("shortened",element_key)
        if shorten_url is not None:
            # Take each sub-document
            base_url=self.db_handler.retrieve_document_by_element_key("baseURL",shorten_url.get("baseURL_elementKey"))
            path=self.db_handler.retrieve_document_by_element_key("path",shorten_url.get("path_elementKey"))
            get_params=self.db_handler.retrieve_document_by_element_key("getParams",shorten_url.get("getParams_elementKey"))

            # Build up the final string: we default the strings as empty
            return {"original_URL": "https://" + base_url.get("baseURL","") + path.get("path","") + "?" + get_params.get("getParams",""), "TTLDateTime":shorten_url.get("TTLDateTime")}
        else:
            # no shorten URL is found 
            return "not_found"
        
    # check if a shortened URL already exists
        
    def check_existing_shortened(self,element_key):
        result=self.db_handler.retrieve_document_by_element_key("shortened",element_key)
        return result
    
    # Check if a base URL already exists
    def check_existing_baseURL(self,base_url):
        result=self.db_handler.retrieve_base_url(base_url)
        return result
    
    # Check if a path already exists
    def check_existing_path(self,path):
        result=self.db_handler.retrieve_path(path)
        return result
    
    # Check if a getParams list already exists
    def check_existing_getParams(self,getParams):
        result=self.db_handler.retrieve_getParams(getParams)
        return result

    # The update in this use case is mostly limited to renewing the TTLDateTime field
    def renew_TTLDateTime_document(self,document_name,element_key):
        current_date_time=datetime.now()
        self.db_handler.update_document(document_name,element_key,current_date_time)
        return self.db_handler.retrieve_document_by_element_key(document_name,element_key)
    

    # Return number of documents by the given elementKey length
    def get_num_documents_by_element_key_length(self, document_name,element_length):
        query={"$expr": {"$eq": [{"$strLenCP": "$elementKey"}, element_length]}}
        return self.db_handler.count_documents_by_query(document_name, query)
    
    # Return a free elementKey according to the elementKey length so that it will be returned the lowest one
    def return_lowest_free_element_key_by_length(self,document_name,element_length):
        
        # If we reached out the number of existing keys we have to return empty, otherwise we search for the 
        if self.get_num_documents_by_element_key_length(document_name,element_length) == (62 ** int(element_length)):
            return None
        else:
            return self.db_handler.search_free_key(document_name,62 ** int(element_length))

    # Method for the garbage collector to delete all of the expired documents in a certain collection
    def garbage_collection_by_document_type(self,document_name,past_delta_time):
        return  self.db_handler.delete_expired_documents(document_name,past_delta_time)
        
    # method to retrieve an already existing shortened by its three elements

    def get_shortened_by_elements(self,base_url_element_key,path_element_key,get_params_element_key):
        return self.db_handler.retrieve_shortened_by_its_elements(base_url_element_key,path_element_key,get_params_element_key)
    