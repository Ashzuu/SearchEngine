from fastapi import FastAPI
import json

from controllers.SearchEngineController import SearchEngineController
from services.factories.DocumentFactory import DocumentFactory
from services.helpers.Singleton import singleton
from data.InitializerData import InitializerData
from repositories.fileManager.CsvDataConnector import CsvDataConnector
from models.Corpus import Corpus
from models.document.RedditDocument import RedditDocument
from models.document.ArvixDocument import ArvixDocument


@singleton
class Api:
    """
    Main class for the API.
    Is a singleton because we must have only one instance of the API.
    """
    _api: FastAPI
    _controllers:list = []

    @property
    def api(self) -> FastAPI:
        """
        Get the API reference of the object to construct it in the client
        :return: The reference of the API built.
        """
        return self._api

    def __init__(self) -> None:
        """
        Constructor for the API.
        """
        self._api = FastAPI(title="Search Engine")
        
        InitializerData()
        corpus = Corpus()
        cached_data = CsvDataConnector().read()
        for row in cached_data:
            doc = DocumentFactory.create(row)
            corpus.add_document(doc)

        print(corpus)
                
        self._controllers.append(SearchEngineController())
        for controller in self._controllers:
            self._api.include_router(controller.get_router())