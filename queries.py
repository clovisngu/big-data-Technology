import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]

### Query 1: Find Average Rating per Book
print("\n🔹 Top 10 Books with Highest Average Ratings:")
pipeline = [
    {"$group": {"_id": "$item_id", "average_rating": {"$avg": "$rating"}}},
    {"$sort": {"average_rating": -1}},
    {"$limit": 10}
]
for doc in collection.aggregate(pipeline):
    print(doc)

### Query 2: Find Top 5 Users Who Rated the Most Books
print("\n🔹 Top 5 Most Active Users:")
pipeline = [
    {"$group": {"_id": "$user_id", "ratings_count": {"$sum": 1}}},
    {"$sort": {"ratings_count": -1}},
    {"$limit": 5}
]
for doc in collection.aggregate(pipeline):
    print(doc)

print("\n✅ Queries executed successfully!")
