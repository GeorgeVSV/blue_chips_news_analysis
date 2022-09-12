
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from scrap import FinScrap
import plotly.express as px


class SentimentProcessing:
    def __init__(self):
        scraper = FinScrap()
        df_dict = scraper.get_chips_news()
        self.df_chips = pd.DataFrame(df_dict, columns=['Stock', 'Date', 'Title'])
        self.data_for_visual = []

    def score_news_polarity(self) -> pd.DataFrame:
        """
        Calculate polarity scores of news and parse the data in appropriate format for visualization

        :return: pd.DataFrame with polairty scores for all blue chips with separation based on days
        """
        vader = SentimentIntensityAnalyzer()
        scores = self.df_chips['Title'].apply(vader.polarity_scores).tolist()
        # Convert the 'scores' list of dicts into a DataFrame
        scores_df = pd.DataFrame(scores)
        # Join the DataFrames of the news and the list of dicts
        parsed_and_scored_news = scores_df.join(scores_df, rsuffix='_right')
        parsed_and_scored_news.Date = pd.to_datetime(parsed_and_scored_news.Date, dayfirst=True)
        # Group polarity score by Stock name and date
        mean_scores = parsed_and_scored_news.groupby(['Stock', 'Date']).mean()
        # Unstack the column 'stock'
        mean_scores = mean_scores.unstack()
        # Get the cross-section of compound in the 'columns' axis
        mean_scores = mean_scores.xs('compound', axis="columns").transpose()
        self.data_for_visual = mean_scores
        return mean_scores

    def plot_daily_news(self, chip_name: str):

        interested_stock = [chip_name]
        stock_news = self.data_for_visual[interested_stock].dropna()
        fig = px.bar(stock_news, x=stock_news.index, y=interested_stock[0],
               title=stock_news.columns[0] + ' Daily Sentiment Scores')
        fig.update_layout(yaxis={'visible': True, 'showticklabels': True})
        fig.show()

v = SentimentProcessing()
v.plot_daily_news('Polymetal International')