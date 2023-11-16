import re
import praw
import time
import threading
import bot_actions
from connection import staging

reddit = praw.Reddit(
    client_id="zRFmLVVtIrtotSAiwLQU0Q",
    client_secret="KQQgQEj87V7t4u4Ob9FYTscq1BdL6w",
    user_agent="Kerbal_Bot",
    username="Kerbal_Bot",
    password="pVzNkPER9JmFYAf",  # TODO: Change bot username and remove password from code
)

# TODO: get new client id and secret - new bot credentials below
# Username: CSSpark_Bot
# Password:Botbros7760321?

subreddit = reddit.subreddit("bot_playground")  # TODO: move to env file

# Keyword to look for in comments
comment_keyword = "!hello"


def comment_stream():
    for comment in subreddit.stream.comments(skip_existing=True):
        handle_command(comment)


def handle_submission(submission):
    try:
        bot_actions.on_reddit_post(staging, submission)

    except Exception as e:
        print(str(e))
        time.sleep(10)


def submission_stream():
    for submission in subreddit.stream.submissions(skip_existing=True):
        handle_submission(submission)


def message_check(message):
    try:  # try to get subject of message if it is a DM - check if subject is Bot Command
        if message.subject.lower() == "bot command":
            message.mark_read()  # Mark message as read when fetching it
            return "DM"
        else:
            return "Error"

    except:
        return "Comment"


# Handle DMs or Comments
def handle_command(message):
    try:
        author = message.author  # Reddit "user" object - author of sent message

        isDM = message_check(
            message
        )  # string indicating type of message - checks for correct DM format

        if isDM == "Error":
            return

        ##############################################################################

        def respond(text):  # embedded function - sends a string reply to bot command
            message.reply(text)
            return

        ##############################################################################

        if "!sub" in message.body:
            bot_actions.on_subscribe(staging, author.username, respond())

        elif (
            "!unsub" in message.body
        ):  # Remove keywords from a user's subscription list
            bot_actions.on_unsubscribe(staging, author.username, respond())

        elif "!list" in message.body:  # User asks for keywords they are subscribed to
            bot_actions.on_list_user_keywords(staging, author.username, respond())

        elif "!publicme" in message.body:  # Make users public on request
            bot_actions.on_visibility_request(staging, author.username, "public")

        elif "!privateme" in message.body:  # Make users private on request
            bot_actions.on_visibility_request(staging, author.username, "private")

        # elif "!findusers" in message.body:  # list users who are subscribed to a certain keyword

    except Exception as e:
        print(str(e))
        time.sleep(10)


# Main function for DM stream
def dm_stream():
    for message in reddit.inbox.stream(skip_existing=True):
        handle_command(message)


if __name__ == "__main__":
    # Start threads for each type of interaction
    comment_thread = threading.Thread(target=comment_stream)
    submission_thread = threading.Thread(target=submission_stream)
    dm_thread = threading.Thread(target=dm_stream)

    comment_thread.start()
    submission_thread.start()
    dm_thread.start()
