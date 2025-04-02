import pymongo
from datetime import datetime

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]

# Sample data
data = [
    {"item_id": 41335427, "user_id": 0, "rating": 5, "timestamp": datetime.now()},
    {"item_id": 52342113, "user_id": 1, "rating": 4, "timestamp": datetime.now()},
    {"item_id": 19273123, "user_id": 2, "rating": 3, "timestamp": datetime.now()}
]

# Insert data into the collection
collection.insert_many(data)

print(f"Inserted {len(data)} records!")
