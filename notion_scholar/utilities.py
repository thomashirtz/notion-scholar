import warnings
from pathlib import Path
from typing import Optional

import keyring


class NotionScholarException(Exception):
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


def write_to_file(file_path: str, content: str) -> None:
    """Write content to a file.

    Args:
        file_path: path of the file that will be written to.
        content: content that will be written.
    """
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(content)


def get_token() -> Optional[str]: # Add returns
    """Retrieve the Notion API token stored with keyring.

    Returns:
        A string containing the token or `None` if the token does not exist.
    """
    return keyring.get_password('notion-scholar', 'token')


def coerce_to_absolute_path(path: str, warn: bool = False) -> str:
    """Coerce the input path to an absolute path.

    Args:
        path: Path needed to be coerced.
        warn: Boolean indicating whether to warn the user if the path is coerced.

    Returns:

    """
    p = Path(path)
    if not p.is_absolute():
        if warn:
            warnings.warn(
                f'The path "{p}" is absolute, the path used is therefore "{Path.cwd().joinpath(p)}".',
            )
        return str(Path.cwd().joinpath(p))
    else:
        return str(p)