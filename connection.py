import os

from pymongo import MongoClient

from dotenv import load_dotenv, dotenv_values
from db_types import ExtendedUser, Topic, User, ExpandedSubscriptions
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

db = client["staging-reddit-bot"]
# delete and rebuild the keyword expansion list to keep it up to date
db.users.delete_many({})
db.users.insert_many(
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


def get_users(aggregate: bool):
    if aggregate:
        # fetch from db and aggregate
        raw_users = db.users.aggregate(keyword_pipeline)

        # convert to ExtendedUser objects
        users = []
        for user_data in raw_users:
            if "expanded_subscriptions" in user_data:
                expanded_subs = user_data["expanded_subscriptions"]
                if not isinstance(expanded_subs, ExpandedSubscriptions):
                    raise TypeError(
                        "expanded_subscriptions must be a list of list of strings"
                    )
                user_data["expanded_subscriptions"] = expanded_subs

            users.append(ExtendedUser(**user_data))
    else:
        raw_users = db.users.find()
        users = [User(**user_data) for user_data in raw_users]
        for user in users:
            user.subscribed_keywords = [
                Topic(**topic_data) for topic_data in user.subscribed_keywords
            ]

    return users


print(get_users(True))


def get_user_by_username(username):
    return db.users.find_one({"reddit_username": username})


# have not tested
def add_keyword_to_user(username, keyword):
    db.users.update_one(
        {"reddit_username": username},
        {
            "$push": {
                # we'll default to expanded and ask the user to change it if they want
                "subscribed_keywords": {"topic_name": keyword, "is_expanded": True}
            }
        },
    )


# have not tested
def unexpand_keyword_for_user(username, keyword):
    db.users.update_one(
        {"reddit_username": username, "subscribed_keywords.topic_name": keyword},
        {"$set": {"subscribed_keywords.$.is_expanded": False}},
    )


# have not tested
def remove_keyword_from_user(username, keyword):
    db.users.updaåte_one(
        {"reddit_username": username},
        {"$pull": {"subscribed_keywords": {"topic_name": keyword}}},
    )


client.close()
