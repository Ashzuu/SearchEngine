import unittest
from services.factories.DocumentFactory import DocumentFactory
from models.document.RedditDocument import RedditDocument
from models.document.ArvixDocument import ArvixDocument


class TestDocumentFactory(unittest.TestCase):
    """
    Tests unitaires pour la fabrique de documents.
    """

    def test_create_reddit_document(self):
        data = {
            "origin": "reddit",
            "title": "Discussion Reddit",
            "author": "reddit_user",
            "date": "1690000000",
            "url": "https://reddit.com/r/ml/1",
            "text": "Contenu du post reddit",
            "comments": "42"
        }

        doc = DocumentFactory.create(data)
        self.assertIsInstance(doc, RedditDocument)
        self.assertEqual(doc.title, "Discussion Reddit")
        self.assertEqual(doc.author, "reddit_user")
        self.assertEqual(doc.comments, 42)
        self.assertEqual(doc.getType(), "reddit")

    def test_create_reddit_document_default_comments(self):
        data = {
            "origin": "reddit",
            "title": "Discussion Reddit sans commentaires",
            "author": "user",
            "date": "1690000000",
            "url": "https://reddit.com",
            "text": "Texte",
            "comments": None
        }

        doc = DocumentFactory.create(data)
        self.assertIsInstance(doc, RedditDocument)
        self.assertEqual(doc.comments, 0)

    def test_create_arxiv_document_with_valid_coauthors(self):
        data = {
            "origin": "arxiv",
            "title": "Arxiv Paper",
            "author": "Principal Author",
            "date": "2023-01-01",
            "url": "https://arxiv.org/abs/2301.0001",
            "text": "Abstract of the paper",
            "coauthors": '["Coauthor 1", "Coauthor 2"]'
        }

        doc = DocumentFactory.create(data)
        self.assertIsInstance(doc, ArvixDocument)
        self.assertEqual(doc.title, "Arxiv Paper")
        self.assertEqual(doc.coauthors, ["Coauthor 1", "Coauthor 2"])
        self.assertEqual(doc.getType(), "arxiv")

    def test_create_arxiv_document_with_invalid_coauthors_json(self):
        data = {
            "origin": "arxiv",
            "title": "Paper with invalid json",
            "author": "Author",
            "date": "2023-01-01",
            "url": "https://arxiv.org/abs/2301.0002",
            "text": "Abstract",
            "coauthors": "not a valid json list"
        }

        doc = DocumentFactory.create(data)
        self.assertIsInstance(doc, ArvixDocument)
        self.assertEqual(doc.coauthors, [])

    def test_create_unknown_origin_raises_value_error(self):
        data = {
            "origin": "unknown_source",
            "title": "Test",
            "text": "Test"
        }

        with self.assertRaises(ValueError) as context:
            DocumentFactory.create(data)
        self.assertIn("Unknown document origin", str(context.exception))


if __name__ == "__main__":
    unittest.main()
