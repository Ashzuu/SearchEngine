from dataclasses import dataclass
from models.document.Document import Document

@dataclass
class ArvixDocument(Document):
    """
    A specific document in Arvix API.
    """
    coauthors: list

    def getType(self) -> str:
        return "arxiv"
    
    def __str__(self) -> str:
        return f"[Arxiv] {super().__str__()}"
