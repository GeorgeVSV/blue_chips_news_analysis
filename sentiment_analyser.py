import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from scrap import FinScrap


class SentimentProcessing:
    def __init__(self):
        scraper = FinScrap()
        df_dict = scraper.get_chips_news()
        self.df_chips = pd.DataFrame(df_dict, columns=['Stock', 'Date', 'Title'])

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
        parsed_and_scored_news.Date = pd.to_datetime(parsed_and_scored_news.Date, infer_datetime_format=True)
        # Group polarit score by Stock name and date
        mean_scores = parsed_and_scored_news.groupby(['Stock', 'Date']).mean()
        # Unstack the column 'stock'
        mean_scores = mean_scores.unstack()
        # Get the cross-section of compound in the 'columns' axis
        mean_scores = mean_scores.xs('compound', axis="columns").transpose()
        return mean_scores


# Time period selection for plotting
'''
# Let's make average on month
avg_month = mean_scores.groupby(pd.Grouper(freq='W')).mean()
avg_month = avg_month[avg_month != 0]
avg_month = avg_month.dropna(axis=0, how='all')
# Switch off second mins and hours to make plot more convinient to analyse
avg_month = avg_month.set_index(avg_month.reset_index().Date.apply(lambda t: t.strftime('%Y-%m-%d')))






# Plot graphs
matplotlib.use('TkAgg')
interese_stock = ['Gazprom', 'Novatek', 'Lukoil']

avg_month[interese_stock].plot(kind= 'bar')

plt.grid()
plt.rcParams['figure.figsize'] = [10, 6]
ax = plt.gca()
plt.legend(bbox_to_anchor=(1.1, 1.1), bbox_transform=ax.transAxes)
plt.show()
'''
