from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Topic:
    topicName: str
    isExpanded: bool

@dataclass
class User:
    reddit_username: str
    isPublic: bool
    subscribedKeywords: List[Topic]

KeywordExpansionDict = Dict[str, List[str]]