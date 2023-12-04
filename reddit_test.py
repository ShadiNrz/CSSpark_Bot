import re
import os
from dotenv import dotenv_values, load_dotenv
import praw
import time
import threading
import bot_actions

# from command_parser import parse_command
# from connection import staging, prod

### TODO: SET THIS TO PROD BEFORE DEPLOYING
# db = staging
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
        print(comment.body)
        comment.reply("hello world")


if __name__ == "__main__":
    # Start threads for each type of interaction
    comment_thread = threading.Thread(target=comment_stream)
    comment_thread.start()
