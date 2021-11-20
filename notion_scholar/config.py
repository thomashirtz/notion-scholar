import keyring  # https://askubuntu.com/a/881212 Solve issues of keyring with WSL
from pathlib import Path
from typing import Tuple
from typing import Optional
from configparser import ConfigParser
from platformdirs import user_config_dir

from notion_scholar.utilities import NotionScholarError


class ConfigError(NotionScholarError):
    """A config exception class for notion-scholar."""


def add_to_config(section: str, option: str, value: str) -> None:
    directory_path = Path(user_config_dir(appname="notion-scholar"))
    config_path = directory_path.joinpath('config').with_suffix('.ini')

    # Create config folder if not exist
    directory_path.mkdir(parents=True, exist_ok=True)

    # Create config file if not exist
    if not config_path.is_file():
        with open(config_path, 'w') as f:
            pass

    # Get the config file content
    config = ConfigParser()
    config.read(config_path)
    if not config.has_section(section):
        config.add_section(section)

    # Edit the value
    config.set(section, option, value)

    # Save the changes
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def get_token() -> Optional[str]:
    return keyring.get_password("notion-scholar", "token")


def get_config() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    directory_path = Path(user_config_dir(appname="notion-scholar"))
    config_path = directory_path.joinpath('config').with_suffix('.ini')

    if not config_path.is_file():
        database_url = None
        input_file_path = None
        output_file_path = None

    else:
        config = ConfigParser()
        config.read(config_path)
        database_url = config.get('notion', 'database_url', fallback=None)
        input_file_path = config.get('paths', 'input_file_path', fallback=None)
        output_file_path = config.get('paths', 'output_file_path', fallback=None)
    return database_url, input_file_path, output_file_path


def setup(
        token: Optional[str] = None,
        database_url: Optional[str] = None,
        input_file_path: Optional[str] = None,
        output_file_path: Optional[str] = None,
) -> None:
    if token is not None:
        keyring.set_password("notion-scholar", "token", str(token))  # keyring.get_password("notion-scholar", "token")
    if input_file_path is not None and Path(input_file_path).is_file():
        add_to_config('paths', 'input_file_path', str(input_file_path))
    if output_file_path is not None and Path(output_file_path).is_file():
        add_to_config('paths', 'output_file_path', str(output_file_path))
    if database_url is not None:
        add_to_config('notion', 'database_url', str(database_url))


def inspect() -> None:
    directory_path = Path(user_config_dir(appname="notion-scholar"))
    config_path = directory_path.joinpath('config').with_suffix('.ini')
    token = get_token()

    database_url, input_file_path, output_file_path = get_config()
    is_token_saved = not (token is None)

    print(f'\nPath of the config file: {str(config_path)}')
    print(f'database_url: {database_url}')
    print(f'input_file_path: {input_file_path}')
    print(f'output_file_path: {output_file_path}')
    print(f'is_token_saved: {is_token_saved}\n')
