from collections import Counter


class NotionScholarError(Exception):
    """A base class for notion-scholar exceptions."""


def append_string_to_file(file_path: str, content: str) -> None:
    with open(file_path, 'a') as f:
        f.write('\n')
        f.write(content)


def get_duplicates(lst: list) -> list:
    return [k for k, v in Counter(lst).items() if v > 1]


def write_to_file(file_path: str, content: str):
    with open(file_path, 'w') as f:
        f.write(content)
