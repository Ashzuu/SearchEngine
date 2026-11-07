import unittest
from models.Author import Author
from models.document.Document import Document


class TestAuthor(unittest.TestCase):
    """
    Tests unitaires pour la classe Author selon le cahier des charges.
    """

    def test_author_initialization(self):
        """Initialisation d'un auteur et valeurs par defaut."""
        author = Author(name="Ada Lovelace")

        self.assertEqual(author.name, "Ada Lovelace")
        self.assertEqual(author.nb_docs, 0)
        self.assertEqual(author.productions, {})
        self.assertEqual(str(author), "Author: Ada Lovelace (0 documents)")

    def test_author_add_single_document(self):
        """Ajout d'un document a la production de l'auteur."""
        author = Author(name="Geoffrey Hinton")
        doc1 = Document(
            title="Deep Learning",
            author="Geoffrey Hinton",
            date="2015",
            url="https://example.com/deep",
            text="Deep learning allows computational models..."
        )

        author.add(doc1)
        self.assertEqual(author.nb_docs, 1)
        self.assertIn(0, author.productions)
        self.assertEqual(author.productions[0], doc1)
        self.assertEqual(str(author), "Author: Geoffrey Hinton (1 documents)")

    def test_author_add_multiple_documents(self):
        """Ajout de plusieurs documents et statistiques de production."""
        author = Author(name="Yann LeCun")
        doc1 = Document("Doc 1", "Yann LeCun", "1998", "url1", "Short text.")
        doc2 = Document("Doc 2", "Yann LeCun", "2004", "url2", "Much longer text for testing length.")

        author.add(doc1)
        author.add(doc2)

        self.assertEqual(author.nb_docs, 2)
        self.assertEqual(len(author.productions), 2)
        self.assertEqual(author.productions[0], doc1)
        self.assertEqual(author.productions[1], doc2)
        self.assertEqual(str(author), "Author: Yann LeCun (2 documents)")

        # Calcul des statistiques (Partie 5.4)
        total_len = sum(len(d.text) for d in author.productions.values())
        avg_len = total_len / author.nb_docs
        self.assertGreater(avg_len, 0)


if __name__ == "__main__":
    unittest.main()
