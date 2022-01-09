from collections import Counter


class NotionScholarError(Exception):
    """A base class for notion-scholar exceptions."""


def append_string_to_file(string: str, file_path: str) -> None:
    with open(file_path, 'a') as f:
        f.write('\n')
        f.write(string)


def get_duplicates(lst: list):
    return [k for k, v in Counter(lst).items() if v > 1]
