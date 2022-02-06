import shutil
import warnings
from configparser import ConfigParser
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import keyring  # https://askubuntu.com/a/881212 Solve issues of keyring w/ WSL
from platformdirs import user_config_dir

from notion_scholar.utilities import NotionScholarError


class ConfigError(NotionScholarError):
    """A config exception class for notion-scholar."""


def get_token() -> Optional[str]:
    return keyring.get_password('notion-scholar', 'token')


def add_to_config(section_option_value_list: List[Tuple[str, str, Any]]) -> None:  # noqa 501
    directory_path = Path(user_config_dir(appname='notion-scholar'))
    config_path = directory_path.joinpath('config').with_suffix('.ini')

    # Create config folder if not exist
    directory_path.mkdir(parents=True, exist_ok=True)

    # Create config file if not exist
    if not config_path.is_file():
        with open(config_path, 'w'):
            pass

    # Get the config file content
    config = ConfigParser()
    config.read(config_path)

    # Edit the value & add section if doesn't exist
    for section, option, value in section_option_value_list:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)

    # Save the changes
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def get_config() -> Dict[str, Any]:
    directory_path = Path(user_config_dir(appname='notion-scholar'))
    config_path = directory_path.joinpath('config').with_suffix('.ini')

    if not config_path.is_file():
        return {}

    else:
        config = ConfigParser()
        config.read(config_path)

        dct = {}
        for section in config.sections():
            dct.update(dict(config[section]))
        return dct


def setup(
        token: Optional[str],
        database_id: Optional[str],
        bib_file_path: Optional[str],
        save: Optional[bool],
) -> None:
    if token is not None:
        keyring.set_password('notion-scholar', 'token', token)

    section_option_list = []
    if bib_file_path is not None:
        if Path(bib_file_path).is_file():
            section_option_list.append(
                ('paths', 'bib_file_path', bib_file_path),
            )
        else:
            warnings.warn(
                f'The file "{bib_file_path}" does not exist, it will not be added to the config file.',  # noqa 501
            )
    if database_id is not None:
        section_option_list.append(('notion_api', 'database_id', database_id))
    if save is not None:
        section_option_list.append(
            ('preferences', 'save_to_bib_file', str(save)),
        )
    add_to_config(section_option_list)


def inspect() -> None:
    directory_path = Path(user_config_dir(appname='notion-scholar'))
    config_path = directory_path.joinpath('config').with_suffix('.ini')
    token = get_token()

    print(f'\nconfig_file_path: {str(config_path)}')
    print(f'config_file_exist: {config_path.exists()}')
    print(f'token: {token}')

    config = get_config()
    for key, value in config.items():
        if key in ['database_id', 'save_to_bib_file', 'bib_file_path']:
            print(f'{key}: {value}')
    print()


def clear() -> None:
    directory_path = Path(user_config_dir(appname='notion-scholar'))
    shutil.rmtree(directory_path, ignore_errors=True)
    keyring.delete_password('notion-scholar', 'token')
