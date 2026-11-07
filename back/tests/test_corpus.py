import unittest
import pandas as pd
from scipy.sparse import csr_matrix
from models.Corpus import Corpus
from models.document.Document import Document
from models.document.RedditDocument import RedditDocument
from models.document.ArvixDocument import ArvixDocument


class TestCorpus(unittest.TestCase):
    """
    Tests unitaires pour la classe Corpus.
    """

    def setUp(self):
        """Reinitialisation de l'instance singleton du Corpus avant chaque test."""
        self.corpus = Corpus()
        self._reset_corpus(self.corpus)

    def tearDown(self):
        """Nettoyage apres chaque test."""
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

    def test_corpus_singleton(self):
        """Unicite du Corpus via le patron Singleton."""
        corpus1 = Corpus()
        corpus2 = Corpus()
        self.assertIs(corpus1, corpus2)

    def test_add_document_and_authors_tracking(self):
        """Ajout de documents et gestion automatique des auteurs."""
        doc1 = Document("Doc 1", "Author One", "2021-01-01", "http://url1", "First text about machine learning.")
        doc2 = RedditDocument("Doc 2", "Author One", "2021-02-01", "http://url2", "Second text about deep learning.", comments=5)
        doc3 = ArvixDocument("Doc 3", "Author Two", "2021-03-01", "http://url3", "Third text about neural networks.", coauthors=["Co1"])

        self.corpus.add_document(doc1)
        self.assertEqual(self.corpus.nb_docs, 1)
        self.assertIn(0, self.corpus.documents)
        self.assertEqual(self.corpus.documents[0], doc1)
        self.assertIn("Author One", self.corpus.authors)
        self.assertEqual(self.corpus.authors["Author One"].nb_docs, 1)

        self.corpus.add_document(doc2)
        self.assertEqual(self.corpus.nb_docs, 2)
        self.assertEqual(self.corpus.authors["Author One"].nb_docs, 2)

        self.corpus.add_document(doc3)
        self.assertEqual(self.corpus.nb_docs, 3)
        self.assertIn("Author Two", self.corpus.authors)
        self.assertEqual(self.corpus.authors["Author Two"].nb_docs, 1)

    def test_texte_concat(self):
        """Concaténation de l'ensemble des textes."""
        self.corpus.add_document(Document("T1", "A1", "D1", "U1", "Text one."))
        self.corpus.add_document(Document("T2", "A2", "D2", "U2", "Text two."))

        texte_concat = self.corpus.texte_concat
        self.assertEqual(texte_concat, "Text one.\nText two.")

    def test_regex_search(self):
        """Recherche par expression reguliere avec contexte."""
        self.corpus.add_document(Document("T1", "A1", "D1", "U1", "This is an important experiment on deep learning."))
        self.corpus.add_document(Document("T2", "A2", "D2", "U2", "Another study regarding machine learning applications."))

        passages = self.corpus.search("learning", context_size=15)
        self.assertGreater(len(passages), 0)
        for passage in passages:
            self.assertIn("learning", passage.lower())

        passages_upper = self.corpus.search("LEARNING", context_size=15)
        self.assertEqual(len(passages), len(passages_upper))
        self.assertEqual(self.corpus.search("quantum"), [])
        self.assertEqual(self.corpus.search(""), [])

    def test_concorde(self):
        """Concordancier sous forme de DataFrame pandas."""
        self.corpus.add_document(Document("T1", "A1", "D1", "U1", "Voici un premier exemple de motif trouve au milieu du texte."))

        df = self.corpus.concorde("motif", context_size=10)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ["contexte gauche", "motif trouvé", "contexte droit"])
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["motif trouvé"], "motif")

        df_empty = self.corpus.concorde("")
        self.assertListEqual(list(df_empty.columns), ["contexte gauche", "motif trouvé", "contexte droit"])
        self.assertEqual(len(df_empty), 0)

    def test_vocab_and_freq(self):
        """Construction du vocabulaire et table des frequences."""
        self.corpus.add_document(Document("T1", "A1", "D1", "U1", "Machine learning is great."))
        self.corpus.add_document(Document("T2", "A2", "D2", "U2", "Deep learning is also learning."))

        vocab = self.corpus.vocab
        self.assertIsInstance(vocab, dict)
        self.assertIn("learning", vocab)
        self.assertIn("machine", vocab)
        self.assertIn("deep", vocab)

        self.assertEqual(vocab["learning"]["term_frequency"], 3)
        self.assertEqual(vocab["learning"]["document_frequency"], 2)
        self.assertEqual(vocab["deep"]["term_frequency"], 1)
        self.assertEqual(vocab["deep"]["document_frequency"], 1)

        freq_df = self.corpus.freq
        self.assertIsInstance(freq_df, pd.DataFrame)
        self.assertIn("term frequency", freq_df.columns)
        self.assertIn("document frequency", freq_df.columns)
        self.assertEqual(freq_df.index[0], "learning")

    def test_sparse_matrices_tf_and_tfidf(self):
        """Matrices creuses TF et TF-IDF."""
        self.corpus.add_document(Document("T1", "A1", "D1", "U1", "Neural network algorithms."))
        self.corpus.add_document(Document("T2", "A2", "D2", "U2", "Convolutional neural network."))

        mat_tf = self.corpus.mat_TF
        mat_tfidf = self.corpus.mat_TFxIDF

        self.assertIsInstance(mat_tf, csr_matrix)
        self.assertIsInstance(mat_tfidf, csr_matrix)
        self.assertEqual(mat_tf.shape, (2, len(self.corpus.vocab)))
        self.assertEqual(mat_tfidf.shape, (2, len(self.corpus.vocab)))
        self.assertGreater(mat_tf.nnz, 0)
        self.assertGreater(mat_tfidf.nnz, 0)

    def test_stats_and_repr_and_display(self):
        """Statistiques, __repr__ et affichage."""
        self.corpus.add_document(Document("Doc A", "Author A", "2020-01-01", "urlA", "Short test text."))
        self.corpus.add_document(Document("Doc B", "Author B", "2021-01-01", "urlB", "Another test text."))

        self.assertIn("Corpus 'Corpus for SearchEngine' with 2 documents", repr(self.corpus))

        stats_df = self.corpus.stats(n=5)
        self.assertIsInstance(stats_df, pd.DataFrame)
        self.corpus.display(n=2)


if __name__ == "__main__":
    unittest.main()
