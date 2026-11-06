from fastapi import APIRouter, Query
from controllers.interface.IController import IController
from models.api.SearchResultDTO import SearchResult
from services.SearchEngine import SearchEngine


class SearchEngineController(IController):
    """
    Controleur des routes de recherche.
    """
    _router: APIRouter

    def __init__(self) -> None:
        self._router = APIRouter()
        self._search_engine = SearchEngine()
        self._init_router()

    def get_router(self) -> APIRouter:
        """
        Retourne le routeur FastAPI.
        """
        return self._router

    async def search(
        self,
        query: str = Query(..., description="Mots cles a rechercher"),
        top_n: int = Query(10, description="Nombre de resultats", ge=1)
    ) -> SearchResult:
        """
        Recherche vectorielle par similarite cosinus.
        """
        df_resultats = self._search_engine.search(query, top_n=top_n)
        resultats_liste = df_resultats.to_dict(orient="records")
        total_trouves = len(resultats_liste)

        reponse = SearchResult(query, total_trouves, resultats_liste)

        return reponse

    async def concorde(
        self,
        expression: str = Query(..., description="Expression pour le concordancier"),
        context_size: int = Query(30, description="Taille du contexte", ge=1)
    ) -> SearchResult:
        """
        Recherche via un concordancier.
        """
        df_concorde = self._search_engine.concorde(expression, context_size=context_size)
        lignes = df_concorde.to_dict(orient="records")
        total_lignes = len(lignes)

        reponse = SearchResult(expression, total_lignes, lignes)

        return reponse

    async def stats(
        self,
        n: int = Query(10, description="Nombre de mots les plus frequents", ge=1)
    ) -> dict:
        """
        Retourne les statistiques textuelles du corpus.
        """
        df_freq = self._search_engine.stats(n=n)
        top_df = df_freq.head(n)
        top_mots = top_df.reset_index().to_dict(orient="records")
        total_vocabulaire = len(df_freq)

        reponse = {
            "total_unique_words": total_vocabulaire,
            "top_frequent_words": top_mots
        }
        return reponse

    def _init_router(self) -> None:
        """
        Enregistre les routes de l'API.
        """
        self._router.add_api_route("/search", self.search, methods=["GET"])
        self._router.add_api_route("/concorde", self.concorde, methods=["GET"])
        self._router.add_api_route("/stats", self.stats, methods=["GET"])
