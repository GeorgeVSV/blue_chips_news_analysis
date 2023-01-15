## Web app for sentiment analysis of blue chips stock news

Homepage with a list of current blue chips of ru stock market

Web app  displays the daily  sentiments for a stock (user to enter stock name as input).

![image](https://user-images.githubusercontent.com/112613534/212565877-3c3bf2d6-4a36-4176-b5a5-11433212e77b.png)




Stock sentiments are determined from financial headlines scraped from the web

There are 2 graphs:

 > -The left graph shows daily sentiment score
  
 > -The right graph shows daily stock close price
    
Also in the bottom there is table with sentiment score for each news(with date and title)
    
![image](https://user-images.githubusercontent.com/112613534/212567683-d556396f-7219-43b1-8a0f-252c61a7e9e6.png)

## Tech stack
1. Nltk (V.A.D.E.R. model) 
> "Valence Aware Dictionary for Sentiment Reasoning" is a model used for text sentiment analysis that is sensitive to both polarity (positive/negative) and intensity (strength) of emotion.
2. Bs4 
3. Flask
4. Visualization using plotly

## Docker 
Prepared dockerfile for local deployment of the app from docker container

