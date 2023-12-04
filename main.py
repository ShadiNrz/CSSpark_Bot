import re
import os
from dotenv import dotenv_values, load_dotenv
import praw
import time
import threading
import bot_actions
from command_parser import parse_command
from connection import staging, prod

### TODO: SET THIS TO PROD BEFORE DEPLOYING
db = staging
load_dotenv()
config = dotenv_values(".env")

# reddit = praw.Reddit(
#     client_id="zRFmLVVtIrtotSAiwLQU0Q",
#     client_secret="KQQgQEj87V7t4u4Ob9FYTscq1BdL6w",
#     user_agent="Kerbal_Bot",
#     username="Kerbal_Bot",
#     password="pVzNkPER9JmFYAf",
# )
reddit = praw.Reddit(
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
    user_agent="CSSpark_Bot",
    username=os.environ["username"],
    password=os.environ["password"],
)


subreddit = reddit.subreddit("bot_playground")  # TODO: move to env file


def comment_stream():
    for comment in subreddit.stream.comments(skip_existing=True):
        handle_command(comment)


def handle_submission(submission):
    try:
        bot_actions.on_reddit_post(db, submission, reddit)

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

        isDM = message_check(message)
        # string indicating type of message - checks for correct DM format
        if isDM == "Error":
            return

        def respond(text):  # embedded function - sends a string reply to bot command
            print(f"BOT_RESPONSE: {text}")
            message.reply(text)

        command = parse_command(message.body)
        cmd, args = command.command, command.args
        if cmd == "!sub":
            # todo possibly support multiple comma separated keywords
            if len(args) == 0:
                respond(
                    "No keyword specified, you can subscribe to a keyword using !sub keyword"
                )
                return
            bot_actions.on_subscribe(db, author.name, args[0], respond)
        elif cmd == "!unsub":
            if len(args) == 0:
                respond(
                    "No keyword specified, you can unsubscribe to a keyword using !unsub keyword"
                )
                return
            # Remove keywords from a user's subscription list
            bot_actions.on_unsubscribe(db, author.name, args[0], respond)
        # TODO: fix !list command - error message - can only join an iterable
        elif (
            cmd == "!list" or cmd == "!listkeywords"
        ):  # User asks for keywords they are subscribed to
            bot_actions.on_list_user_keywords(db, author.name, respond)
        elif cmd == "!publicme":  # Make users public on request
            bot_actions.on_publicme(db, author.name, respond)
        elif cmd == "!privateme":  # Make users private on request
            bot_actions.on_privateme(db, author.name, respond)

        # TODO: figure out if we want to keep this
        # elif cmd == "!findusers":  # list users who are subscribed to a certain keyword

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
