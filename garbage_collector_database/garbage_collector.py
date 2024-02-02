from database_manager import UrlDBHandler
from datetime import datetime, timedelta


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
        seconds_TTL=timedelta(seconds=self.garbage_TTL)
        if time_delta > seconds_TTL:
            print(f"Garbage collector started at {current_moment.strftime("%H:%M:%S %Y-%m-%d ")}")
            
            # Time has passed to gather garbage
            num_get_params_del=self.db_handler.garbage_collection_by_document_type("getParams",current_moment)
            num_path_del=self.db_handler.garbage_collection_by_document_type("path",current_moment)
            num_baseURL_del=self.db_handler.garbage_collection_by_document_type("baseURL",current_moment)
            num_shortened_del=self.db_handler.garbage_collection_by_document_type("shortened",current_moment)
            
            print(f"Garbage collector ended at {current_moment.strftime("%H:%M:%S %Y-%m-%d ")}")
            print(f"Elements removed:\r\n- GET Parameters: {num_get_params_del}\r\n- Path(s): {num_path_del}\r\n- base URL(s): {num_baseURL_del}\r\n- Shortened URL(s): {num_shortened_del}")
            # We update the last execution time with a fresher datetime.now due to the time needed to clean the DB
            self.last_execution_time=datetime.now()

