from command_parser import is_missing_args, is_missing_command, parse_command
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

command_list = {
    "!sub": 1,
    "!unsub": 1,
    "!unexpand": 1,
    "!publicme": 0,
    "!privateme": 0,
    "!list": 0,
    "!listexpansions": 0,
    "!testpost": 0,
    "!listusers": 0,
    "!exit": 0,
}


def main():
    def respond(text):
        print(f"BOT RESPONSE: {text}")

    while True:
        input_command = input("Enter a bot command: ")
        command = parse_command(input_command)
        if is_missing_command(command):
            print(
                "Missing command (!sub, !unsub, !unexpand, !publicme, !privateme, !list, !listusers)"
            )
            continue
        if command.command not in command_list:
            print(command.command)
            print("Invalid command")
            continue
        arg_count = command_list[command.command]

        if len(command.args) != arg_count:
            print(
                f"Invalid number of arguments. Expected {arg_count}, got {len(command.args)}"
            )
            continue
        args = command.args
        cmd = command.command
        if cmd == "!exit":
            break
        elif cmd == "!list":
            data = get_users(staging, aggregate=False)
            for user in data:
                print(user.reddit_username)
                print(
                    f"Public: {user.is_public}, Subscribed keywords: {user.subscribed_keywords}"
                )
        elif cmd == "!listexpansions":
            data = get_users(staging, aggregate=True)
            for user in data:
                print(user.reddit_username)
                print(
                    f"Public: {user.is_public}, expanded keywords: {user.expanded_subscriptions}"
                )
        elif cmd == "!testpost":
            text = input("Enter reddit post text ")
            test_reddit_post(staging, text, respond)
        elif cmd == "!sub":
            username = input("Enter username ")
            keyword = args[0]
            on_subscribe(staging, username, keyword, respond)
        elif cmd == "!unsub":
            username = input("Enter username ")
            keyword = args[0]
            on_unsubscribe(staging, username, keyword, respond)
        elif cmd == "!unexpand":
            username = input("Enter username ")
            keyword = args[0]
            on_unexpand(staging, username, keyword, respond)
        elif cmd == "!publicme":
            username = input("Enter username ")
            on_publicme(staging, username, respond)
        elif cmd == "!privateme":
            username = input("Enter username ")
            on_privateme(staging, username, respond)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
