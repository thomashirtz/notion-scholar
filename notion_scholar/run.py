from collections import Counter
from typing import List
from typing import Optional

from bibtexparser import dumps
from bibtexparser.bibdatabase import BibDatabase

from notion_scholar.bibtex import get_bib_database_from_file
from notion_scholar.bibtex import get_bib_database_from_string
from notion_scholar.bibtex import get_key_list
from notion_scholar.bibtex import get_publication_list
from notion_scholar.notion_api import add_publications_to_database
from notion_scholar.notion_api import get_publication_key_list_from_database
from notion_scholar.publication import Publication
from notion_scholar.utilities import append_string_to_file
from notion_scholar.utilities import NotionScholarException


class IllegalArgumentException(NotionScholarException):
    pass


def run(
        token: str,
        database_id: str,
        bib_file_path: Optional[str],
        bib_string: Optional[str],
        save_to_bib_file: bool = True,
) -> int:
    if bib_string is not None:
        bib_database: BibDatabase = get_bib_database_from_string(
            string=bib_string,
        )
    elif bib_file_path is not None:
        bib_database = get_bib_database_from_file(
            file_path=bib_file_path,
        )
    else:
        raise IllegalArgumentException(
            'Must provide a "bib_string" or a "bib_file_path"',
        )

    publication_list: List[Publication] = get_publication_list(bib_database)
    key_list = get_publication_key_list_from_database(
        token=token,
        database_id=database_id,
    )
    publication_list_filtered = [p for p in publication_list if p.key not in key_list]  # noqa: E501
    add_publications_to_database(
        publications=publication_list_filtered,
        token=token,
        database_id=database_id,
    )

    if not publication_list_filtered and publication_list:
        print('\nAll the publications are already present in the database.')

    if bib_string is not None and save_to_bib_file and bib_file_path is not None:  # noqa E501 todo edit
        key_list = get_key_list(bib_file_path)
        duplicate_key_list = [k for k, v in Counter(key_list).items() if v > 1]
        if duplicate_key_list:
            print(f'\nWarning! There is duplicates in the file: {duplicate_key_list}')  # noqa: E501

        entries = []
        print(f'\nSaving the entries to {bib_file_path}')
        for i, entry in enumerate(bib_database.entries):
            if entry['ID'] not in key_list:
                entries.append(entry)
            else:
                print(f'"{entry["ID"]}" is already present in the file.')

        bib_database.entries = entries
        string = dumps(bib_database)
        append_string_to_file(content=string, file_path=bib_file_path)
    return 0
