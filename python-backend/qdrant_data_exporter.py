import os
import json
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

for collection in collections:
    print(f"\n{'='*50}")
    print(f"COLLECTION: {collection.upper()}")
    print(f"{'='*50}")
    
    try:
        # Get all points from the collection
        points, next_page_offset = client.scroll(
            collection_name=collection,
            limit=10000,  # Adjust if you have more than 10k points
            with_payload=True,
            with_vectors=False  # We don't need vectors for readability
        )
        
        if not points:
            print("No data found in this collection.")
            continue
            
        print(f"Total points: {len(points)}")
        print()
        
        for i, point in enumerate(points, 1):
            print(f"--- Point {i} ---")
            print(f"ID: {point.id}")
            print("Payload:")
            # Pretty print the payload
            print(json.dumps(point.payload, indent=2, default=str))
            print()
            
        # If there are more points, you might need to paginate
        if next_page_offset:
            print(f"Warning: More points available after offset {next_page_offset}. Increase limit or implement pagination.")
            
    except Exception as e:
        print(f"Error retrieving data from {collection}: {e}")

print("\nData export complete.")