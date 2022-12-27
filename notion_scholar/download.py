from notion_scholar.notion_api import get_bibtex_string_list_from_database
from notion_scholar.utilities import write_to_file


def download(
        file_path: str,
        token: str,
        database_id: str,
) -> int:
    """Write the bibliography from the database `database_id` in the file
    located at `file_path`.

    Args:
        file_path: File path in which the bibliography will be saved.
        token: Notion API token.
        database_id: Targeted database id.

    Returns:
        Error code.
    """
    bibtex_str_list = get_bibtex_string_list_from_database(
        token=token,
        database_id=database_id,
    )
    write_to_file(
        content='\n\n'.join(bibtex_str_list),
        file_path=file_path,

    )
    return 0
