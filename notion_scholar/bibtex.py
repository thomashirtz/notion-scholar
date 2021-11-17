from typing import List

from bibtexparser import load
from bibtexparser import dumps
from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.publication import Publication


def get_bib_database(path: str) -> BibDatabase:
    with open(path) as bibtex_file:
        return load(bibtex_file)


def get_publications(bib_database: BibDatabase) -> List[Publication]:
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
