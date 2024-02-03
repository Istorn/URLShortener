from config_loader import get_DB_garbage_collector_TTL, garbage_collector_runner
from garbage_collector_database import GarbageCollectorDB
from database_manager import UrlDBHandler

if __name__ == "__main__":
    #Load elements from config
    db_base_URL, db_port, database_name, garbage_ttl,encryption_key_size = get_DB_garbage_collector_TTL()
    connection_string=f"mongodb://{db_base_URL}:{db_port}/"
    
    url_db_handler=UrlDBHandler(connection_string,database_name)
    garbage_collector=GarbageCollectorDB(garbage_ttl,url_db_handler)
    garbage_collector_runner(garbage_collector,garbage_ttl)
