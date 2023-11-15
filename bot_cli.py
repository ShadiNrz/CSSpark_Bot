from connection import get_users, staging
from bot_actions import (
    on_reddit_post,
    on_subscribe,
    on_unsubscribe,
    on_unexpand,
    test_reddit_post,
    on_privateme,
    on_publicme,
)


def main():
    def respond(text):
        print(f"BOT RESPONSE: {text}")

    while True:
        input_command = input("Enter a bot command: ")
        if input_command == "exit":
            break
        elif input_command == "ls":
            data = get_users(staging, aggregate=False)
            for user in data:
                print(user.reddit_username)
                print(
                    f"Public: {user.is_public}, Subscribed keywords: {user.subscribed_keywords}"
                )
        elif input_command == "ls -e":
            data = get_users(staging, aggregate=True)
            for user in data:
                print(user.reddit_username)
                print(
                    f"Public: {user.is_public}, expanded keywords: {user.expanded_subscriptions}"
                )
        elif input_command == "reddit_post":
            text = input("Enter reddit post text ")
            test_reddit_post(staging, text, respond)
        elif input_command == "!sub":
            username = input("Enter username ")
            keyword = input("Enter keyword ")
            on_subscribe(staging, username, keyword, respond)
        elif input_command == "!unsub":
            username = input("Enter username ")
            keyword = input("Enter keyword ")
            on_unsubscribe(staging, username, keyword, respond)
        elif input_command == "!unexpand":
            username = input("Enter username ")
            keyword = input("Enter keyword ")
            on_unexpand(staging, username, keyword, respond)
        elif input_command == "!publicme":
            username = input("Enter username ")
            on_publicme(staging, username, respond)
        elif input_command == "!privateme":
            username = input("Enter username ")
            on_privateme(staging, username, respond)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
