from bs4 import BeautifulSoup
from configparser import ConfigParser
from googletrans import Translator
from tqdm import tqdm
import pandas as pd
import requests
import re


class FinancialScrapper:
    """Class for scrapping investfunds.ru site """
    def __init__(self, chip_name: str = 'decoy', config_path: str = 'config/cnf.ini'):
        """
        Construct all the necessary attributes for the parsing.

        :param config_path: path to the config file with urls
        :param chip_name: name of interested stock
        """
        conf = ConfigParser()
        conf.read(config_path)
        conf_select = conf['website_url']
        self.prices_df = []
        self.translator = Translator()
        self.chip_name = chip_name
        self.chip_link = ''
        self.base_url = conf_select['base_url']
        self.blue_chips_url = conf_select['blue_chips_url']
        self.usr_agent_key = conf_select['usr_agent_key']
        self.usr_agent_value = conf_select['usr_agent_value']
        self.chips_links = {}
        self.chip_news = {}

    def get_chips_links(self, for_landing: bool = False) -> dict:
        """
        Returns blue chips links from 'investfunds.ru'.

        :param for_landing: if True then form pd.Dataframe with unique stock names
        :return: dict with blue chips names as keys and their links as values
        """
        chips_links = {}
        # Request to site
        response = requests.get(self.blue_chips_url, headers={self.usr_agent_key: self.usr_agent_value})
        # Scrap html using bs4
        html = BeautifulSoup(response.text, 'lxml')
        # Retrieve specific tags
        raw_chips = html.find('tbody')
        hyperlinks_to_chips = raw_chips.find_all('a')
        # Clean chip name using regular expression
        for link in tqdm(hyperlinks_to_chips, desc='Scrapping chip links'):
            chip_name = (re.sub(r',.*', "", link.text))
            chip_name = self.translator.translate(chip_name).text
            chips_links[chip_name] = (self.base_url + link.get('href'))
        # Save result to class argument
        self.chips_links = chips_links
        if for_landing:
            return pd.DataFrame({'Stock': list(chips_links.keys())}, index=range(1, 16))
        return chips_links

    def get_chip_news(self) -> list:
        """
        Scrap blue chips news and collect them.

        :return: dict with blue chip names as key and dict with its Dates & Titles of news as values:
                 {'chip_name': {'Dates': [Date1, Date2..], 'Titles': [Title1, Title2..]}
        """
        chip_news = []
        # Collect chips links
        link = self.get_chips_links()[self.chip_name]
        self.chip_link = link
        # Scrap blue chip news info from their links
        # Request to site
        response = requests.get(link, headers={self.usr_agent_key: self.usr_agent_value})
        # Parse html with bs4
        html = BeautifulSoup(response.text, 'lxml')
        # Find specific tags in html
        raw_news = html.find('ul', class_='newsList')
        all_items = raw_news.find_all('li')
        # Collect news titles and dates
        for item in all_items:
            # Clean news titles & dates
            date = item.find('span').text.replace('|', '')
            title = item.find('b').text
            # Set translator
            trans_date = self.translator.translate(date).text
            trans_title = self.translator.translate(title).text
            trans_chip = self.translator.translate(self.chip_name).text
            # Add data to list with chips data
            chip_news.append([trans_chip, trans_date, trans_title])
        # Save result to class argument
        self.chip_news = chip_news
        return chip_news

    def get_chip_price(self) -> pd.DataFrame:
        """
        Scrap stock closing price with dates

        :return: pd.DataFrame with stock closing prices and dates marks of the last 30 days
        """
        response = requests.get(self.chips_links[self.chip_name], headers={self.usr_agent_key: self.usr_agent_value})
        html = BeautifulSoup(response.text, 'lxml')
        # First scrap dates
        raw_news = html.find('tbody').get_text()
        # Clean dates from redundant symbols
        dates_list = raw_news.split(" \n\n\n ")
        # Delete 'today' price because it is ambiguous
        del dates_list[0]
        # Filter dates ascending
        dates_list = dates_list[::-1]
        # Clean first date from redundant symbols
        dates_list[0] = re.sub(r'[^0-9.]', "", dates_list[0])
        # Scrap stock price
        prices_info = html.find_all('td', class_='field_legal_close_price')
        # Delete 'today' price because it is ambiguous
        del prices_info[0]
        prices = []
        for price_string in prices_info:
            noise_price = price_string.get_text()
            # Use regular expression for cleaning str
            price = re.sub(r'[^0-9]', "", noise_price)
            prices.append(int(price))
        # Filter prices due to dates
        prices = prices[::-1]
        # Concat 2 lists into pd.DataFrame
        zip_lists = list(zip(dates_list, prices))
        price_df = pd.DataFrame(zip_lists, columns=['Date', 'Stock_Price_Rub'])
        # Convert date column to datetime format
        price_df.Date = pd.to_datetime(price_df.Date, dayfirst=True)
        # Mark pennies
        price_df.Stock_Price_Rub = price_df.Stock_Price_Rub / 100
        self.prices_df = price_df
        return price_df
