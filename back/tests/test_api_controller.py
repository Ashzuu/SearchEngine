import unittest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from controllers.SearchEngineController import SearchEngineController
from models.Corpus import Corpus
from models.document.Document import Document


class TestApiController(unittest.TestCase):
    """
    Tests unitaires et d'integration pour le SearchEngineController et l'API FastAPI.
    """

    @classmethod
    def setUpClass(cls):
        corpus = Corpus()
        corpus.documents.clear()
        corpus.nb_docs = 0
        corpus.authors.clear()
        corpus._texte_concat = None
        corpus._vocab = None
        corpus._freq = None
        corpus._mat_TF = None
        corpus._mat_TFxIDF = None

        doc = Document(
            title="FastAPI Search Engine",
            author="Dev Author",
            date="2023-01-01",
            url="http://localhost",
            text="FastAPI makes high performance web APIs very simple and enjoyable."
        )
        corpus.add_document(doc)

        cls.controller = SearchEngineController()
        app = FastAPI()
        app.include_router(cls.controller.get_router())
        cls.client = TestClient(app)

    def test_search_endpoint_success(self):
        """Verifie que l'endpoint /search retourne un code 200 et la structure SearchResult."""
        response = self.client.get("/search?query=FastAPI&top_n=5")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("query", data)
        self.assertIn("count", data)
        self.assertIn("result", data)
        self.assertEqual(data["query"], "FastAPI")
        self.assertIsInstance(data["result"], list)

    def test_search_endpoint_missing_query(self):
        """Une requete /search sans le parametre obligatoire 'query' doit retourner un code 422."""
        response = self.client.get("/search")
        self.assertEqual(response.status_code, 422)

    def test_search_endpoint_invalid_top_n(self):
        """Le parametre top_n doit etre superieur ou egal a 1 (ge=1)."""
        response = self.client.get("/search?query=test&top_n=0")
        self.assertEqual(response.status_code, 422)

    def test_stats_endpoint_success(self):
        """Verifie que l'endpoint /stats retourne le nombre total de mots uniques et les plus frequents."""
        response = self.client.get("/stats?n=5")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("total_unique_words", data)
        self.assertIn("top_frequent_words", data)
        self.assertIsInstance(data["top_frequent_words"], list)
        self.assertIsInstance(data["total_unique_words"], int)

    def test_stats_endpoint_invalid_n(self):
        """Le parametre n doit etre superieur ou egal a 1."""
        response = self.client.get("/stats?n=-1")
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
