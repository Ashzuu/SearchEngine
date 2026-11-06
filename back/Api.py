from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.SearchEngineController import SearchEngineController
from services.factories.DocumentFactory import DocumentFactory
from services.helpers.Singleton import singleton
from data.InitializerData import InitializerData
from repositories.fileManager.CsvDataConnector import CsvDataConnector
from models.Corpus import Corpus


@singleton
class Api:
    """
    Application principale de l'API.
    """
    def __init__(self) -> None:
        self._api = FastAPI(title="Search Engine")
        self._controllers = []

        # Initialisation des donnees
        InitializerData()
        connector = CsvDataConnector()
        donnees = connector.read()

        # Remplissage du corpus
        corpus = Corpus()
        for ligne in donnees:
            document = DocumentFactory.create(ligne)
            corpus.add_document(document)

        print(corpus)

        # Enregistrement des controleurs
        controller = SearchEngineController()
        self._controllers.append(controller)
        router = controller.get_router()
        self._api.include_router(router)

        self._api.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:4200"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @property
    def api(self) -> FastAPI:
        """
        Retourne l'instance FastAPI.
        """
        return self._api
