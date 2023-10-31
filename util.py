from __future__ import annotations
from typing import List
from db_types import Topic, User
def get_subscribed_keywords(user: User) -> List[str]:
    """
    Returns a list of expanded topic names for a given user.

    Parameters:
        user (User): The user object containing subscribed keywords.

    Returns:
        List[str]: A list of expanded topic names.
    """
    expanded_keywords = []
    return expanded_keywords