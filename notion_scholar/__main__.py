from typing import List

from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.utilities import merge_files
from notion_scholar.publication import Publication
from notion_scholar.bibtex import get_publications
from notion_scholar.bibtex import get_bib_database
from notion_scholar.notion_api import add_publications_to_database

from notion_scholar.config import token
from notion_scholar.config import input_path
from notion_scholar.config import database_url
from notion_scholar.config import bibliography_path


def main(input_path: str = input_path, bibliography_path: str = bibliography_path) -> None:
    bib_database: BibDatabase = get_bib_database(path=input_path)
    publications: List[Publication] = get_publications(bib_database=bib_database)
    add_publications_to_database(publications=publications, token=token, database_url=database_url)
    merge_files(input_path=input_path, bibliography_path=bibliography_path)


if __name__ == '__main__':
    main()
