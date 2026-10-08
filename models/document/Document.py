from dataclasses import dataclass

@dataclass
class Document:
    """
    Representing a generic Document object.
    """
    title: str
    author: str
    date: str
    url: str
    text: str

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
    
    def getType(self) -> str:
        return "generic"