from typing import List

from bibtexparser import dumps
from bibtexparser import load
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser

from notion_scholar.publication import Publication


def get_bib_database_from_file(file_path: str) -> BibDatabase:
    """Read a file and parse the BibTex entries present in it.

    Args:
        file_path: path of the file that needs to be parsed.

    Returns:
        BibDatabase object that contains the instances present in the
        file.
    """
    with open(file_path, encoding='utf-8') as bibtex_file:
        parser = BibTexParser(
            common_strings=True,
            ignore_nonstandard_types=False,
        )
        return load(bibtex_file, parser=parser)


def get_bib_database_from_string(string: str) -> BibDatabase:
    """Create a BibDatabase object from a string of BibTex entries.

    Args:
        string: string containing the BibTex entries.

    Returns:
        BibDatabase object that contains the instances present in the
        string.
    """
    bibtex_parser = BibTexParser(
        interpolate_strings=False,
        common_strings=True,
        ignore_nonstandard_types=False,
    )
    return bibtex_parser.parse(string)


def get_bibtex_str(entry: dict) -> str:
    """"""
    database = BibDatabase()
    database.entries = [dict(entry)]
    bibtex_str = dumps(database)

    copied_entry = dict(entry)
    if len(bibtex_str) > 2000:
        copied_entry.pop('abstract', None)

    database.entries = [copied_entry]
    bibtex_str = dumps(database)
    return bibtex_str if len(bibtex_str) > 2000 else ''


def get_publication_list(bib_database: BibDatabase) -> List[Publication]:
    """Convert a BibDatabase object into a list of "Publication"s.

    Args:
        bib_database: a BibDatabase object.

    Returns:
        List of "Publication"s.
    """
    publications = []
    for entry in bib_database.entries:
        publications.append(
            Publication(
                key=entry.get('ID', ''),
                title=entry.get('title', ''),
                authors=entry.get('author', '').replace('\n', ' '),
                year=int(entry['year']) if 'year' in entry.keys() else None,
                journal=entry.get('journal', ''),
                url=entry.get('url', ''),
                abstract=entry.get('abstract', ''),
                doi=entry.get('doi', ''),
                type=entry.get('ENTRYTYPE', '').lower(),
                bibtex=get_bibtex_str(entry),
                keywords=entry.get('keywords',''),
            ),
        )
    return publications


def get_key_list(bib_file_path: str) -> list:
    """Read a BibTex file and return the list of ID of the paper present in it.

    Args:
        bib_file_path: path of the file that needs to be inspected.

    Returns:
        List of IDs.
    """
    bib_database = get_bib_database_from_file(bib_file_path)
    return [entry['ID'] for entry in bib_database.entries]
