from fastapi import FastAPI, APIRouter, Query
from controllers.interface.IController import IController
from services.SearchEngine import SearchEngine


class SearchEngineController(IController):
    """
    Controller to manage the search engine
    """
    _api: FastAPI
    _router: APIRouter

    def __init__(self) -> None:
        """
        Constructor for the Search Engine Controller
        """
        self._router = APIRouter()
        self._search_engine = SearchEngine()
        self._init_router()

    def get_router(self) -> APIRouter:
        """
        Get the router created by the controller
        :return: The router created
        """
        return self._router

    async def search(self, query: str = Query(..., description="The query to search in the search engine")) -> dict:
        """
        Search engine for query
        :param query: The query to search in the search engine
        :return: The result of the query
        """
        results = self._search_engine.search(query)
        return {"query": query, "results": results}

    def _init_router(self) -> None:
        """
        Init the router for the controller with all routes, and function which corresponds
        """
        self._router.add_api_route("/search", self.search, methods=["GET"])