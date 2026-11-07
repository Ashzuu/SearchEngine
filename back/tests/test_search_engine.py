import unittest
import pandas as pd
from models.Corpus import Corpus
from models.document.Document import Document
from models.document.RedditDocument import RedditDocument
from models.document.ArvixDocument import ArvixDocument
from services.SearchEngine import SearchEngine


class TestSearchEngine(unittest.TestCase):
    """
    Tests unitaires pour la classe SearchEngine.
    """

    def setUp(self):
        self.corpus = Corpus()
        self._reset_corpus(self.corpus)
        self._populate_corpus()
        self.engine = SearchEngine(self.corpus)

    def tearDown(self):
        self._reset_corpus(self.corpus)

    def _reset_corpus(self, corpus):
        corpus.documents.clear()
        corpus.nb_docs = 0
        corpus.authors.clear()
        corpus._texte_concat = None
        corpus._vocab = None
        corpus._freq = None
        corpus._mat_TF = None
        corpus._mat_TFxIDF = None

    def _populate_corpus(self):
        doc1 = Document(
            title="Transformer Architecture for Deep Learning",
            author="Author Alpha",
            date="2020-01-01",
            url="http://example.com/1",
            text="Transformers revolutionized natural language processing and computer vision."
        )
        doc2 = RedditDocument(
            title="Discussion on Computer Vision Models",
            author="reddit_geek",
            date="2021-05-10",
            url="http://reddit.com/r/ml/2",
            text="Computer vision with convolutional neural networks and vision transformers.",
            comments=15
        )
        doc3 = ArvixDocument(
            title="Reinforcement Learning in Robotics",
            author="Dr. Beta",
            date="2022-09-15",
            url="http://arxiv.org/abs/2209.001",
            text="Policy gradient algorithms and reinforcement learning applied to robotic manipulation.",
            coauthors=["Gamma"]
        )
        self.corpus.add_document(doc1)
        self.corpus.add_document(doc2)
        self.corpus.add_document(doc3)

    def test_search_engine_initialization(self):
        self.assertIsNotNone(self.engine.mat_TF)
        self.assertIsNotNone(self.engine.mat_TFxIDF)
        self.assertIsNotNone(self.engine.idf)
        self.assertIsNotNone(self.engine.doc_norms)
        self.assertEqual(len(self.engine.vocab), len(self.corpus.vocab))

    def test_search_valid_query_ranking(self):
        """Verifie que les documents les plus pertinents obtiennent les meilleurs scores."""
        df = self.engine.search("robotics reinforcement", top_n=5)

        self.assertIsInstance(df, pd.DataFrame)
        expected_columns = ["id", "score", "titre", "origine", "url", "auteur", "date", "texte"]
        self.assertListEqual(list(df.columns), expected_columns)
        self.assertGreater(len(df), 0)

        premier_resultat = df.iloc[0]
        self.assertEqual(premier_resultat["id"], 2)
        self.assertEqual(premier_resultat["origine"], "arxiv")
        self.assertGreater(premier_resultat["score"], 0)

    def test_search_reddit_document_metadata(self):
        """Verifie que la recherche retourne correctement les metadonnees Reddit."""
        df = self.engine.search("convolutional networks", top_n=5)

        self.assertGreater(len(df), 0)
        premier = df.iloc[0]
        self.assertEqual(premier["id"], 1)
        self.assertEqual(premier["origine"], "reddit")
        self.assertEqual(premier["auteur"], "reddit_geek")

    def test_search_empty_query(self):
        """Une requete vide doit renvoyer un DataFrame vide avec les colonnes attendues."""
        df = self.engine.search("")
        self.assertEqual(len(df), 0)
        expected_columns = ["id", "score", "titre", "origine", "url", "auteur", "date", "texte"]
        self.assertListEqual(list(df.columns), expected_columns)

    def test_search_query_without_matching_words(self):
        """Une requete composee uniquement de mots absents du vocabulaire doit retourner 0 resultat."""
        df = self.engine.search("supercalifragilistic nonexistingword")
        self.assertEqual(len(df), 0)

    def test_search_top_n_limit(self):
        """La recherche doit respecter le parametre top_n."""
        df = self.engine.search("learning", top_n=1)
        self.assertLessEqual(len(df), 1)

    def test_concorde_and_stats_delegation(self):
        """Verifie la delegation des methodes concorde et stats vers le corpus."""
        df_concorde = self.engine.concorde("transformers")
        self.assertIsInstance(df_concorde, pd.DataFrame)
        self.assertIn("motif trouvé", df_concorde.columns)

        df_stats = self.engine.stats(n=3)
        self.assertIsInstance(df_stats, pd.DataFrame)
        self.assertIn("term frequency", df_stats.columns)


if __name__ == "__main__":
    unittest.main()
