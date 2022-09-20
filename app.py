import flask
import plotly
import json
from flask import Flask, render_template
from sentiment_analyser import SentimentProcessing
from scrap import FinScrap


app = Flask(__name__)


@app.route('/')
def index():
    scrapper = FinScrap()
    parsed_stocks = scrapper.get_chips_links(for_landing=True)
    return render_template('index.html', table=parsed_stocks.to_html(classes='data'))


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
    # Make plotly chart with daily stock closing price
    fig_daily_price = parsed_news.plot_price()
    # Encode plotly chart into JSON formatted object
    graph_json_daily_price = json.dumps(fig_daily_price, cls=plotly.utils.PlotlyJSONEncoder)
    # Text for header of sentiment page
    header = "{}".format(chip_name)
    return render_template('sentiment.html', graphJSON_daily=graph_json_daily,
                           graphJSON_daily_price=graph_json_daily_price, header=header,
                           table=parsed_score_news.to_html(classes='data'))


if __name__ == '__main__':
    app.debug = True
    app.run()
