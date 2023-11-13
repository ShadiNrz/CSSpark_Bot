import re
import praw
import time
import threading

reddit = praw.Reddit(
    client_id="zRFmLVVtIrtotSAiwLQU0Q",
    client_secret="KQQgQEj87V7t4u4Ob9FYTscq1BdL6w",
    user_agent="Kerbal_Bot",
    username="Kerbal_Bot",
    password="pVzNkPER9JmFYAf",  # TODO: Change bot username and remove password from code
)

subreddit = reddit.subreddit("bot_playground")  # TODO: move to env file

# Keyword to look for in comments
comment_keyword = "!hello"

# TEMPORARY STORAGE FOR SUBSCRIPTIONS AND USERNAMES
subscription_dict = {}
public_users = []


def keywordFormatting(body, operation):
    # seperate keywords by commas
    operation = operation + " "
    keywords = body.replace(operation, "").split(", ")

    # force keywords into lower case
    keywords = [k.lower() for k in keywords]

    keywords_string = ""
    for word in keywords:
        keywords_string = keywords_string + ", " + word
    keywords_string = keywords_string.split(",")[1:]
    keywords_string = ", ".join(keywords_string)

    return keywords, keywords_string


#def handle_comment(comment):
    #if comment_keyword in comment.body:
        #try:
            #reply_text = f"Hii {comment.author.name}"
            #comment.reply(reply_text)
            # comment.author.message('Hello', 'How are you?') #TODO: Replace with whatever Rhett did
            #print(f"Replied to comment from {comment.author.name}")
        #except Exception as e:
            #print(str(e))
            #time.sleep(10)


#def comment_stream():
    #for comment in subreddit.stream.comments(skip_existing=True):
        #handle_comment(comment)


def handle_submission(submission):
    try:
        title_upper = submission.title.upper()
        self_text_upper = submission.selftext.upper()
        reply_text = f"Title: {title_upper}\n\nContent: {self_text_upper}"
        submission.reply(reply_text)
        print(f"Replied to submission {submission.id}")
    except Exception as e:
        print(str(e))
        time.sleep(10)


def submission_stream():
    for submission in subreddit.stream.submissions(skip_existing=True):
        handle_submission(submission)


# Handle DMs
def handle_dm(message):
    if message.was_comment:

        return  # Skip if this was a comment reply

    try:

        message.mark_read()  # Mark message as read when fetching it

        author = message.author  # Reddit "user" object - author of sent message

        if message.subject == "Bot Command":  # check if message subject is "Bot Command"

            if "!sub" in message.body:  # sub command passed - add new keyword subscription for user
                keywords, keywords_string = keywordFormatting(message.body, "!sub")  # Format keywords in message

                if author not in subscription_dict:  # add author and keywords to the author's subscriptions
                    subscription_dict[author] = keywords

                else:  # add new keywords to existing author's subscriptions

                    for word in keywords:

                        if word not in subscription_dict[author]:
                            subscription_dict[author].append(word)

                # send confirmation message in reply
                message.reply("*Beep Boop* \n\nYou are now subscribed to keyword(s)" + keywords_string)

            elif "!unsub" in message.body:  # Remove keywords from a user's subscription list
                keywords, keywords_string = keywordFormatting(message.body, "!unsub")  # Format keywords in message

                if author in subscription_dict:  # remove keywords from user's subscription list

                    for keyword in keywords:

                        if keyword in subscription_dict[author]:
                            subscription_dict[author].remove(keyword)

                # Reply to author of message affirming unsubscription
                message.reply("*Beep Boop* \n\nYou are now unsubscribed from keyword(s)" + keywords_string)

            elif "!publicme" in message.body:  # Make users public on request

                if author not in public_users:
                    public_users.append(author)

                # Have the bot reply to the comment confirming privacy setting changed
                message.reply("*Beep Boop* \n\nYour profile is now public.")

            elif "!privateme" in message.body:  # Make users private on request

                if author in public_users:
                    public_users.remove(author)

                # Have the bot reply to the comment confirming privacy setting changed
                message.reply("*Beep Boop* \n\nYour profile is now private.")

            # DO WE REMOVE THIS?
            ############
            elif "!findusers" in message.body:  # list users who are subscribed to a certain keyword
                ###########

                # Format keywords in message
                keywords, keywords_string = keywordFormatting(message.body, "!findusers")

                users_per_keyword = {}
                for word in keywords:
                    users_per_keyword[word] = []

                    for user in subscription_dict:

                        if user in public_users and word in subscription_dict[user]:
                            users_per_keyword[word].append(user.name)

                # Have the bot reply to the command with found usernames
                if str(users_per_keyword) != '[]':
                    message.reply("*Beep Boop* \n\nThese are the users I found:\n\n" + str(users_per_keyword))

                else:
                    message.reply("*Beep Boop* \n\nI found no users!")

    except Exception as e:
        print(str(e))
        time.sleep(10)


# Main function for DM stream
def dm_stream():
    for message in reddit.inbox.stream(skip_existing=True):
        handle_dm(message)


if __name__ == "__main__":
    # Start threads for each type of interaction
    comment_thread = threading.Thread(target=comment_stream)
    submission_thread = threading.Thread(target=submission_stream)
    dm_thread = threading.Thread(target=dm_stream)

    comment_thread.start()
    submission_thread.start()
    dm_thread.start()
