from fastapi import FastAPI

from controllers.SearchEngineController import SearchEngineController
from services.helpers.Singleton import singleton


@singleton
class Api:
    """
    Main class for the API.
    Is a singleton because we must have only one instance of the API.
    """
    _api: FastAPI
    _controllers:list = []

    @property
    def api(self):
        """
        Get the API reference of the object to construct it in the client
        :return: The reference of the API built.
        """
        return self._api

    def __init__(self):
        """
        Constructor for the API.
        """
        self._api = FastAPI(title="Search Engine")
        self._controllers.append(SearchEngineController())
        for controller in self._controllers:
            self._api.include_router(controller.get_router())