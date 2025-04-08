import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["book_ratings_db"]  # Database name

# Collections
ratings_collection = db["ratings"]
metadata_collection = db["metadata"]

with open("ratings.json", "r", encoding="utf-8") as file:
    ratings_data = []
    for line in file:
        try:
            rating = json.loads(line)
            ratings_data.append(rating)
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")

ratings_collection.insert_many(ratings_data)

with open("metadata.json", "r", encoding="utf-8") as file:
    metadata_data = []
    for line in file:
        try:
            book = json.loads(line)
            metadata_data.append(book)
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line}")


metadata_collection.insert_many(metadata_data)



# Aggregate average ratings for each book
avg_ratings = ratings_collection.aggregate([
    {
        "$group": {
            "_id": "$item_id",  # Group by item_id (book)
            "avg_rating": {"$avg": "$rating"}  # Calculate average rating
        }
    }
])


for avg in avg_ratings:
    item_id = avg["_id"]
    avg_rating = avg["avg_rating"]

    # Find the book title using the item_id
    book = metadata_collection.find_one({"item_id": item_id})

    if book:
        title = book["title"]
        print(f"Book: {title}, Average Rating: {avg_rating:.2f}")
    else:
        print(f"Book with")
