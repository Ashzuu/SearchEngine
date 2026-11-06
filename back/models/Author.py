from dataclasses import dataclass


@dataclass
class Author:
    """
    Author class which represents an author of a document
    """
    name: str
    nb_docs: int = 0
    productions: dict = None

    def __post_init__(self) -> None:
        if self.productions is None:
            self.productions = {}

    def add(self, document) -> None:
        self.productions[self.nb_docs] = document
        self.nb_docs += 1

    def __str__(self) -> str:
        return f"Author: {self.name} ({self.nb_docs} documents)"