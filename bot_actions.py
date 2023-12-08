from bot_actions_helpers import get_or_create_user, is_user_subscribed_to_keyword
from connection import (
    add_keyword_to_user,
    get_clusters,
    get_ping_limit,
    get_user_by_username,
    get_users,
    create_user,
    remove_keyword_from_user,
    set_ping_limit,
    set_user_is_public,
    unexpand_keyword_for_user,
)
from util import get_cluster, get_user_keyword_counts

i_am_a_bot = """I am a bot and this action was performed automatically. Please check my profile to see the full list of commands available."""
no_user_str = f"User not found, please subscribe to a keyword with with !sub command to join my userbase\n\n{i_am_a_bot}"


def test_reddit_post(db, text, respond):
    """
    Tests getting the users to ping
    """
    # Get all users from the database
    users = get_users(db, True)
    MAX_PINGS = get_ping_limit(db)
    filtered_users = get_user_keyword_counts(users, text)
    print(filtered_users)
    top_users = sorted(filtered_users, key=filtered_users.get, reverse=True)[:MAX_PINGS]
    top_users_str = ", ".join([f"u/{user}" for user in top_users])
    if len(top_users) == 0:
        # no response if no users are found
        return
    respond(
        f"Beep boop, I spy a keyphrase of interest to r/CompSocial community members: {top_users_str}\n\nPlease join the converstation and tell us what you think!\n\n{i_am_a_bot}\n\nFeel free to contact the mod team if you notice any issues with my behavior."
    )


def on_ping_limit(db, limit, respond):
    """
    Called when a user wants to change the ping limit

    Parameters:
        db (Database): The database object.
        limit(int): The new ping limit
        respond (function): A function that can be called to respond to the user.
    """
    set_ping_limit(db, limit)
    respond(f"Successfully set ping limit to {limit}\n\n{i_am_a_bot}")


def on_get_ping_limit(db, respond):
    """
    Called when a user wants to get the ping limit

    Parameters:
        db (Database): The database object.
        respond (function): A function that can be called to respond to the user.
    """
    limit = get_ping_limit(db)
    respond(f"The current ping limit is {limit}\n\n{i_am_a_bot}")


def on_remove(db, reddit_username, respond):
    """
    Called when a user wants to be removed from the database

    Parameters:
        db (Database): The database object.
        reddit_username: The username of the user
        respond (function): A function that can be called to respond to the user.
    """
    user = get_user_by_username(db, reddit_username)
    if user == None:
        respond(no_user_str)
        return
    db.users.delete_one({"reddit_username": reddit_username})
    respond(
        f"User {reddit_username} has been removed from the database\n\n{i_am_a_bot}"
    )


def on_reddit_post(db, submission, reddit):
    """
    Called when a new Reddit post is detected.

    Parameters:
        db (Database): The database object.
        submission (Submission): The Reddit post object.
    """
    MAX_PINGS = get_ping_limit(db)
    title = submission.title.upper()
    post_text = submission.selftext.upper()

    # Get all users from the database
    users = get_users(db, True)

    public_users = []
    private_users = []

    # sort users based on privacy status
    for user in users:
        if user.is_public:
            public_users.append(user)
        else:
            private_users.append(user)

    public_filtered_users = get_user_keyword_counts(
        public_users, f"{title} {post_text}"
    )
    private_filtered_users = get_user_keyword_counts(
        private_users, f"{title} {post_text}"
    )
    top_public_users = sorted(
        public_filtered_users, key=public_filtered_users.get, reverse=True
    )[:MAX_PINGS]
    top_private_users = sorted(
        private_filtered_users, key=private_filtered_users.get, reverse=True
    )[:MAX_PINGS]

    top_public_users_str = ", ".join([f"u/{user}" for user in top_public_users])

    if len(top_public_users) != 0:
        submission.reply(
            f"Beep boop, I spy a keyphrase of interest to r/CompSocial community members: {top_public_users_str}\n\nPlease join the converstation and tell us what you think!\n\n{i_am_a_bot}"
        )
    if len(top_public_users) > 3:
        top_private_users = top_private_users + top_public_users

    for user in top_private_users:
        print(f"messaging {user}")
        try:
            post_url = submission.shortlink
            reddit.redditor(user).message(
                f"Keyword Mentioned",
                f"{post_url} ({title}) mentions your keyphrase\n\nGo check out this post and see what you think!\n\n{i_am_a_bot}",
            )
            print(
                "BOT_DM"
                + f"{post_url} ({title}) mentions your keyphrase\n\nGo check out this post and see what you think!\n\n{i_am_a_bot}",
            )
        except Exception as e:
            print(f"Failed to message {user}: {e}")

    print(f"Replied to submission {submission.id}: {title}")
    print(f"Sent messages to private users in reply to {submission.id}: {title}")


def on_subscribe(db, reddit_username, keyword, respond):
    """
    Called when a user subscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user subscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    keyword = keyword.lower()
    print(f"User {reddit_username} subscribed to keyword {keyword}.")
    user = get_or_create_user(db, reddit_username)
    if is_user_subscribed_to_keyword(user, keyword):
        respond(f"You are already subscribed to {keyword}.\n\n{i_am_a_bot}")
        return
    add_keyword_to_user(db, reddit_username, keyword)
    # check if keyword is part of a cluster
    db_clusters = get_clusters(db)
    cluster = get_cluster(keyword, db_clusters)
    if cluster:
        respond(
            f"Successfully subscribed to {keyword}! That keyword is part of a cluster with the following keywords: \n\n>{', '.join(cluster)}\n\n if you would like to only subscribe to the keyword you entered and not the entire cluster, please respond with \n\n!unexpand {keyword}\n\n{i_am_a_bot}"
        )
    else:
        respond(f"Successfully subscribed to {keyword}!\n\n{i_am_a_bot}")
        unexpand_keyword_for_user(db, reddit_username, keyword)


def on_unsubscribe(db, reddit_username, keyword, respond):
    """
    Called when a user unsubscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user unsubscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    keyword = keyword.lower()
    user = get_user_by_username(db, reddit_username)
    if not user:
        respond(no_user_str)

    # check if the user has the keyword
    if not is_user_subscribed_to_keyword(user, keyword):
        respond(
            f"You are not subscribed to {keyword},respond with !listkeywords to see your subscriptions.\n\n{i_am_a_bot}"
        )
        return
    remove_keyword_from_user(db, reddit_username, keyword)
    respond(f"Successfully unsubscribed to {keyword}!\n\n{i_am_a_bot}")


def on_unexpand(db, reddit_username, keyword, respond):
    """
    Called when a user unsubscribes to a keyword.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        keyword (str): The keyword that the user unsubscribed to.
        respond (function): A function that can be called to respond to the user.
    """
    keyword = keyword.lower()
    user = get_user_by_username(db, reddit_username)
    if not user:
        respond(no_user_str)

    # check if the keyword is already unexpanded
    if any(
        keyword in topic["topic_name"] and not topic["is_expanded"]
        for topic in user["subscribed_keywords"]
    ):
        respond(f"Keyword {keyword} is already unexpanded")
        return

    unexpand_keyword_for_user(db, reddit_username, keyword)
    respond(f"Successfully unexpanded {keyword}!\n\n{i_am_a_bot}")


def on_list_user_keywords(db, reddit_username, respond):
    """
    Called when a user wants to list their subscribed keywords.

    Parameters:
        db (Database): The database object.
        user (User): The user object.
        respond (function): A function that can be called to respond to the user.
    """
    user = get_user_by_username(db, reddit_username)
    if not user:
        respond(no_user_str)
    # loop through the user's keywords and their expanded status and add to a string
    clusters = get_clusters(db)
    keyword_list = ""
    for topic in user["subscribed_keywords"]:
        keyword_list += (
            f"\ttopic_name: {topic['topic_name']}, is_expanded: {topic['is_expanded']}"
        )
        if topic["is_expanded"]:
            if get_cluster(topic["topic_name"], clusters):
                keyword_list += f", expanded keywords: {', '.join(get_cluster(topic['topic_name'], clusters ))}"
            else:
                keyword_list += f", no expanded keywords"
        keyword_list += "\n\n"
    respond(
        f"Subscribed keywords list for {reddit_username}: \n\n{keyword_list}\n\n{i_am_a_bot}"
    )


def on_publicme(db, reddit_username, respond):
    """
    Called when a user wants to change their public/private status

    Parameters:
        db (Database): The database object.
        reddit_username: The username of the user
        respond (function): A function that can be called to respond to the user.
    """
    user = get_user_by_username(db, reddit_username)
    if user is None:
        respond(no_user_str)
        return
    if user["is_public"]:
        respond(f"User {reddit_username} is already public\n\n{i_am_a_bot}")
        return
    set_user_is_public(db, reddit_username, True)
    respond(f"User {reddit_username} is now public\n\n{i_am_a_bot}")


def on_privateme(db, reddit_username, respond):
    """
    Called when a user wants to change their public/private status

    Parameters:
        db (Database): The database object.
        reddit_username: The username of the user
        respond (function): A function that can be called to respond to the user.
    """
    user = get_user_by_username(db, reddit_username)
    if user == None:
        respond(no_user_str)
        return
    if not user["is_public"]:
        respond(f"User {reddit_username} is already private\n\n{i_am_a_bot}")
        return
    set_user_is_public(db, reddit_username, False)
    respond(f"User {reddit_username} is now private\n\n{i_am_a_bot}")
