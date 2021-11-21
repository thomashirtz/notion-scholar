from typing import List

from bibtexparser import load
from bibtexparser import dumps
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.publication import Publication


def get_bib_database_from_file(file_path: str) -> BibDatabase:
    with open(file_path) as bibtex_file:
        return load(bibtex_file)


def get_bib_database_from_string(string: str) -> BibDatabase:
    bibtex_parser = BibTexParser(interpolate_strings=False)
    return bibtex_parser.parse(string)


def get_publication_list(bib_database: BibDatabase) -> List[Publication]:
    publications = []
    for entry in bib_database.entries:
        db = BibDatabase()
        db.entries = [entry]
        bibtex_str = dumps(db)
        publications.append(Publication(
            key=entry.get('ID', ''),
            title=entry.get('title', ''),
            author=entry.get('author', '').replace("\n", " "),
            year=int(entry.get('year', '')),
            journal=entry.get('journal', ''),
            url=entry.get('url', ''),
            abstract=entry.get('abstract', ''),
            bibtex=bibtex_str,
        ))
    return publications


def get_key_list(bib_file_path):
    bib_database = get_bib_database_from_file(bib_file_path)
    return [entry['ID'] for entry in bib_database.entries]
