from typing import List, Dict, NoReturn

import bs4
import cloudscraper
from bs4 import BeautifulSoup

from functions import clean_results


class Pharmacy:
    """
    This is a class defining the behavior of a particular Pharmacy.

    Attributes:

    - :class:`str` name --> The name of the Pharmacy.
    - :class:`str` search_address --> The base link, needed to access the particular pharmacy web-site search engine.
    - :class:`dict` delivery_terms --> A list containing the predefined prices for delivery + Free delivery threshold.
    - :class:`str` titles_grabber --> BeautifulSoup tag selectors needed to extract the title for each found product.
    - :class:`str` price_grabber --> BeautifulSoup tag selectors needed to extract the prices for a product found.
    - :class:`list` results_found --> Empty list at initialization to hold founded results for each valid query.

    Methods:

    - :class:`func` __get_url --> Method to create a complete URL by concatenating "search_address" + user's search query.
    - :class:`func` add_found --> Method to add found products to a Pharmacy's "results_found" list.
    - :class:`func` search_for --> Method responsible for the scraping, parsing and generating raw data.

    Properties:

    - :class:`func` stock --> Boolean returning whether Pharmacy's "results_found" list is empty or not.
    """

    def __init__(self, name: str, search_address: str, delivery_terms: dict,
                 titles_grabber: str, price_grabber: str) \
            -> NoReturn:
        self.name = name
        self.search_address = search_address
        self.delivery_terms = delivery_terms
        self.titles_grabber = titles_grabber
        self.price_grabber = price_grabber
        self.results_found: List = []

    def __get_url(self, search: str) -> str:
        return self.search_address + search

    def add_found(self, result: List[Dict]) -> NoReturn:
        self.results_found.extend(result)

    def search_for(self, search: str) -> List[Dict]:
        scraper = cloudscraper.create_scraper()
        url = self.__get_url(search)
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        raw_titles: bs4.element.ResultSet = soup.select(self.titles_grabber)
        raw_prices: List = [price.text for price in soup.select(self.price_grabber)]
        results: List[Dict] = clean_results(raw_titles, raw_prices, search)
        return results

    @property
    def stock(self) -> bool:
        return bool(self.results_found)
