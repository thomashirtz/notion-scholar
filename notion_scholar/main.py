import sys
import argparse
from pathlib import Path, PurePath
from distutils.util import strtobool

from notion_scholar.run import run
from notion_scholar.download import download
from notion_scholar.utilities import fallback

from notion_scholar.config import clear
from notion_scholar.config import setup
from notion_scholar.config import inspect
from notion_scholar.config import get_token
from notion_scholar.config import get_config
from notion_scholar.config import ConfigException


def get_parser():
    token = get_token()
    config = get_config()

    parser = argparse.ArgumentParser(
        description='notion-scholar',
        usage='Use "notion-scholar --help" or "ns --help" for more information',  # noqa: E501
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Parent parser
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Choice of the subparser
    subparsers = parser.add_subparsers(
        help='Selection of the action', dest='mode',
    )

    # Run parser
    run_parser = subparsers.add_parser(
        'run', parents=[parent_parser],
        help='Run notion-scholar.',
    )
    run_parser.add_argument(
        '-t', '--token',
        default=None, type=str, metavar='', required=token is None,
        help=f'Token used to connect to Notion. \n(default: {token})',
    )
    run_parser.add_argument(
        '-db', '--database-id',
        default=None, type=str, metavar='',
        help=f'Database that will be furnished. The database_id can be found in the url of the database: \nhttps://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n(default: {config.get("database_id", None)})',  # noqa: E501
    )

    if config.get('bib_file_path', None) is None:
        group = run_parser.add_mutually_exclusive_group(required=True)
    else:
        group = run_parser.add_argument_group()
    group.add_argument(
        '-f', '--bib-file-path',
        default=None, type=str, metavar='',
        help=f'Bib file that will be used. This argument is required if the bib file is not saved in the config and no bib-string is passed. \n(default: {config.get("bib_file_path", None)})',  # noqa: E501
    )
    group.add_argument(
        '-s', '--bib-string',
        default=None, type=str, metavar='',
        help='Bibtex entries to add (must be in-between three quotes \"\"\"<bib-string>\"\"\"). By default, the entries will be saved to the bib file from the config. It is possible to disable this behavior by changing the "save" option: "ns setup -save false".',  # noqa: E501
    )

    # Download bibtex parser
    download_parser = subparsers.add_parser(
        'download', parents=[parent_parser],
        help='Download the bibtex entries present in the database.',
    )
    download_parser.add_argument(
        '-f', '--file-path',
        default=None, type=str, metavar='', required=True,
        help='File in which the bibtex entries will be saved',
    )
    download_parser.add_argument(  # todo group w/ run function
        '-t', '--token',
        default=None, type=str, metavar='', required=token is None,
        help=f'Token used to connect to Notion. \n(default: {token})',
    )
    download_parser.add_argument(  # todo group w/ run function
        '-db', '--database-id',
        default=None, type=str, metavar='',
        help=f'Database that will be furnished. The database_id can be found in the url of the database: \nhttps://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n(default: {config.get("database_id", None)})',  # noqa: E501
    )

    # Clear config parser
    clear_parser = subparsers.add_parser(  # noqa: F841
        'clear-config', parents=[parent_parser],
        help='Clear the notion-scholar config.',
    )

    # Inspect config parser
    inspect_parser = subparsers.add_parser(  # noqa: F841
        'inspect-config', parents=[parent_parser],
        help='Inspect the notion-scholar config.',
    )

    # Setup parser
    setup_parser = subparsers.add_parser(
        'set-config', parents=[parent_parser],
        help='Save the default values of notion-scholar.',
    )
    setup_parser.add_argument(
        '-f', '--bib-file-path',
        default=None, type=str, metavar='',
        help=f'Save the input file path in the user config using "platformdirs". The path must be absolute and the file need to exist. (current: {config.get("bib_file_path", None)})',  # noqa: E501
    )
    setup_parser.add_argument(
        '-s', '--save',
        default=None, type=lambda x: bool(strtobool(x)), metavar='',
        help=f'Set whether the entries from "bib-string" will be saved in the bib file. (current: {config.get("save_to_bib_file", True)})',  # noqa: E501
    )
    setup_parser.add_argument(
        '-t', '--token',
        default=None, type=str, metavar='',
        help=f'Save the Notion token using "keyring". \n(current: {token})',
    )
    setup_parser.add_argument(
        '-db', '--database-id',
        default=None, type=str, metavar='',
        help=f'Save the database-id in the user config using the library "platformdirs". The database_id can be found in the url of the database: \nhttps://www.notion.so/{{workspace_name}}/{{database_id}}?v={{view_id}} \n(current: {config.get("database_id", None)})',  # noqa: E501
    )

    return parser


def sanitize_arguments(**kwargs):
    config = get_config()

    if 'token' in kwargs:
        kwargs['token'] = fallback(kwargs['token'], get_token())
        if kwargs['token'] is None:
            raise ConfigException('The Notion token is not set nor saved.')

    if 'database_id' in kwargs:
        kwargs['database_id'] = fallback(kwargs['database_id'], config.get('database_id', None))  # noqa: E501
        if kwargs['database_id'] is None:
            raise ConfigException('The database_id is not set nor saved.')

    if 'bib_file_path' in kwargs:
        if kwargs['bib_file_path'] is not None and not Path(kwargs['bib_file_path']).is_absolute():
            kwargs['bib_file_path'] = str(Path.cwd().joinpath(kwargs['bib_file_path']))
        else:
            kwargs['bib_file_path'] = fallback(kwargs['bib_file_path'], config.get('bib_file_path', None))

    if 'save_to_bib_file' in kwargs:
        kwargs['save_to_bib_file'] = fallback(kwargs['save_to_bib_file'], config.get('save_to_bib_file', 'True'))  # noqa: E501

    return kwargs


def main() -> int:
    parser = get_parser()
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    kwargs = vars(arguments)
    mode = kwargs.pop('mode', None)

    if mode == 'run':
        kwargs = sanitize_arguments(**kwargs)
        return run(**kwargs)

    elif mode == 'download':
        kwargs = sanitize_arguments(**kwargs)
        return download(**kwargs)

    elif mode == 'set-config':
        if kwargs['bib_file_path'] is not None and not Path(kwargs['bib_file_path']).is_absolute():
            kwargs['bib_file_path'] = str(Path.cwd().joinpath(kwargs['bib_file_path']))
            print(f'The path was relative, path used: {kwargs["bib_file_path"]}')
        return setup(**kwargs)

    elif mode == 'inspect-config':
        return inspect()

    elif mode == 'clear-config':
        return clear()

    else:
        raise NotImplementedError('Invalid mode selection.')
