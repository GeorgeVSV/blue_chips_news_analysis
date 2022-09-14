import flask
import plotly
import json
from flask import Flask, render_template
from sentiment_analyser import SentimentProcessing


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sentiment', methods=['POST'])
def sentiment():
    # Get chip name from user input
    chip_name = flask.request.form['chip']
    # Parsed news for interested chip
    parsed_news = SentimentProcessing(chip_name)
    # Calc news polarity score
    parsed_score_news = parsed_news.score_news_polarity()
    # Make plotly chart with daily polarity score distribution
    fig_daily = parsed_news.plot_daily_news()
    # Encode plotly chart into JSON formatted object
    graph_json_daily = json.dumps(fig_daily, cls=plotly.utils.PlotlyJSONEncoder)
    # Text for header of sentiment page
    header = "Daily Sentiment of {} Stock".format(chip_name)
    # Description with some details about graphs and stock's info
    description = """
    The above chart averages the sentiment daily scores of {} stock.
    The table below gives each of the most recent headlines of the stock and the negative, neutral, positive and an aggregated sentiment score.
    The news headlines are obtained from the investfunds website.
    Sentiments are given by the nltk.sentiment.vader Python library."""
    description = description.format(chip_name)
    return render_template('sentiment.html', graphJSON_daily=graph_json_daily, header=header,
                           table=parsed_score_news.to_html(classes='data'), description=description)


if __name__ == '__main__':
    app.debug = True
    app.run()
