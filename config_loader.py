
import json
config_file="./config.json"
def load_config():
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(config_file, "w") as file:
        json.dump(config, file)

def get_DB_garbage_collector_TTL(args):
    # If the values are provided by CLI we use them
    if args.database and args.garbage_collector_TTL and encryption_key_size:
        return args.database, args.garbage_collector_TTL, args.encryption_key_size

    # Otherwise from config local file
    config = load_config()
    db_base_URL = config.get("mongoDB_URL")
    db_port = config.get("mongoDB_port")
    database_name = config.get("mongoDB_database")
    garbage_ttl = config.get("garbage_collector_TTL")
    encryption_key_size = config.get("encryption_key_size")
    

    # Update configuration
    save_config(config)
    return db_base_URL, db_port, database_name, garbage_ttl, encryption_key_size