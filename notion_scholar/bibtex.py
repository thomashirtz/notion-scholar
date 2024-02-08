from typing import List

from bibtexparser import dumps
from bibtexparser import load
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser

from notion_scholar.publication import Publication


def get_bib_database_from_file(file_path: str) -> BibDatabase:
    """
    Parses a BibTeX file to create a BibDatabase object.

    This function reads a BibTeX file specified by the file path, parses the
    BibTeX entries within it, and returns a BibDatabase object containing all
    the parsed entries.

    Args:
        file_path (str): The path to the BibTeX file to be parsed.

    Returns:
        BibDatabase: An object containing the parsed BibTeX entries from the file.
    """
    with open(file_path, encoding='utf-8') as bibtex_file:
        parser = BibTexParser(
            common_strings=True,
            ignore_nonstandard_types=False,
        )
        return load(bibtex_file, parser=parser)


def get_bib_database_from_string(string: str) -> BibDatabase:
    """
    Converts a string containing BibTeX entries into a BibDatabase object.

    This function takes a string that contains one or more BibTeX entries,
    parses these entries, and returns a BibDatabase object that encapsulates
    the parsed entries.

    Args:
        string (str): A string containing BibTeX entries.

    Returns:
        BibDatabase: An object containing the parsed BibTeX entries.
    """
    bibtex_parser = BibTexParser(
        interpolate_strings=False,
        common_strings=True,
        ignore_nonstandard_types=False,
    )
    return bibtex_parser.parse(string)


def get_bibtex_str(entry: dict) -> str:
    """
    Generates a BibTeX string from a single entry dictionary, excluding the 'abstract' field if the resulting string is too long.

    This function takes a dictionary representing a single BibTeX entry, converts
    it to a BibTeX-formatted string, and returns it. If the generated string exceeds
    2000 characters, the 'abstract' field is omitted to reduce size.

    Args:
        entry (dict): A dictionary representing a single BibTeX entry.

    Returns:
        str: A BibTeX-formatted string. Returns an empty string if the resulting string without the 'abstract' is still over 2000 characters.
    """
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
    """
    Converts a BibDatabase object into a list of Publication objects.

    This function iterates over each entry in a BibDatabase object, creates a
    Publication object for each entry, and returns a list of these Publication
    objects. Each Publication object contains bibliographic information such as
    title, authors, year, etc., extracted from the BibDatabase entries.

    Args:
        bib_database (BibDatabase): The BibDatabase object containing BibTeX entries.

    Returns:
        List[Publication]: A list of Publication objects created from the BibDatabase entries.
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
            ),
        )
    return publications


def get_key_list(bib_file_path: str) -> list:
    """
    Extracts and returns the list of IDs from a BibTeX file.

    This function reads a BibTeX file, parses it to extract all entries, and
    then compiles a list of the 'ID' fields from these entries, which typically
    serve as unique identifiers for the bibliographic entries.

    Args:
        bib_file_path (str): The file path to the BibTeX file.

    Returns:
        list: A list of string IDs from the BibTeX file entries.
    """
    bib_database = get_bib_database_from_file(bib_file_path)
    return [entry['ID'] for entry in bib_database.entries]
