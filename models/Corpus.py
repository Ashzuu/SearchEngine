from services.helpers.Singleton import singleton

@singleton
class Corpus:
    """
    Corpus class which represents all documents referenced
    """
    def __init__(self) -> None:
        self.name: str = "Corpus for SearchEngine"
        self.documents: dict = {}
        self.nb_docs: int = 0
        self.authors: dict = {}

    def add_document(self, doc) -> None:
        self.documents[self.nb_docs] = doc
        self.nb_docs += 1

    def __repr__(self) -> str:
        return f"Corpus '{self.name}' with {self.nb_docs} documents"
    
    def display(self, n: int = 5) -> None:
        sorted_docs = sorted(self.documents.values(), key=lambda x: (x.date, x.title))
        for doc in sorted_docs[:n]:
            print(doc)