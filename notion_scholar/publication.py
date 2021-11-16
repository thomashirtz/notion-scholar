from typing import NamedTuple


class Publication(NamedTuple):
    key: str
    title: str
    author: str
    year: int
    journal: str
    url: str
    bibtex: str
    abstract: str
