import json

from models.document.ArvixDocument import ArvixDocument
from models.document.Document import Document
from models.document.RedditDocument import RedditDocument


class DocumentFactory:

    @staticmethod
    def create(data: dict) -> Document:
        """
        Factory for documents
        :param data: Data to implement in document
        :return: The correct document
        """
        doc: Document
        if data.get('origin') == 'reddit':
            return RedditDocument(
                title=data.get('title', ''),
                author=data.get('author', ''),
                date=str(data.get('date', '')),
                url=data.get('url', ''),
                text=data.get('text', ''),
                comments=int(data.get('comments', 0) or 0)
            )
        elif data.get('origin') == 'arxiv':
            try:
                coauthors = json.loads(data.get('coauthors', '[]'))
            except json.JSONDecodeError:
                coauthors = []
            return ArvixDocument(
                title=data.get('title', ''),
                author=data.get('author', ''),
                date=str(data.get('date', '')),
                url=data.get('url', ''),
                text=data.get('text', ''),
                coauthors=coauthors
            )
        raise ValueError("Unknown document origin")
