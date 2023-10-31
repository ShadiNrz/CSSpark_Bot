from __future__ import annotations
from typing import Dict, List
from db_types import Topic, User, KeywordExpansionDict

def get_user_keyword_counts(users: List[User], post_text: str) -> Dict[str, int]:
    """
    Counts the number of subscribed keywords for each user in a given Reddit post text.

    Parameters:
        users (List[User]): A list of User objects containing their subscribed keywords.
        post_text (str): The text content of the Reddit post.

    Returns:
        Dict[str, int]: A dictionary mapping usernames to the count of their subscribed keywords in the post text.
    """
    user_keyword_counts = {}
    for user in users:
        matching_keywords = count_subscribed_keywords(user, post_text)
        if(matching_keywords > 0):
            user_keyword_counts[user.reddit_username] = matching_keywords
    return user_keyword_counts

def count_subscribed_keywords(user: User, post_text: str) -> int:
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
