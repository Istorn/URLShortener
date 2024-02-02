from database_manager import UrlDBHandler
from datetime import datetime


class GarbageCollectorDB:
    _single_instance=None

    def __new__(cls, *args, **kwargs):
        if not cls._single_instance:
            cls._single_instance=super(GarbageCollectorDB, cls).__new__(GarbageCollectorDB)
        return cls._single_instance
    
    def __init__(self, garbage_TTL,url_db_handler:UrlDBHandler):
        if not hasattr(self, 'initialized'):

            self.last_execution_time=datetime.now()
            self.garbage_TTL=garbage_TTL
            self.initialized=True
            self.db_handler=url_db_handler
    
    # Method to remove the unused elements from the DB
    def collect_garbage_from_DB(self):
        current_moment=datetime.now()
        time_delta=current_moment - self.last_execution_time
        seconds_TTL=time_delta(seconds=self.garbage_TTL)
        if time_delta > seconds_TTL:
            
            # Time has passed to gather garbage
            self.db_handler.garbage_collection_by_document_type("getParams",current_moment)
            self.db_handler.garbage_collection_by_document_type("path",current_moment)
            self.db_handler.garbage_collection_by_document_type("baseURL",current_moment)
            self.db_handler.garbage_collection_by_document_type("shortened",current_moment)
            
            # We update the last execution time with a fresher datetime.now due to the time needed to clean the DB
            self.last_execution_time=datetime.now()

