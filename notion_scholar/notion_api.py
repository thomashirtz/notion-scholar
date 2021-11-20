from typing import List

from notion.client import NotionClient
from notion_scholar.publication import Publication


def add_publications_to_database(
        publications: List[Publication],
        token: str,
        database_url: str,
) -> None:
    client = NotionClient(token_v2=token)
    cv = client.get_collection_view(database_url)
    for publication in publications:
        print(publication.key, publication)
        row = cv.collection.add_row()
        row.name = publication.title
        row.abstract = publication.abstract
        row.year = publication.year
        row.bibtex = publication.bibtex
        row.filename = publication.key
        row.journal = publication.journal
        row.authors = publication.author
        row.url = publication.url
        row.inbox = True
