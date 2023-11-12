import os

from pymongo import MongoClient

from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")
MONGODB_URI = os.environ["MONGODB_URI"]
# Create a new client and connect to the server
client = MongoClient(MONGODB_URI)
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

for db in client.list_databases():
    print(db)

db = client["staging-reddit-bot"]
# delete and rebuild the keyword expansion list to keep it up to date
db.keyword_expansion.delete_many({})
db.keyword_expansion.insert_many(
    [
        {
            "name": "ai",
            "expansions": [
                "artificial intelligence",
                "machine learning",
                "deep learning",
            ],
        },
        {"name": "gaming", "expansions": ["gaming", "video games"]},
        {"name": "ml", "expansions": ["machine learning", "deep learning"]},
        {"name": "robotics", "expansions": ["robotics", "robots"]},
    ]
)


def get_users():
    return db.users.find()


def get_user_by_username(username):
    return db.users.find_one({"reddit_username": username})


client.close()
