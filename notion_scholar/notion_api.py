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


def add_publications_to_database(
        publications: List[Publication],
        token: str,
        database_id: str,
) -> None:
    client = Client(auth=token)
    for i, publication in enumerate(publications, start=1):
        print(f'{i}/{len(publications)}: {publication}')
        client.pages.create(
            parent={'database_id': database_id},
            properties={
                'Title': Property.title(publication.title),
                'Abstract': Property.rich_text(publication.abstract),
                'Bibtex': Property.rich_text(publication.bibtex),
                'Filename': Property.rich_text(publication.key),
                'Journal': Property.rich_text(publication.journal),
                'Authors': Property.rich_text(publication.authors),
                'Year': Property.number(publication.year),
                'URL': Property.url(publication.url),
                'Inbox': Property.checkbox(True),
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
