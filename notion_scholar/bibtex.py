from typing import List

from bibtexparser import load
from bibtexparser import dumps
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.publication import Publication


def get_bib_database_from_file(file_path: str) -> BibDatabase:
    """
    Read a file and parse the BibTex entries present in it.

    Args:
        file_path: path of the file that needs to be parsed.

    Returns:
        BibDatabase object that contains the instances present in the
        file.
    """
    with open(file_path) as bibtex_file:
        parser = BibTexParser(common_strings=True)
        return load(bibtex_file, parser=parser)


def get_bib_database_from_string(string: str) -> BibDatabase:
    """
    Create a BibDatabase object from a string of BibTex entries.

    Args:
        string: string containing the BibTex entries.

    Returns:
        BibDatabase object that contains the instances present in the
        string.
    """
    bibtex_parser = BibTexParser(interpolate_strings=False, common_strings=True)
    return bibtex_parser.parse(string)


def get_publication_list(bib_database: BibDatabase) -> List[Publication]:
    """
    Convert a BibDatabase object into a list of "Publication"s.

    Args:
        bib_database: a BibDatabase object.

    Returns:
        List of "Publication"s.
    """
    publications = []
    for entry in bib_database.entries:
        db = BibDatabase()
        db.entries = [entry]
        bibtex_str = dumps(db)
        publications.append(Publication(
            key=entry.get('ID', ''),
            title=entry.get('title', ''),
            authors=entry.get('author', '').replace("\n", " "),
            year=int(entry.get('year', '')),
            journal=entry.get('journal', ''),
            url=entry.get('url', ''),
            abstract=entry.get('abstract', ''),
            bibtex=bibtex_str,
        ))
    return publications


def get_key_list(bib_file_path: str) -> list:
    """
    Read a BibTex file and return the list of ID of the paper present in it.

    Args:
        bib_file_path: path of the file that needs to be inspected.

    Returns:
        List of IDs.
    """
    bib_database = get_bib_database_from_file(bib_file_path)
    return [entry['ID'] for entry in bib_database.entries]
