from dataclasses import dataclass

from models.document import Document

@dataclass
class ArvixDocument(Document):
    """
    A specific document in Arvix API.
    """
    __coauthors: list
