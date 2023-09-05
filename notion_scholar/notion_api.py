import warnings
from typing import Any
from typing import Callable
from typing import List
from typing import Union

from notion_client import Client

from notion_scholar.publication import Publication


class Property:
    @staticmethod
    def title(value: str) -> dict:
        return {'title': [{'text': {'content': value}}]}

    @staticmethod
    def rich_text(value: str) -> dict:
        return {'rich_text': [{'text': {'content': value}}]}

    @staticmethod
    def number(value: Union[int, float]) -> dict:
        return {'number': value}

    @staticmethod
    def url(value: str) -> dict:
        return {'url': value if value else None}

    @staticmethod
    def checkbox(value: bool) -> dict:
        return {'checkbox': value}

    @staticmethod
    def select(value: str) -> dict:
        return {"select": {"name": value}}


def add_publications_to_database(
        publications: List[Publication],
        token: str,
        database_id: str,
) -> None:
    # todo retrieve the list of all the property and filter
    # todo update_database_with_publications check the empty fields and fill them
    client = Client(auth=token)
    for i, publication in enumerate(publications, start=1):
        print(f'{i}/{len(publications)}: {publication}')

        abstract = publication.abstract
        if len(abstract) > 2000:
            warnings.warn(
                f'{publication.key} has its abstract too long ({len(abstract)} > 2000). '
                f'Because of the 2000 characters API limitation, the abstract has '
                f'therefore been truncated at the 2000th character.',
                stacklevel=0,
            )
            abstract = abstract[:2000]
        authors = publication.authors
        if len(authors) > 2000:
            warnings.warn(
                f'{publication.key} has its abstract too long ({len(authors)} > 2000). '
                f'Because of the 2000 characters API limitation, the author list has '
                f'therefore been truncated at the 2000th character.',
                stacklevel=0,
            )
            authors = authors[:2000]
        bibtex = publication.bibtex
        if len(bibtex) > 2000:
            warnings.warn(
                f'{publication.key} has its abstract too long ({len(bibtex)} > 2000). '
                f'Because of the 2000 characters API limitation, the author list has '
                f'therefore been truncated at the 2000th character.',
                stacklevel=0,
            )
            bibtex = bibtex[:2000]
        client.pages.create(
            parent={'database_id': database_id},
            properties={
                'Title': Property.title(publication.title),
                'Abstract': Property.rich_text(abstract),
                'Bibtex': Property.rich_text(bibtex),
                'Filename': Property.rich_text(publication.key),
                'Journal': Property.rich_text(publication.journal),
                'Authors': Property.rich_text(authors),
                'Year': Property.number(publication.year),
                'URL': Property.url(publication.url),
                'Category': Property.relation(publication.keywords),
                'Inbox': Property.checkbox(True),
                'Type': Property.select(publication.type),
                'DOI': Property.rich_text(publication.doi),
            },
        )


def get_property_list_from_database(
        token: str,
        database_id: str,
        retriever: Callable[[dict], Any],
        page_size: int = 100,
) -> List[str]:
    notion = Client(auth=token)

    results = []
    query = notion.databases.query(
        database_id=database_id, page_size=page_size,
    )
    results.extend(query['results'])
    while query['next_cursor'] or (query['results'] is None and not results):
        query = notion.databases.query(
            database_id=database_id,
            start_cursor=query['next_cursor'],
            page_size=page_size,
        )
        results.extend(query['results'])

    key_list = []
    for result in results:
        try:
            key_list.append(retriever(result))
        except IndexError:
            pass
    return key_list


def get_publication_key_list_from_database(
        token: str,
        database_id: str,
        page_size: int = 100,
) -> List[str]:

    def retrieve_publication_key(result: dict) -> str:
        return result['properties']['Filename']['rich_text'][0]['plain_text']

    return get_property_list_from_database(
        token=token,
        database_id=database_id,
        retriever=retrieve_publication_key,
        page_size=page_size,
    )


def get_bibtex_string_list_from_database(
        token: str,
        database_id: str,
        page_size: int = 100,
) -> List[str]:

    def retrieve_bibtex_string(result: dict) -> str:
        return result['properties']['Bibtex']['rich_text'][0]['plain_text']

    return get_property_list_from_database(
        token=token,
        database_id=database_id,
        retriever=retrieve_bibtex_string,
        page_size=page_size,
    )
