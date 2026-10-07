from abc import abstractmethod, ABC


class IController(ABC):
    @abstractmethod
    def get_router(self):
        pass