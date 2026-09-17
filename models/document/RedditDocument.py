from dataclasses import dataclass

from models.document.Document import Document


@dataclass
class RedditDocument(Document):
    """
    A specific document in Reddit API.
    """
    comment:str