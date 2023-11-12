import json
from db_types import Topic, User, Cluster
from typing import List

# JSON placeholder data (probably similar to what we'll get from the database?)
users_json = """
[
    {
        "reddit_username": "123madskillz",
        "is_public": true,
        "subscribed_keywords": [
            {"topic_name": "ai", "is_expanded": true},
            {"topic_name": "gaming", "is_expanded": false}
        ]
    },
    {
        "reddit_username": "R_Online1",
        "is_public": true,
        "subscribed_keywords": [
            {"topic_name": "ML", "is_expanded": true},
            {"topic_name": "robotics", "is_expanded": false}
        ]
    }
]
"""
keyword_clusters_json = """
[
   {
      "word_cluster":[
         "ai",
         "ml",
         "artificial intelligence",
         "machine learning",
         "deep learning"
      ]
   },
   {
      "word_cluster":[
         "gaming",
         "video games"
      ]
   },
   {
      "word_cluster":[
         "robotics",
         "robots",
         "hri"
      ]
   }
]
"""
# Parsing the JSON string to Python objects
parsed_users = json.loads(users_json)
# Converting dictionaries to User and Topic objects
users = [User(**user_data) for user_data in parsed_users]
for user in users:
    user.subscribed_keywords = [
        Topic(**topic_data) for topic_data in user.subscribed_keywords
    ]

parsed_keyword_dict: List[Cluster] = json.loads(keyword_clusters_json)

print(users)
