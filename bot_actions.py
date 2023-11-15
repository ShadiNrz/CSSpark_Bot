from connection import (
    add_keyword_to_user,
    get_clusters,
    get_user_by_username,
    get_users,
    create_user,
    remove_keyword_from_user,
    unexpand_keyword_for_user,
)
from util import get_cluster, get_user_keyword_counts

MAX_PINGS = 7  # TODO: Add this to the database so that mods can configure it

def on_reddit_post(db, submission):
    """
    Called when a new Reddit post is detected.

    Parameters:
        db (Database): The database object.
        submission (Submission): The Reddit post object.
    """
    title = submission.title.upper()
    post_text = submission.selftext.upper()

    # Get all users from the database
    users = get_users(db, True)
    filtered_users = get_user_keyword_counts(users, f"{title} {post_text}")
    # get the top MAX_PINGS users (not sure if this works)
    # TODO: seperate public from private users
    top_users = sorted(filtered_users, key=filtered_users.get, reverse=True)[:MAX_PINGS]
    top_users_str = ", ".join(top_users)
    submission.reply(
        f"{top_users_str} you are mentioned because your keywords were found in this post!"
    )
    print(f"Replied to submission {submission.id}: {title}")


def on_subscribe(db, reddit_username, keyword, respond):
    """
    Called when a user subscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user subscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    print(f"User {reddit_username} subscribed to keyword {keyword}.")
    user = get_user_by_username(db, reddit_username)
    if user == None:
        print(f"User {reddit_username} not found, creating an account")
        create_user(
            db, reddit_username, True, [{"topic_name": keyword, "is_expanded": True}]
        )
    else:
        print(f"User {reddit_username} found, adding keyword")
        add_keyword_to_user(db, reddit_username, keyword)

    print(f"subscribed to {keyword}")

    # check if keyword is part of a cluster
    if get_cluster(keyword, get_clusters(db)):
        print(f"found cluster for {keyword}")
        cluster = get_cluster(keyword, get_clusters(db))
        respond(
            f"Sucessfully subscribed to {keyword}! That keyword is part of the cluster with the following keywords: {' ,'.join(cluster)}, if you would like to only subscribe to the keyword you entered and not the entire cluster, please type \n!unexpand {keyword}"
        )
    else:
        respond(f"Sucessfully subscribed to {keyword}!")


def on_unsubscribe(db, reddit_username, keyword, respond):
    """
    Called when a user unsubscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user unsubscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    print(f"User {reddit_username} wants to unsubscribe to {keyword}.")
    user = get_user_by_username(db, reddit_username)
    if user == None:
        respond(
            f"User {reddit_username} not found, please subscribe to a keyword with with !sub command"
        )
        return

    print(f"User {reddit_username} found, unsubscribing keyword")
    # check if the user has the keyword
    if not any(keyword in topic["topic_name"] for topic in user["subscribed_keywords"]):
        respond(
            f"User {reddit_username} not subscribed to keyword {keyword}, please subscribe to a keyword with with !sub command"
        )
        return
    remove_keyword_from_user(db, reddit_username, keyword)
    respond(f"Sucessfully unsubscribed to {keyword}!")

    print(f"unsubscribed to {keyword}")


def on_unexpand(db, reddit_username, keyword, respond):
    """
    Called when a user unsubscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user unsubscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    print(f"User {reddit_username} wants to unexpand {keyword}.")
    user = get_user_by_username(db, reddit_username)
    if user == None:
        respond(
            f"User {reddit_username} not found, please subscribe to the keyword with with !sub command"
        )
        return

    print(f"User {reddit_username} found, unexpanding keyword")

    # check if the user has the keyword
    if not any(keyword in topic["topic_name"] for topic in user["subscribed_keywords"]):
        respond(
            f"User {reddit_username} not subscribed to keyword {keyword}, please subscribe to the keyword with with !sub command"
        )
        return

    # check if the keyword is already unexpanded
    if any(
        keyword in topic["topic_name"] and not topic["is_expanded"]
        for topic in user["subscribed_keywords"]
    ):
        respond(f"Keyword {keyword} is already unexpanded")
        return

    unexpand_keyword_for_user(db, reddit_username, keyword)
    respond(f"Sucessfully unexpanded {keyword}!")


def on_list_user_keywords(db, reddit_username, respond):
    """
    Called when a user wants to list their subscribed keywords.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        respond (function): A function that can be called to respond to the user.
    """
    print(f"User {reddit_username} wants to list their subscribed keywords.")
    user = get_user_by_username(db, reddit_username)
    if user == None:
        respond(
            f"User {reddit_username} not found, please subscribe to a keyword with with !sub command"
        )
        return
    # loop through the user's keywords and their expanded status and add to a string
    clusters = get_clusters(db)
    keyword_list = ""
    for topic in user["subscribed_keywords"]:
        keyword_list += (
            f"\ttopic_name: {topic['topic_name']}, is_expanded: {topic['is_expanded']}"
        )
        if topic["is_expanded"]:
            keyword_list += f"expanded keywords: {', '.join(
                get_cluster(topic['topic_name'],clusters )
                )}"
        keyword_list += "\n"
    respond(f"Subscribed keywords list for {reddit_username}: \n{keyword_list}")

def on_visibility_request(db, reddit_username, request):
    """
        Called when a user wants to change their public/private status

        Parameters:
            db (Database): The database object.
            reddit_username: The username of the user
            request: string ["private" or "public"]
        """
    user = get_user_by_username(db, reddit_username)

    if request == "public":
        user.is_public = True
    else:
        user.is_public = False

