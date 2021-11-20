from typing import List
from typing import Optional

from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.utilities import clean_file
from notion_scholar.utilities import merge_files
from notion_scholar.publication import Publication
from notion_scholar.utilities import append_string_to_file
from notion_scholar.bibtex import get_publication_list
from notion_scholar.bibtex import get_bib_database_from_file
from notion_scholar.bibtex import get_bib_database_from_string
from notion_scholar.notion_api import add_publications_to_database


def run(
        token: str,
        database_url: str,
        output_file_path: str,
        bibtex_string: Optional[str] = None,
        input_file_path: Optional[str] = None,
        clean_input_file: bool = True,
        save_to_output_file: bool = True,
) -> None:

    if input_file_path is not None:
        bib_database: BibDatabase = get_bib_database_from_file(file_path=input_file_path)
    elif bibtex_string is not None:
        bib_database: BibDatabase = get_bib_database_from_string(string=bibtex_string)
    else:
        raise Exception('Must provide bib_string or input file')

    publications: List[Publication] = get_publication_list(bib_database=bib_database)
    add_publications_to_database(publications=publications, token=token, database_url=database_url)

    if input_file_path is not None and output_file_path is not None:
        if save_to_output_file:
            merge_files(input_path=input_file_path, output_file=output_file_path)
        if clean_input_file:
            clean_file(file_path=input_file_path)

    elif output_file_path is not None:
        append_string_to_file(string=bibtex_string, file_path=output_file_path)
