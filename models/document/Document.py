from dataclasses import dataclass


@dataclass
class Document:
    """
    Representing a generic Document object.
    """
    __title:str
    __author:str
    __date:str
    __url:str
    __text:str