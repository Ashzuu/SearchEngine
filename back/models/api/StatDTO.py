class StatDTO:
    """
    Class representing statistical data for a corpus
    """
    totalUniqueWord:int
    topFrequentWord:dict

    def __init__(self, top_unique_words: int, top_frequent_words: dict):
        self.topUniqueWord = top_unique_words
        self.topFrequentWord = top_frequent_words