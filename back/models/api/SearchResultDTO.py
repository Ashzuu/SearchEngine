from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    Class to represent search result
    """
    query: str
    count: int
    result: dict

    def __init__(self, query, count, result):
        """
        Constructor for SearchResult class
        :param query: The query to search for
        :param count: The count of documents to return
        :param result: Documents resulting of the search
        """
        self.query = query
        self.count = count
        self.result = result