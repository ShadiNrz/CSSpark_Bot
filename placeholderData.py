from dataclasses import dataclass
from typing import List
import json

@dataclass
class Topic:
    topicName: str
    isExpanded: bool

@dataclass
class User:
    reddit_username: str
    isPublic: bool
    subscribedKeywords: List[Topic]


#JSON placeholder data (probably similar to what we'll get from the database?)
users_json = '''
[
    {
        "reddit_username": "123madskillz",
        "isPublic": true,
        "subscribedKeywords": [
            {"topicName": "ai", "isExpanded": true},
            {"topicName": "gaming", "isExpanded": false}
        ]
    },
    {
        "reddit_username": "R_Online1",
        "isPublic": true,
        "subscribedKeywords": [
            {"topicName": "ML", "isExpanded": true},
            {"topicName": "robotics", "isExpanded": false}
        ]
    }
]
'''

# Parsing the JSON string to Python objects
parsed_users = json.loads(users_json)

# Converting dictionaries to User and Topic objects
users = [User(**user_data) for user_data in parsed_users]
for user in users:
    user.subscribedKeywords = [Topic(**topic_data) for topic_data in user.subscribedKeywords]

print(users)
