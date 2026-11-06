from dataclasses import dataclass
from models.document.Document import Document

@dataclass
class RedditDocument(Document):
    """
    A specific document in Reddit API.
    """
    comments: int

    def getType(self) -> str:
        return "reddit"
    
    def __str__(self) -> str:
        return f"[Reddit] {super().__str__()}"