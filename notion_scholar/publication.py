from typing import List
from typing import NamedTuple


class Publication(NamedTuple):
    key: str
    title: str
    authors: str
    year: int
    journal: str
    url: str
    bibtex: str
    abstract: str

    def __str__(self):
        return f'Publication(key="{self.key}", title="{self.title}")'


def filter_publication_list(
        publication_list: List[Publication],
        key_list_to_exclude: List[str],
) -> List[Publication]:
    return [p for p in publication_list if p.key not in key_list_to_exclude]
