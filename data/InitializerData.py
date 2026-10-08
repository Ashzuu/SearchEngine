import praw
import pandas as pd
import requests
import xmltodict
from repositories.fileManager.CsvDataConnector import CsvDataConnector

class InitializerData:
    """
    Initialize of data if data.csv is empty
    """
    __LIMIT: int = 250
    __THEME: str = "Machine Learning"
    __THEME_REDDIT: str = "MachineLearning"

    __dataReddit:list = []
    __dataArvix:list = []

    __writer: CsvDataConnector = CsvDataConnector()

    @property
    def dataReddit(self):
        """
        Get data of reddit extracted on initialization.
        """
        return self.__dataReddit

    @property
    def dataArvix(self):
        """
        Get data of arvix extracted on initialization.
        :return:
        """
        return self.__dataArvix

    def __init__(self):
        """
        Initialize of data if data.csv is empty.
        """
        try:
            data = self.__writer.read()
            if not data:
                self.__initialize_and_save()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.__initialize_and_save()

    def __initialize_and_save(self):
        self.__initRedditData()
        self.__initArvixData()
        
        all_data = self.__dataReddit + self.__dataArvix
        if all_data:
            self.__writer.write(all_data)

    def __initRedditData(self)->None:
        """
        Initialize data of reddit with the chosen theme.
        """
        redditClient = praw.Reddit(
            client_id="m4W3R1MLvrnNI9LTbG35Eg",
            client_secret="ynb_xt5pKo4IFhssuuqr5ENTMu5Q4g",
            user_agent="Evan_M1",
        )
        redditClientThemed:list = redditClient.subreddit(self.__THEME_REDDIT)
        listOfPosts:list = list(redditClientThemed.hot(limit=self.__LIMIT))
        for post in listOfPosts:
            # Instead of that, use a factory to make reddit post instead of writing hand.
            text: str = ""
            text+=post.title.replace("\n", " ") + ". "
            if post.selftext:
                text += post.selftext.replace("\n", " ")
            elif post.url:
                text += post.url

            data = {
                'id': len(self.__dataReddit),
                'text': text,
                'origin': 'reddit'
            }

            self.__dataReddit.append(data)

    def __initArvixData(self)->None:
        """
        Initialize data of arvix with the chosen theme.
        """
        url = f"http://export.arxiv.org/api/query?search_query=all:{self.__THEME.replace(' ', '+')}&start=0&max_results={self.__LIMIT}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = xmltodict.parse(response.text)
                entries = data.get('feed', {}).get('entry', [])
                if not isinstance(entries, list):
                    entries = [entries]
                for entry in entries:
                    title = entry.get('title', '').replace('\n', ' ')
                    summary = entry.get('summary', '').replace('\n', ' ')
                    text = f"{title}. {summary}"
                    
                    doc = {
                        'id': len(self.__dataReddit) + len(self.__dataArvix),
                        'text': text,
                        'origin': 'arxiv'
                    }
                    self.__dataArvix.append(doc)
        except Exception as e:
            print(f"Error fetching Arxiv data: {e}")