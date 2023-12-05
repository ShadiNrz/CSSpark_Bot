from __future__ import annotations
from typing import Dict, List
from db_types import Cluster, Topic, User, ExpandedSubscriptions
import re


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


def is_keyword_present(text, keyword):
    pattern = r"\b" + re.escape(keyword) + r"\b"
    return re.search(pattern, text, re.IGNORECASE) is not None


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
    matched_count = 0
    for keyword_array in expanded_subscriptions:
        if any(is_keyword_present(post_text, keyword) for keyword in keyword_array):
            matched_count += 1
    return matched_count


def get_cluster(keyword: str, clusters: List[Cluster]) -> bool:
    """
    Returns the cluster that contains the given keyword.

    Parameters:
        keyword (str): The keyword to find.
        clusters (List[Cluster]): A list of clusters, where each cluster is a list of keywords.

    Returns:
        List[str]: The cluster that contains the given keyword.
    """
    for cluster in clusters:
        if keyword in cluster.word_cluster:
            return cluster.word_cluster
    return None
