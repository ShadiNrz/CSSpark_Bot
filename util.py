from __future__ import annotations
from typing import Dict, List
from db_types import Topic, User, ExpandedSubscriptions


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
        matching_keywords = count_subscribed_keywords(
            user.expanded_subscriptions, post_text
        )
        if matching_keywords > 0:
            user_keyword_counts[user.reddit_username] = matching_keywords
    return user_keyword_counts


def count_subscribed_keywords(
    expanded_subscriptions: ExpandedSubscriptions, post_text: str
) -> int:
    """
    Counts the number of keyword arrays where at least one keyword is present in a Reddit post's text.

    Parameters:
        expanded_subscriptions (list of list of str): Arrays of keywords, including expansions.
        post_text (str): The text content of the Reddit post.

    Returns:
        int: The count of keyword arrays where at least one keyword is found in the post text.
    """
    # TODO: TEST ME
    matched_count = 0
    for keyword_array in expanded_subscriptions:
        if any(keyword.lower() in post_text.lower() for keyword in keyword_array):
            matched_count += 1
    return matched_count
