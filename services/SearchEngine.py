from data.InitializerData import InitializerData


class SearchEngine:
    """
    The shell of the Search Engine, which manages logic.
    """
    _initializr:InitializerData = InitializerData()

    def __init__(self):
        self._initializr = InitializerData()

    def search(self, query: str):
        """
        Perform a search query.
        :param query: The query to search.
        :return: Dummy search results for now.
        """
        return []
