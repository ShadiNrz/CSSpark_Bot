from dataclasses import dataclass
from typing import List


ExpandedSubscriptions = List[List[str]]


@dataclass
class Topic:
    topic_name: str
    is_expanded: bool


@dataclass
class User:
    _id: str
    reddit_username: str
    is_public: bool
    subscribed_keywords: List[Topic]


@dataclass
class ExtendedUser:
    _id: str
    reddit_username: str
    is_public: bool
    expanded_subscriptions: ExpandedSubscriptions


@dataclass
class Cluster:
    _id: str
    word_cluster: List[str]
