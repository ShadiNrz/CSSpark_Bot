import os

from pymongo import MongoClient

from dotenv import load_dotenv, dotenv_values
from db_types import ExtendedUser, Topic, User
from keyword_pipeline import keyword_pipeline

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

prod = client["prod-reddit-bot"]
staging = client["staging-reddit-bot"]


def rebuild_sample_users_db(db):
    staging.users.delete_many({})
    staging.users.insert_many(
        [
            {
                "reddit_username": "123madskillz",
                "is_public": True,
                "subscribed_keywords": [
                    {"topic_name": "ai", "is_expanded": False},
                    {"topic_name": "gaming", "is_expanded": True},
                ],
            },
            {
                "reddit_username": "R_Online1",
                "is_public": True,
                "subscribed_keywords": [
                    {"topic_name": "ml", "is_expanded": True},
                    {"topic_name": "robotics", "is_expanded": False},
                ],
            },
        ]
    )


def rebuild_keyword_expansion_db(db):
    # delete and rebuild the keyword expansion list to keep it up to date
    db.keyword_expansion.delete_many({})
    db.keyword_expansion.insert_many(
        [
            {
                "word_cluster": [
                    "ai",
                    "ml",
                    "artificial intelligence",
                    "machine learning",
                    "deep learning",
                ],
            },
            {"word_cluster": ["gaming", "video games"]},
            {"word_cluster": ["robotics", "robots", "hri"]},
        ]
    )


def get_users(db, aggregate: bool):
    if aggregate:
        # fetch from db and aggregate
        raw_users = db.users.aggregate(keyword_pipeline)

        # convert to ExtendedUser objects
        users = [ExtendedUser(**user_data) for user_data in raw_users]
    else:
        raw_users = db.users.find()
        users = [User(**user_data) for user_data in raw_users]
        for user in users:
            user.subscribed_keywords = [
                Topic(**topic_data) for topic_data in user.subscribed_keywords
            ]

    return users


def get_user_by_username(db, username, aggregate=False):
    return db.users.find_one({"reddit_username": username})


def create_user(db, username, is_public=True, subscribed_keywords=[]):
    db.users.insert_one(
        {
            "reddit_username": username,
            "is_public": is_public,
            "subscribed_keywords": subscribed_keywords,
        }
    )


def add_keyword_to_user(db, username, keyword):
    db.users.update_one(
        {"reddit_username": username},
        {
            "$push": {
                # we'll default to expanded and ask the user to change it if they want
                "subscribed_keywords": {"topic_name": keyword, "is_expanded": True}
            }
        },
    )


def unexpand_keyword_for_user(db, username, keyword):
    db.users.update_one(
        {"reddit_username": username, "subscribed_keywords.topic_name": keyword},
        {"$set": {"subscribed_keywords.$.is_expanded": False}},
    )


def remove_keyword_from_user(db, username, keyword):
    db.users.update_one(
        {"reddit_username": username},
        {"$pull": {"subscribed_keywords": {"topic_name": keyword}}},
    )


# client.close()
