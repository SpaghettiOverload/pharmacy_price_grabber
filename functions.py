from typing import List, Dict, Tuple
import re
import bs4


def clean_results(raw_titles: bs4.element.ResultSet, raw_prices: list, search: str) -> List[Dict]:
    """
    Function to process raw data to meaningful values to work with.

    :param raw_titles: BeautifulSoup set of parsed results to be processed.
    :param raw_prices: BeautifulSoup list of parsed results to be processed.
    :param search: User's search query. Passed to this function to check against results and minimize irrelevancy.
    :return: List with dictionaries, each representing an item found. List is sorted by price in ascending order.
    """

    results: List[Dict] = list()
    for index, result in enumerate(raw_titles):
        item_title = result.text.strip()
        if search.upper() not in item_title.upper():  # Minimizing irrelevant results. TROUBLESOME!,
            continue                                  # more complex filtering or multi-word searches greatly limit results.
        promotion, price, promotional_price = get_prices(raw_prices[index])
        results.append({
            "Name": item_title,
            "Promotion": promotion,
            "Price": price,
            "Promotional price": promotional_price
        })
    sorted_results = sorted(results, key=lambda x: x["Price"])
    return sorted_results


def get_prices(x: str) -> Tuple[bool, float, float]:
    """
    Function to process raw prices and convert them from strings to float.

    :param x: BeautifulSoup string which holds pricing data.
    :return: Tuple of three values: Bool and two Float prices.
    """

    prices = x.replace("лв", " ").split()
    caught_prices: List = list()

    for value in prices:
        if "," in value:
            value = value.replace(",", ".")
        try:
            price = float(value)
            caught_prices.append(price)
        except ValueError:
            continue

    promotion = True if len(caught_prices) > 1 else False
    if promotion:
        caught_prices: sorted(List) = sorted(caught_prices)
        promotional_price, price = caught_prices
    else:
        promotional_price, price = 0.00, caught_prices[0]
    return promotion, price, promotional_price


def validate_user_quantity() -> int:
    """
    Function to validate the quantity for the product search is always a whole number.

    :return: int if the input is valid else continues to ask for an input
    """

    while True:
        quantity = input("Количество: ")
        try:
            return int(quantity)
        except ValueError:
            print("Невалидно количество, моля въведете цяло число!")


def validate_user_input() -> str:
    """
    Function to validate the searched product string contains allowed characters with a simple Regex.

    REGEX PATTERN: No empty string (But can contain spaces between words).
    Starting with OR be at least 3 letters long.
    If longer, can contain any count of letters, numbers, spaces, "_", "%" and "." symbols afterwards.
    It provides basic and loose validation on purpose, considering the wide range of product titles.

    :return: str (if the input is valid)
    """

    while True:
        search_input = input("Търсене за: ")
        if re.match(r"^[а-яА-Яa-zA-Z]{3,}[\w%. ]*$", search_input):
            return search_input
        print("Непозволени символи, моля опитайте отново!")
