import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]

# Open the file and read line by line
with open("ratings.json", "r") as file:
    data = []
    for line in file:
        data.append(json.loads(line.strip()))  # Convert each line into a JSON object

# Insert all documents into MongoDB
collection.insert_many(data)

print(f"Inserted {len(data)} records successfully!")
