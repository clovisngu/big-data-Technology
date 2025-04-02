import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

# 🔹 Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["book_ratings_db"]
collection = db["ratings"]

# 🔹 Load Data from MongoDB

# Top 10 Books with Highest Average Ratings
top_books = list(collection.aggregate([
    {"$group": {"_id": "$item_id", "average_rating": {"$avg": "$rating"}}},
    {"$sort": {"average_rating": -1}},
    {"$limit": 10}
]))

# Convert to DataFrame
df_books = pd.DataFrame(top_books)
df_books.rename(columns={"_id": "item_id"}, inplace=True)

# 🔹 Top 5 Most Active Users
top_users = list(collection.aggregate([
    {"$group": {"_id": "$user_id", "ratings_count": {"$sum": 1}}},
    {"$sort": {"ratings_count": -1}},
    {"$limit": 5}
]))

# Convert to DataFrame
df_users = pd.DataFrame(top_users)
df_users.rename(columns={"_id": "user_id"}, inplace=True)

# 🔹 Plot Top 5 Users by Rating Activity
plt.figure(figsize=(10, 5))
sns.barplot(x="user_id", y="ratings_count", data=df_users, palette="magma")
plt.xlabel("User ID")
plt.ylabel("Total Ratings")
plt.title("Top 5 Most Active Users")
plt.show()



print("✅ Visualizations generated successfully!")
