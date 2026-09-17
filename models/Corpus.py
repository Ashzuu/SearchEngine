from services.helpers.Singleton import singleton


@singleton
@classmethod
class Corpus:
    """
    Corpus class which represents all documents referenced
    """
    __name:str
    __documents:list
    __nb_docs:int
    __author:dict