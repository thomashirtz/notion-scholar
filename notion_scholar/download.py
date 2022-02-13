from notion_scholar.notion_api import get_bibtex_string_list_from_database
from notion_scholar.utilities import write_to_file


def download(
        file_path: str,
        token: str,
        database_id: str,
):
    bibtex_str_list = get_bibtex_string_list_from_database(
        token=token,
        database_id=database_id,
    )
    write_to_file(
        content='\n\n'.join(bibtex_str_list),
        file_path=file_path,
    )
    return 0
