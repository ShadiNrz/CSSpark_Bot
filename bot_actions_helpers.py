from connection import add_keyword_to_user, create_user, get_user_by_username


def get_or_create_user(db, reddit_username, keyword):
    user = get_user_by_username(db, reddit_username)
    if user is None:
        create_user(
            db, reddit_username, True, [{"topic_name": keyword, "is_expanded": True}]
        )
        user = get_user_by_username(db, reddit_username)
        return user
    add_keyword_to_user(db, reddit_username, keyword)
    return user


def is_user_subscribed_to_keyword(user, keyword):
    """
    Check if the user is subscribed to a specific keyword.

    Parameters:
        user: The user object containing subscribed keywords.
        keyword (str): The keyword to check.

    Returns:
        bool: True if the user is subscribed to the keyword, False otherwise.
    """
    return any(keyword in topic["topic_name"] for topic in user["subscribed_keywords"])
