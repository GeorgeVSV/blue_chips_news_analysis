import json
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

file_jsn = open('result.json')
chips = json.load(file_jsn)


s = pd.DataFrame(chips, columns=['Stock', 'Date', 'Title'])
vader = SentimentIntensityAnalyzer()


scores = s['Title'].apply(vader.polarity_scores).tolist()
# Convert the 'scores' list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)
# Join the DataFrames of the news and the list of dicts
parsed_and_scored_news = s.join(scores_df, rsuffix='_right')
parsed_and_scored_news.Date = pd.to_datetime(parsed_and_scored_news.Date, infer_datetime_format=True)

mean_scores = parsed_and_scored_news.groupby(['Stock', 'Date']).mean()
# Unstack the column ticker
mean_scores = mean_scores.unstack()
# Get the cross-section of compound in the 'columns' axis

mean_scores = mean_scores.xs('compound', axis="columns").transpose()

# Let's make average on month
avg_month = mean_scores.groupby(pd.Grouper(freq='W')).mean()
avg_month = avg_month[avg_month != 0]
avg_month = avg_month.dropna(axis=0, how='all')
# Switch off second mins and hours to make plot more convinient to analyse
avg_month = avg_month.set_index(avg_month.reset_index().Date.apply(lambda t: t.strftime('%Y-%m-%d')))



interese_stock = ['Gazprom', 'Novatek', 'Lukoil']

avg_month[interese_stock].plot(kind= 'bar')

plt.grid()
plt.rcParams['figure.figsize'] = [10, 6]
ax = plt.gca()
plt.legend(bbox_to_anchor=(1.1, 1.1), bbox_transform=ax.transAxes)
plt.show()
