from dataclasses import dataclass


@dataclass
class Command:
    command: str
    args: list


def parse_command(message):
    """
    Parses a command from a comment or DM and returns the command and arguments.

    Parameters:
      message (str): The message that the user sent.

    Returns:
       Command: An object containing the command and a list of arguments.
    """

    if not message.startswith("!"):
        return Command(None, [])

    parts = message.split(" ", 1)
    command = parts[0]

    if len(parts) == 1:
        return Command(command, [])

    args = parts[1].split(",")
    args = [arg.strip() for arg in args]

    return Command(command, args)


def is_missing_command(command):
    """
    Checks if a command is missing.

    Parameters:
      command (Command): The command to check.

    Returns:
      bool: True if the command is missing, False otherwise.
    """

    return command.command == None


def is_missing_args(command):
    """
    Checks if a command is missing arguments.

    Parameters:
      command (Command): The command to check.

    Returns:
      bool: True if the command is missing arguments, False otherwise.
    """

    return len(command.args) == 0
