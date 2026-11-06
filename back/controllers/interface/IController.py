from abc import abstractmethod, ABC
from fastapi import APIRouter

class IController(ABC):
    @abstractmethod
    def get_router(self) -> APIRouter:
        pass