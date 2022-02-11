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
