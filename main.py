import argparse
import threading
from config_loader import get_DB_garbage_collector_TTL
from database_manager import UrlDBHandler
from garbage_collector_database import GarbageCollectorDB
from shorten_composer import Shortener

def main():

    # Load or let the user set the DB and the TTL for the garbage collector
    db_base_URL, db_port, database_name, garbage_ttl,encryption_key_size = get_DB_garbage_collector_TTL(args)
    connection_string=f"mongodb://{db_base_URL}:{db_port}/"
    # Initialize the shortener, the URLDBHandler and the garbage collector
    url_db_handler=UrlDBHandler(connection_string,database_name)
    shortener_URL=Shortener(url_db_handler,garbage_ttl,encryption_key_size)
    garbage_collector=GarbageCollectorDB(garbage_ttl,url_db_handler)


    parser = argparse.ArgumentParser(description="URL shortener")
    parser.add_argument("--minify", help="Minify the given URL")
    parser.add_argument("--expand", help="Expand the given shortened URL")
    parser.add_argument("--exit", action="store_true", help="Exit the program")
    args = parser.parse_args()

    if args.exit:
        print("Closing the URL shortener.")
        return


    # Running the Garbage Collector in a separate thread
    parallel_thread = threading.Thread(target=garbage_collector)
    parallel_thread.start()

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
