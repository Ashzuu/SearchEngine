import unittest
from models.document.Document import Document
from models.document.RedditDocument import RedditDocument
from models.document.ArvixDocument import ArvixDocument


class TestDocuments(unittest.TestCase):
    """
    Tests unitaires pour les classes Document, RedditDocument et ArvixDocument
    selon le cahier des charges.
    """

    def test_document_attributes_and_str(self):
        """Verification des attributs de base et de __str__."""
        doc = Document(
            title="Introduction to Machine Learning",
            author="Alan Turing",
            date="1950-10-01",
            url="https://example.com/ml",
            text="A computer would deserve to be called intelligent if it could deceive a human."
        )

        self.assertEqual(doc.title, "Introduction to Machine Learning")
        self.assertEqual(doc.author, "Alan Turing")
        self.assertEqual(doc.date, "1950-10-01")
        self.assertEqual(doc.url, "https://example.com/ml")
        self.assertEqual(doc.text, "A computer would deserve to be called intelligent if it could deceive a human.")
        self.assertEqual(str(doc), "Introduction to Machine Learning by Alan Turing")
        self.assertEqual(doc.getType(), "generic")

    def test_reddit_document_inheritance_and_specifics(self):
        """Verification de la classe RedditDocument."""
        doc = RedditDocument(
            title="Cool discussion on Neural Networks",
            author="redditor_user",
            date="1609459200",
            url="https://reddit.com/r/MachineLearning/comments/123",
            text="Discussion text content here",
            comments=42
        )

        self.assertIsInstance(doc, Document)
        self.assertEqual(doc.comments, 42)
        self.assertEqual(doc.getType(), "reddit")
        self.assertEqual(str(doc), "[Reddit] Cool discussion on Neural Networks by redditor_user")

    def test_arxiv_document_inheritance_and_specifics(self):
        """Verification de la classe ArvixDocument."""
        coauthors = ["Alice Martin", "Bob Dupont"]
        doc = ArvixDocument(
            title="Attention Is All You Need",
            author="Ashish Vaswani",
            date="2017-06-12",
            url="https://arxiv.org/abs/1706.03762",
            text="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.",
            coauthors=coauthors
        )

        self.assertIsInstance(doc, Document)
        self.assertEqual(doc.coauthors, coauthors)
        self.assertEqual(doc.getType(), "arxiv")
        self.assertEqual(str(doc), "[Arxiv] Attention Is All You Need by Ashish Vaswani")

    def test_polymorphism_in_collection(self):
        """Verification du polymorphisme entre differentes sous-classes."""
        docs = [
            Document("Generic Doc", "Author A", "2020", "url1", "text1"),
            RedditDocument("Reddit Doc", "Author B", "2021", "url2", "text2", comments=10),
            ArvixDocument("Arxiv Doc", "Author C", "2022", "url3", "text3", coauthors=["Author D"])
        ]

        types = [d.getType() for d in docs]
        self.assertEqual(types, ["generic", "reddit", "arxiv"])

        representations = [str(d) for d in docs]
        self.assertEqual(representations, [
            "Generic Doc by Author A",
            "[Reddit] Reddit Doc by Author B",
            "[Arxiv] Arxiv Doc by Author C"
        ])


if __name__ == "__main__":
    unittest.main()
