from collections import Counter


class NotionScholarError(Exception):
    """A base class for notion-scholar exceptions."""


def append_string_to_file(file_path: str, content: str) -> None:
    """Append content to a file.

    Args:
        file_path: path of the file that will be appended to.
        content: content that will be appended.
    """
    with open(file_path, 'a') as f:
        f.write('\n')
        f.write(content)


def get_duplicates(lst: list) -> list:
    """Get duplicates from a list.

    Args:
        lst: list that will be inspected.

    Returns:
        List of duplicates from the list.
    """
    return [k for k, v in Counter(lst).items() if v > 1]


def write_to_file(file_path: str, content: str) -> None:
    """Write content to a file.

    Args:
        file_path: path of the file that will be written to.
        content: content that will be written.
    """
    with open(file_path, 'w') as f:
        f.write(content)


def fallback(choice_1, choice_2):
    """Fallback function to use choice_2 if choice_1 is None"""
    return choice_1 if choice_1 is not None else choice_2
