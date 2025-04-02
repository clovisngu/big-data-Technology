import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]

# Create indexes for faster queries
collection.create_index([("user_id", pymongo.ASCENDING)])  # Index for user-based queries
collection.create_index([("item_id", pymongo.ASCENDING)])  # Index for book-based queries
collection.create_index([("rating", pymongo.DESCENDING)])  # Index for sorting by ratings

print("Indexes created successfully!")
