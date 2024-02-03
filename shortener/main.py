import argparse
import time
from config_loader import get_DB_garbage_collector_TTL
from database_manager import UrlDBHandler
from shorten_composer import Shortener

def main():

    #Load elements from config
    db_base_URL, db_port, database_name, garbage_ttl,encryption_key_size = get_DB_garbage_collector_TTL()
    connection_string=f"mongodb://{db_base_URL}:{db_port}/"

    # Initialize the shortener, the URLDBHandler
    url_db_handler=UrlDBHandler(connection_string,database_name)
    shortener_URL=Shortener(url_db_handler,garbage_ttl,encryption_key_size)
    
    parser = argparse.ArgumentParser(description="URL Shortener/Expander")
    parser.add_argument("--minify", help="Shorten a URL")
    parser.add_argument("--expand", help="Expand a shortened URL")
    

    args = parser.parse_args()

    if args.minify:
        
        minified_url = shortener_URL.shorten_url(args.minify)
        print(f"Result: {minified_url}")

    elif args.expand:
        original_url = shortener_URL.compose_original_url(args.expand)
        print(f"Result: {original_url}")

    else:
        print("Please provide either --minify or --expand parameter.")


if __name__ == "__main__":
    main()
