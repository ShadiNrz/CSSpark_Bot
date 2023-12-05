import os

from pymongo import MongoClient

from dotenv import load_dotenv, dotenv_values
from db_types import Cluster, ExtendedUser, Topic, User
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


def rebuild_admin_settings_db(db):
    print("REBUILDING ADMIN SETTINGS DB")
    db.admin_settings.delete_many({})
    db.admin_settings.insert_one({"ping_limit": 7})


def rebuild_sample_users_db():
    print("REBUILDING USERS DB")
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
    print("REBUILDING KEYWORD EXPANSION DB")
    # delete and rebuild the keyword expansion list to keep it up to date
    db.keyword_expansion.delete_many({})
    db.keyword_expansion.insert_many(
        [
            {
                "word_cluster": [
                    "machine learning",
                    "artificial intelligence",
                    "ai",
                    "ml",
                    "supervised learning",
                    "unsupervised learning",
                    "deep learning",
                    "neural networks",
                    "natural language processing",
                    "nlp",
                    "predictive analytics",
                    "feature engineering",
                    "reinforcement learning",
                    "algorithm development",
                ],
            },
            {
                "word_cluster": [
                    "human-centered computing",
                    "hcc",
                    "social computing",
                    "sc",
                    "ethical computing",
                    "human-computer interaction",
                    "hci",
                ]
            },
            {
                "word_cluster": [
                    "online community",
                    "virtual communities",
                    "online communities",
                    "sense of virtual communities",
                    "sovc",
                    "virtual collaboration",
                ]
            },
            {
                "word_cluster": [
                    "social media",
                    "user engagement strategies",
                    "reddit",
                    "twitter",
                    "facebook",
                    "instagram",
                    "tiktok",
                    "linkedin",
                    "youtube",
                ]
            },
            {
                "word_cluster": [
                    "social support",
                    "spiritual support",
                    "emotional support",
                    "informational support",
                    "instrumental support",
                    "esteem support",
                    "network support",
                    "peer support",
                    "mental health services",
                    "counseling and therapy",
                    "social welfare",
                    "crisis intervention",
                    "support networks",
                    "family services",
                    "self-help strategies",
                ]
            },
        ]
    )


def get_clusters(db):
    db_clusters = db.keyword_expansion.find()
    clusters = [Cluster(**cluster_data) for cluster_data in db_clusters]
    return clusters


def get_ping_limit(db):
    return db.admin_settings.find_one()["ping_limit"]


def set_ping_limit(db, ping_limit):
    db.admin_settings.update_one(
        {},
        {"$set": {"ping_limit": ping_limit}},
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


def set_user_is_public(db, username, is_public):
    db.users.update_one(
        {"reddit_username": username},
        {"$set": {"is_public": is_public}},
    )


# client.close()
