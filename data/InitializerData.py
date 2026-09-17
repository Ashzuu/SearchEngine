import praw
from repositories.fileManager.CsvDataConnector import CsvDataConnector

class InitializerData:
    """
    Initialize of data if data.csv is empty
    """
    __LIMIT: int = 10
    __THEME: str = "MachineLearning"

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
        self.__initRedditData()
        self.__initArvixData()

    def __initRedditData(self)->None:
        """
        Initialize data of reddit with the chosen theme.
        """
        redditClient = praw.Reddit(
            client_id="m4W3R1MLvrnNI9LTbG35Eg",
            client_secret="ynb_xt5pKo4IFhssuuqr5ENTMu5Q4g",
            user_agent="Evan_M1",
        )
        redditClientThemed:list = redditClient.subreddit(self.__THEME)
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
        pass