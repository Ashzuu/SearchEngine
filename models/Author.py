from dataclasses import dataclass


@dataclass
class Author:
    """
    Author class which represents an author of a document
    """
    __name:str
    __nb_docs:int
    __productions:dict