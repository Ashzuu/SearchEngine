import os
import unittest
import tempfile
import pandas as pd
from repositories.fileManager.interfaces.DataConnectorInterface import DataConnectorInterface
from repositories.fileManager.CsvDataConnector import CsvDataConnector
from models.api.SearchResultDTO import SearchResult
from models.api.StatDTO import StatDTO
from services.helpers.Singleton import singleton


class TestDataConnectorsAndDTO(unittest.TestCase):
    """
    Tests unitaires pour les connecteurs de donnees, DTOs et le patron Singleton.
    """

    def test_singleton_decorator(self):
        """Test du decorateur singleton sur une classe generique."""
        @singleton
        class TestService:
            def __init__(self, value=1):
                self.value = value

        instance1 = TestService(10)
        instance2 = TestService(20)

        self.assertIs(instance1, instance2)
        self.assertEqual(instance1.value, 10)
        self.assertEqual(instance2.value, 10)

    def test_csv_data_connector_implements_interface(self):
        connector = CsvDataConnector()
        self.assertIsInstance(connector, DataConnectorInterface)

    def test_csv_data_connector_read_and_write(self):
        """Test d'ecriture et lecture via CsvDataConnector avec separateur tabulation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, "test_data.csv")

            connector = CsvDataConnector()
            # On remplace temporairement le chemin prive pour le test
            original_path = getattr(connector, "_CsvDataConnector__filePath")
            setattr(connector, "_CsvDataConnector__filePath", temp_file)

            try:
                sample_data = [
                    {
                        "id": 0,
                        "title": "Title 1",
                        "author": "Author 1",
                        "date": "2022",
                        "url": "http://example.com/1",
                        "text": "Sample text one",
                        "comments": 5,
                        "origin": "reddit"
                    },
                    {
                        "id": 1,
                        "title": "Title 2",
                        "author": "Author 2",
                        "date": "2023",
                        "url": "http://example.com/2",
                        "text": "Sample text two",
                        "comments": "",
                        "origin": "arxiv"
                    }
                ]

                connector.write(sample_data)
                self.assertTrue(os.path.exists(temp_file))

                with open(temp_file, "r", encoding="utf-8") as f:
                    first_line = f.readline()
                    self.assertIn("\t", first_line)

                loaded_data = connector.read()
                self.assertEqual(len(loaded_data), 2)
                self.assertEqual(loaded_data[0]["title"], "Title 1")
                self.assertEqual(loaded_data[1]["author"], "Author 2")

            finally:
                setattr(connector, "_CsvDataConnector__filePath", original_path)

    def test_search_result_dto(self):
        dto = SearchResult(query="machine learning", count=2, result=[{"id": 0}, {"id": 1}])
        self.assertEqual(dto.query, "machine learning")
        self.assertEqual(dto.count, 2)
        self.assertEqual(len(dto.result), 2)

    def test_stat_dto(self):
        dto = StatDTO(top_unique_words=100, top_frequent_words={"learning": 50, "machine": 30})
        self.assertEqual(dto.topUniqueWord, 100)
        self.assertEqual(dto.topFrequentWord, {"learning": 50, "machine": 30})


if __name__ == "__main__":
    unittest.main()
