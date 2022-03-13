from typing import NamedTuple


class Publication(NamedTuple):
    """NamedTuple object used to store a bibtex publication reference."""
    key: str
    title: str
    authors: str
    year: int
    journal: str
    url: str
    bibtex: str
    abstract: str
    doi: str
    type: str

    def __str__(self):  # noqa TYP004
        return f'Publication(key="{self.key}", title="{self.title}")'
