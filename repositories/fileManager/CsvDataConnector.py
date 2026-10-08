import os
import pandas as pd
from repositories.fileManager.interfaces.DataConnectorInterface import DataConnectorInterface


class CsvDataConnector(DataConnectorInterface):
    """
    Constructor for the DataWriter class.
    """

    __filePath: str = "data/data.csv"
    __data: list

    def __init__(self) -> None:
        """
        Constructor for the CsvDataConnector class, to initialize the data file if not exists.
        """
        os.makedirs(os.path.dirname(self.__filePath), exist_ok=True)


    def write(self, data: list) -> None:
        """
        Method to write data to csv file
        :param data:
        :return:
        """
        df = pd.DataFrame(data)
        df.to_csv(self.__filePath, sep='\t', index=False)

    def read(self) -> list:
        """
        Read data from csv file
        """
        df = pd.read_csv(self.__filePath, sep='\t')
        df = df.fillna('')
        return df.to_dict('records')