import shutil
import warnings
from configparser import ConfigParser
from pathlib import Path
from typing import Optional
from typing import Dict

import keyring
from platformdirs import user_config_dir

from notion_scholar.utilities import NotionScholarException, coerce_to_absolute_path, get_token


class ConfigException(NotionScholarException):
    """A config exception class for notion-scholar."""


class ConfigManager:
    """Class that manages all the notion-scholar configuration."""
    def __init__(
            self,
            token: Optional[str] = None,
            string: Optional[str] = None,
            file_path: Optional[str] = None,
            database_id: Optional[str] = None,
    ):
        self.token = token
        self.string = string
        self.file_path = file_path
        self.database_id = database_id

        directory_path = Path(user_config_dir(appname='notion-scholar'))
        self.config_path = directory_path.joinpath('config').with_suffix('.ini')

    def get_download_kwargs(self) -> dict:
        return {
            'file_path': coerce_to_absolute_path(path=self.file_path),
            **self._get_sanitized_kwargs()
        }

    def get_run_kwargs(self) -> dict:
        config = self.get()

        file_path = self.file_path
        if file_path is not None:
            file_path = coerce_to_absolute_path(path=file_path)

            if not Path(file_path).exists():
                raise ConfigException("The file_path provided to the argparse does not exist.")
        elif self.string is None:
            file_path = config.get('file_path', None)
            if file_path is None:
                raise ConfigException("No file_path or bib string provided and no file path set in the config.")
            if not Path(file_path).exists():
                raise ConfigException("No file_path or bib string provided and the file_path set in the config does not exist.")

        return {
            'bib_string': self.string,
            'bib_file_path': file_path,
            **self._get_sanitized_kwargs()
        }

    def _get_sanitized_kwargs(self):
        config = self.get()

        token = self.token
        if token is None:
            token = get_token()

            if token is None:
                raise ConfigException('The Notion token is not set nor saved.')

        database_id = self.database_id
        if database_id is None:
            database_id = config.get('database_id', None)

            if database_id is None:
                raise ConfigException('The database_id is not set nor saved.')

        return {
            'token': token,
            'database_id': database_id,
        }

    def setup(self) -> None:
        # Save the token if provided
        if self.token is not None:
            keyring.set_password('notion-scholar', 'token', self.token)

        # Void the file_path argument if the file doesn't exist
        if self.file_path is not None:
            self.file_path = coerce_to_absolute_path(path=self.file_path, warn=True)

            if not Path(self.file_path).exists():
                warnings.warn(
                    f'The file "{self.file_path}" does not exist, it will not be added to the config file.',  # noqa 501
                )
                self.file_path = None

        # Create config folder if not exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Create config file if not exist
        if not self.config_path.is_file():
            with open(self.config_path, 'w'):
                pass

        # Get the config file content
        config = ConfigParser()
        config.read(self.config_path)

        # Setup the section
        if not config.has_section('Settings'):
            config.add_section('Settings')

        # Write the values
        key_to_value = {
            "database_id": self.database_id,
            "file_path": self.file_path,
        }

        for key, value in key_to_value.items():
            if value is not None:
                config.set(section='Settings', option=key, value=value)

        # Save the changes
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def inspect(self) -> None:
        print(f'\nconfig_file_path: {str(self.config_path)}')
        print(f'config_file_exist: {self.config_path.exists()}\n')
        print(f'token: {get_token()}')

        config = self.get()
        for key, value in config.items():
            print(f'{key}: {value}')

    def get(self) -> Dict[str, str]:
        if not self.config_path.is_file(): # todo check if is a file and exist + right section
            return {}
        else:
            config = ConfigParser()
            config.read(self.config_path)
            try:
                return dict(config['Settings'])
            except KeyError:
                warnings.warn(
                    'The notion scholar seems to have the old config structure. '
                    'A function will be executed in order to update the config. '
                    'If some problems arise in the future, please run `ns clear-config`'
                )
                return self._update_config()

    def clear(self) -> None:
        shutil.rmtree(self.config_path.parent, ignore_errors=True)
        keyring.delete_password('notion-scholar', 'token')

    def _update_config(self):
        """To seamlessly upgrade from notion-scholar 0.2.0 to 0.3.0"""
        config = ConfigParser()
        config.read(self.config_path)
        config.add_section('Settings')

        dct = {
            ('paths', 'bib_file_path'): 'file_path',
            ('notion_api', 'database_id'): 'database_id'
        }
        for (old_section, old_option), new_option in dct.items():
            try:
                path = config[old_section][old_option]
                config.set(section='Settings', option=new_option, value=path)
                config.remove_section(old_section)
            except KeyError:
                pass

        try:
            config.remove_section('preferences')
        except KeyError:
            pass

        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

        return dict(config['Settings'])
