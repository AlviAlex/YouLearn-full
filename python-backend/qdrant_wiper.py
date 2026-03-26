import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    print("Error: QDRANT_URL and QDRANT_API_KEY must be set in environment variables.")
    exit(1)

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

collections = ["youlearn_docs", "youlearn_memory"]

print("WARNING: This will permanently delete all data from the following collections:")
for collection in collections:
    print(f"  - {collection}")

confirm = input("\nType 'YES' to confirm deletion: ")
if confirm != "YES":
    print("Operation cancelled.")
    exit(0)

for collection in collections:
    try:
        if client.collection_exists(collection):
            client.delete_collection(collection)
            print(f"✓ Deleted collection: {collection}")
        else:
            print(f"Collection {collection} does not exist.")
    except Exception as e:
        print(f"Error deleting {collection}: {e}")

print("\nAll data has been wiped. Qdrant is now fresh.")