from dataclasses import dataclass
from typing import List

@dataclass
class Topic:
    topicName: str
    isExpanded: bool

@dataclass
class User:
    reddit_username: str
    isPublic: bool
    subscribedKeywords: List[Topic]
