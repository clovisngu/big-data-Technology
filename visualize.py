import pymongo
import json
import matplotlib.pyplot as plt

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client["book_ratings_db"]  # Database name

# Collections
ratings_collection = db["ratings"]
metadata_collection = db["metadata"]


avg_ratings = ratings_collection.aggregate([
    {
        "$group": {
            "_id": "$item_id",  # Group by item_id (book)
            "avg_rating": {"$avg": "$rating"}  # Calculate average rating
        }
    },
    {"$sort": {"avg_rating": -1}},  # Sort by average rating (descending)
    {"$limit": 10}  # Limit to top 10
])

# Fetch titles for top 10 rated books
top_books = []
for avg in avg_ratings:
    item_id = avg["_id"]
    avg_rating = avg["avg_rating"]

    # Find the book title using the item_id
    book = metadata_collection.find_one({"item_id": item_id})

    if book:
        title = book["title"]
        top_books.append({"title": title, "avg_rating": avg_rating})

# Print the top 10 books by average rating
print("\nTop 10 Books by Average Rating:")
for idx, book in enumerate(top_books, 1):
    print(f"{idx}. {book['title']} - Average Rating: {book['avg_rating']:.2f}")



most_rated_books = ratings_collection.aggregate([
    {
        "$group": {
            "_id": "$item_id",  # Group by item_id (book)
            "rating_count": {"$count": {}},  # Count the number of ratings for each book
        }
    },
    {"$sort": {"rating_count": -1}},  # Sort by rating count (descending)
    {"$limit": 10}  # Limit to top 10
])

# Fetch titles for most rated books
top_most_rated_books = []
for book in most_rated_books:
    item_id = book["_id"]
    rating_count = book["rating_count"]

    # Find the book title using the item_id
    book_metadata = metadata_collection.find_one({"item_id": item_id})

    if book_metadata:
        title = book_metadata["title"]
        top_most_rated_books.append({"title": title, "rating_count": rating_count})

# Print the top 10 most rated books
print("\nTop 10 Most Rated Books:")
for idx, book in enumerate(top_most_rated_books, 1):
    print(f"{idx}. {book['title']} - Number of Ratings: {book['rating_count']}")


book_titles = [book['title'] for book in top_books]
avg_ratings = [book['avg_rating'] for book in top_books]

plt.figure(figsize=(10, 6))
plt.barh(book_titles, avg_ratings, color='skyblue')
plt.xlabel('Average Rating')
plt.title('Top 10 Books by Average Rating')
plt.gca().invert_yaxis()  # Invert y-axis to show the highest rating at the top
plt.show()


most_rated_book_titles = [book['title'] for book in top_most_rated_books]
rating_counts = [book['rating_count'] for book in top_most_rated_books]

plt.figure(figsize=(10, 6))
plt.barh(most_rated_book_titles, rating_counts, color='lightcoral')
plt.xlabel('Number of Ratings')
plt.title('Top 10 Most Rated Books')
plt.gca().invert_yaxis()  # Invert y-axis to show the highest rating at the top
plt.show()
