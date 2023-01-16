## Web app for sentiment analysis of blue chips stock news

Homepage with a list of current blue chips of ru stock market

Web app  displays the daily  sentiments for a stock (user to insert stock name as input).

![image](https://user-images.githubusercontent.com/112613534/212647564-3e6e8df8-c507-495b-b60c-4595942f35fc.png)





Stock sentiments are determined from financial headlines scraped from the web

There are 2 graphs:

 > -The left graph shows daily sentiment score
  
 > -The right graph shows daily stock close price
    
Also in the bottom there is table with sentiment score for each news(with date and title)
    
![image](https://user-images.githubusercontent.com/112613534/212649296-bd3b82ee-e77c-4aa5-8f34-4dcd717ccf6c.png)

## Tech stack
1. Nltk (V.A.D.E.R. model) 
> "Valence Aware Dictionary for Sentiment Reasoning" is a model used for text sentiment analysis that is sensitive to both polarity (positive/negative) and intensity (strength) of emotion.
2. Bs4 
3. Flask
4. Visualization using plotly

## Requirements
 googletrans -> version 4.0.0c1, other may cause http errors.

## Installation
 1.   git clone https://github.com/GeorgeVSV/blue_chips_news_analysis.git
 2.   pip install -r requirements.txt
 
## Launch(on 5000 port)
    python app.py 
 
## Docker 
> Prepared dockerfile for local deployment of the app from docker container

