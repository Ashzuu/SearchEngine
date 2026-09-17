from abc import abstractmethod, ABC


class DataConnectorInterface(ABC):
    """
    Generic reader for data
    """
    @abstractmethod
    def read(self)->list:
        """Read data from a datasource"""

    @abstractmethod
    def write(self, data:list):
        """Persists data to a datasource"""