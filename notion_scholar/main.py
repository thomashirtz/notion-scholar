import sys
import argparse
from typing import Optional

from notion_scholar.run import run
from notion_scholar import config


def get_parser():
    database_url, input_file_path, output_file_path = config.get_config()

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
        '-o', '--output-file-path', default=output_file_path, type=str, metavar='',
        help='Output file to use (default: %(default)s)'
    )
    run_parser.add_argument(
        '-t', '--token', default=None, type=str, metavar='',
        help='Token used to connect to Notion (default: token stored in "keyring")'
    )
    run_parser.add_argument(
        '-db', '--database-url', default=database_url, type=str, metavar='',
        help='Database that will be furnished (default: %(default)s)'
    )
    run_parser.add_argument(
        '-c', '--clean', default=False, action='store_true',
        help='Erasing the input file after the uploading bibtex to database'
    )
    run_parser.add_argument(
        '-ns', '--no-save', default=False, action='store_true',
        help='Disabling saving to output file'
    )

    if input_file_path is None:
        group = run_parser.add_mutually_exclusive_group(required=True)  # https://stackoverflow.com/questions/11154946/require-either-of-two-arguments-using-argparse
    else:
        group = run_parser.add_argument_group()

    group.add_argument(
        '-i', '--input-file-path', default=input_file_path, type=str, metavar='',
        help='Input file that will be used. This argument is required if the output file is not saved in the config (default: %(default)s)'
    )
    group.add_argument(
        '-b', '--bibtex', default=None, type=str, metavar='',
        help='Bibtex entry to add (default: %(default)s)'
    )

    # Setup parser
    setup_parser = subparsers.add_parser(
        "setup", parents=[parent_parser],
        help='Save the default values of notion-scholar.'
    )
    setup_parser.add_argument(
        '-i', '--input-file-path', default=input_file_path, type=str, metavar='',
        help='Save the input file path in the user config using "platformdirs". The path must be absolute and the file need to exist. (default: %(default)s)'
    )
    setup_parser.add_argument(
        '-o', '--output-file-path', default=output_file_path, type=str, metavar='',
        help='Save the output file path in the user config using "platformdirs". The path must be absolute and the file need to exist. (default: %(default)s)'
    )
    setup_parser.add_argument(
        '-t', '--token', default=None, type=str, metavar='',
        help='Save the token used to connect to Notion using "keyring" (default: %(default)s)'
    )
    setup_parser.add_argument(
        '-db', '--database-url', default=database_url, type=str, metavar='',
        help='Save the database-url in the user config using "platformdirs" (default: %(default)s)'
    )

    # Inspect config parser
    inspect_parser = subparsers.add_parser(
        "inspect", parents=[parent_parser],
        help='Inspect the notion-scholar config.'
    )
    return parser


def sanitize_arguments_and_run(
        token: Optional[str],
        database_url: Optional[str],
        input_file_path: Optional[str],
        output_file_path: Optional[str],
        bibtex_string: Optional[str],
        clean: bool,
        no_save: bool,
        **kwargs,
):
    token = token if token is not None else config.get_token()

    if bibtex_string is not None:
        input_file_path = None

    if token is None:
        raise config.ConfigError("The token is not set nor saved in the key ring.")
    if database_url is None:
        raise config.ConfigError("The database_url is not set nor saved in the config file.")

    return run(
        token=token,
        database_url=database_url,
        output_file_path=output_file_path,
        clean_input_file=clean,
        bibtex_string=bibtex_string,
        input_file_path=input_file_path,
        save_to_output_file=not no_save,
    )


def main():
    parser = get_parser()
    arguments = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    kwargs = vars(arguments)
    mode = kwargs.pop('mode', 'run')

    if mode == 'run':
        bibtex_string = kwargs.pop('bibtex', None)
        sanitize_arguments_and_run(bibtex_string=bibtex_string, **kwargs)
    elif mode == 'setup':
        config.setup(**kwargs)
    elif mode == 'inspect':
        config.inspect()
    else:
        raise NotImplementedError
