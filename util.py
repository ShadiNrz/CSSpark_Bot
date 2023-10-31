from __future__ import annotations
from typing import List
from db_types import Topic, User, KeywordExpansionDict

def find_subscribed_keywords(user: User, post_text: str) -> int:
    """
    Finds the number of user-subscribed keywords present in the given Reddit post text.

    Parameters:
        user (User): The user object containing subscribed keywords.
        post_text (str): The text of the Reddit post to search for keywords.

    Returns:
        int: The number of subscribed keywords found in the post text. This is unique per keyword and doesn't include expanded keywords.
    """
    keyword_count = 0
    # Your implementation here
    # loop through the user's subscribed topics
        # call is_topic_in_post for each topic, and increment keyword_count if true
    return keyword_count

def is_topic_in_post(topic: Topic, post_text: str, keyword_expansions: KeywordExpansionDict) -> bool:
    """
    Determines whether a given topic is present in a Reddit post's text, considering keyword expansions.

    Parameters:
        topic (Topic): The topic to search for in the post text (and wether to expand it).
        post_text (str): The text content of the Reddit post.
        keyword_expansions (KeywordExpansionDict): A mapping of keywords to their expansions.

    Returns:
        bool: True if the topic is found in the post text, considering keyword expansions; otherwise, False.
    """
    # Your implementation here
    return False
