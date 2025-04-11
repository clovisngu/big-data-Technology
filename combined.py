import pymongo
import json
from datetime import datetime
import os


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]


collection.create_index([("user_id", pymongo.ASCENDING)])
collection.create_index([("item_id", pymongo.ASCENDING)])
collection.create_index([("rating", pymongo.DESCENDING)])
print("Indexes created successfully!")


json_file = "ratings.json"
if os.path.exists(json_file):
    with open(json_file, "r") as file:
        data = [json.loads(line.strip()) for line in file]
    collection.insert_many(data)
    print(f"Inserted {len(data)} records from '{json_file}'")
else:
    print(f"No file named '{json_file}' found. Skipping file import.")


sample_data = [
    {"item_id": 41335427, "user_id": 0, "rating": 5, "timestamp": datetime.now()},
    {"item_id": 52342113, "user_id": 1, "rating": 4, "timestamp": datetime.now()},
    {"item_id": 19273123, "user_id": 2, "rating": 3, "timestamp": datetime.now()}
]
collection.insert_many(sample_data)
print(f"Inserted {len(sample_data)} sample records!")
