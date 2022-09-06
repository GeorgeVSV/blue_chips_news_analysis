from bs4 import BeautifulSoup
from configparser import ConfigParser
from tqdm import tqdm
import requests
import re


class FinScrap:
    """Class for scrapping investfunds.ru site """
    def __init__(self, config_path: str = 'config/cnf.ini'):
        """
        Construct all the necessary attributes for the parsing.

        :param config_path: path to the config file with urls
        :type config_path: str
        """
        conf = ConfigParser()
        conf.read(config_path)
        conf_select = conf['website_url']
        self.base_url = conf_select['base_url']
        self.blue_chips_url = conf_select['blue_chips_url']
        self.usr_agent = conf_select['usr_agent']
        self.usr_agent1 = conf_select['usr_agent_1']
        self.chips_links = {}
        self.chip_news = {}

    def get_chips_links(self) -> dict:
        """
        Returns blue chips links from investfunds.ru.

        :return: dict with blue chips names as keys and their links as values
        """
        chips_links = {}
        # Request to site
        response = requests.get(self.blue_chips_url, headers={self.usr_agent: self.usr_agent1})
        # Scrap html using bs4
        html = BeautifulSoup(response.text, 'lxml')
        # Retrieve specific tags
        raw_chips = html.find('tbody')
        hyperlinks_to_chips = raw_chips.find_all('a')
        # Clean chip name using regula expression
        for link in tqdm(hyperlinks_to_chips, desc='Scrapping chip links'):
            chip_name = (re.sub(r',.*', "", link.text))
            chips_links[chip_name] = (self.base_url + link.get('href'))
        # Save result to class argument
        self.chips_links = chips_links
        return chips_links

    def scrap_chips_news(self) -> dict:
        """
        Scrap blue chips news and collect them.

        :return: dict with blue chips names as keys and dict with their Dates & Titles of news as values:
                 {'chip_name': {'Dates': [Date1, Date2..], 'Tiles': [Title1, Title2..]}
        """
        chip_news = {}
        # Scrap blue chips news info from their links
        for chip, chip_url in tqdm(self.chips_links.items(), desc='Scrapping chips'):
            # Create key in dict for each chip
            chip_news[chip] = {}
            chip_news[chip]['Dates'] = []
            chip_news[chip]['Titles'] = []
            # Request to site
            response = requests.get(chip_url, headers={self.usr_agent: self.usr_agent1})
            # Parse html with bs4
            html = BeautifulSoup(response.text, 'lxml')
            # Find specific tags in html
            raw_news = html.find('ul', class_='newsList')
            all_items = raw_news.find_all('li')
            # Collect news titles and dates
            for item in all_items:
                # Clean news titles
                date = item.find('span').text.replace('|', '')
                chip_news[chip]['Dates'].append(date)
                title = item.find('b').text
                chip_news[chip]['Titles'].append(title)
        # Save result to class argument
        self.chip_news = chip_news
        return chip_news
