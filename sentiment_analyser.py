import pandas as pd
import plotly.express as px
from nltk.sentiment import SentimentIntensityAnalyzer
from scrap import FinScrap


class SentimentProcessing:
    """Class for calculating polarity scores for news and visualization dynamic of their changing"""
    def __init__(self, stock: str):
        """
        :param stock: name of interested stock
        """
        self.chip_name = stock
        self.df_chip = pd.DataFrame
        self.parsed_news = pd.DataFrame

    def score_news_polarity(self) -> pd.DataFrame:
        """
        Calculate polarity scores of news and parse the data in appropriate format for visualization

        :return: pd.DataFrame with polarity scores for all blue chips with separation based on days
        """
        # Scrap news from investfunds.ru
        scraper = FinScrap(self.chip_name)
        df_dict = scraper.get_chip_news()
        # Make pandas dataframe from dict
        self.df_chip = pd.DataFrame(df_dict, columns=['Stock', 'Date', 'Title'])
        # Set sentiment analyser
        vader = SentimentIntensityAnalyzer()
        # Calc polarity score for each headline
        scores = self.df_chip['Title'].apply(vader.polarity_scores).tolist()
        # Convert the 'scores' list of dicts into a DataFrame
        scores_df = pd.DataFrame(scores)
        # Concat the DataFrames of the news and their polarity scores
        parsed_news = pd.concat([self.df_chip, scores_df.set_index(self.df_chip.index)], axis=1)
        parsed_news.Date = pd.to_datetime(parsed_news.Date, dayfirst=True)
        # Delete unnecessary column stock and correct index
        parsed_news = parsed_news.drop('Stock', axis=1).set_index([list(range(1, len(parsed_news)+1))])
        self.parsed_news = parsed_news
        return parsed_news

    def plot_daily_news(self):
        """
        Plot daily sentiment score for interested stock
        """
        fig = px.bar(self.parsed_news, x=self.parsed_news.Date, y=self.parsed_news.compound,
                     title=self.chip_name + ' Daily Sentiment Scores')
        fig.update_yaxes(title=None)
        # Return fig and then turn it into a graphjson object for displaying in web page later
        return fig

