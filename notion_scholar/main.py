import sys
import argparse
from typing import Optional

from notion_scholar.run import run

from notion_scholar.config import clear
from notion_scholar.config import setup
from notion_scholar.config import inspect
from notion_scholar.config import get_token
from notion_scholar.config import get_config
from notion_scholar.config import ConfigError


def get_parser():
    token = get_token()
    config = get_config()

    def custom_bool(string: str) -> Optional[bool]:
        if string == "False":
            return False
        elif string == "True":
            return True
        else:
            return None

    parser = argparse.ArgumentParser(
        description='notion-scholar',
        usage='Use "notion-scholar --help" or "ns --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Parent parser
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Choice of the subparser
    subparsers = parser.add_subparsers(help='Selection of the action', dest='mode')

    # Run parser
    run_parser = subparsers.add_parser(
        "run", parents=[parent_parser],
        help='Run notion-scholar.'
    )
    run_parser.add_argument(
        '-t', '--token', default=None, type=str, metavar='', required=token is None,
        help=f'Token used to connect to Notion. (Already set? {token is not None})'
    )
    run_parser.add_argument(
        '-db', '--database-url', default=None, type=str, metavar='',
        help=f'Database that will be furnished (default: {config.get("database_url", None)})'
    )

    if config.get('bib_file_path', None) is None:
        group = run_parser.add_mutually_exclusive_group(required=True)  # https://stackoverflow.com/questions/11154946/require-either-of-two-arguments-using-argparse
    else:
        group = run_parser.add_argument_group()
    group.add_argument(
        '-f', '--bib-file-path', default=None, type=str, metavar='',
        help=f'Bib file that will be used. This argument is required if the bib file is not saved in the config and no bib-string is passed. (default: {config.get("bib_file_path", None)})'
    )
    group.add_argument(
        '-s', '--bib-string', default=None, type=str, metavar='',
        help='Bibtex entries to add (must be in-between three quotes \"\"\"<bib-string>\"\"\"). By default, the entries will be saved to the bib file from the config. It is possible to disable this behavior by changing the "save" option: "ns setup -save false".'
    )

    # Setup parser
    setup_parser = subparsers.add_parser(
        "set", parents=[parent_parser],
        help='Save the default values of notion-scholar.'
    )
    setup_parser.add_argument(
        '-f', '--bib-file-path', default=None, type=str, metavar='',
        help=f'Save the input file path in the user config using "platformdirs". The path must be absolute and the file need to exist. (default: {config.get("bib_file_path", None)})'
    )
    setup_parser.add_argument(  # todo clean how to handle boolean
        '-s', '--save', default=None, type=custom_bool, metavar='',
        help=f'Set whether the entries from "bib-string" will be saved in the bib file. (default: {config.get("save_to_bib_file", True)})'
    )
    setup_parser.add_argument(
        '-t', '--token', default=None, type=str, metavar='',
        help='Save the Notion token using "keyring".'
    )
    setup_parser.add_argument(
        '-db', '--database-url', default=None, type=str, metavar='',
        help=f'Save the database-url in the user config using the library "platformdirs". (default: {config.get("database_url", None)})'
    )

    # Inspect config parser
    inspect_parser = subparsers.add_parser(
        "inspect-config", parents=[parent_parser],
        help='Inspect the notion-scholar config.'
    )
    # Inspect config parser
    clear_parser = subparsers.add_parser(
        "clear-config", parents=[parent_parser],
        help='Clear the notion-scholar config.'
    )
    return parser


def sanitize_arguments_and_run(
        token: Optional[str] = None,
        database_url: Optional[str] = None,
        bib_file_path: Optional[str] = None,
        bib_string: Optional[str] = None,
        save: Optional[bool] = None,
        **kwargs,  # todo clean function
):
    def fallback(choice_1, choice_2):
        return choice_1 if choice_1 is not None else choice_2

    token = fallback(token, get_token())
    if token is None:
        raise ConfigError("The Notion token is not set nor saved.")

    config = get_config()
    database_url = fallback(database_url, config.get("database_url", None))
    if database_url is None:
        raise ConfigError("The database_url is not set nor saved.")

    bib_file_path = fallback(bib_file_path, config.get("bib_file_path", None))
    save_str = config.get("save_to_bib_file", "True")
    save = fallback(save, save_str == "True")
    return run(
        token=token,
        database_url=database_url,
        bib_string=bib_string,
        bib_file_path=bib_file_path,
        save_to_bib_file=save,
    )


def main():
    parser = get_parser()
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    kwargs = vars(arguments)
    mode = kwargs.pop('mode', None)

    if mode == 'run':
        sanitize_arguments_and_run(**kwargs)
    elif mode == 'set':
        setup(**kwargs)
    elif mode == 'inspect-config':
        inspect()
    elif mode == 'clear-config':
        clear()
    else:
        raise NotImplementedError
