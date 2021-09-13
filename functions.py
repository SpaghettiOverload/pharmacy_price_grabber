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

    results: List[Dict] = list()  # Creating an empty list to hold dictionary values.
    for index, result in enumerate(raw_titles):  # Iterating over each result, while keep track on indexing.
        item_title = result.text.strip()
        if search.upper() not in item_title.upper():  # Minimizing irrelevant results. TROUBLESOME!,
            continue                                  # more complex filtering or multi-word searches greatly limit results.
        promotion, price, promotional_price = get_prices(raw_prices[index])  # Passing raw price data to a function for processing.
        results.append({  # Creating a dict to hold the processed data of the current result and adds it to the "results" list.
            "Name": item_title,
            "Promotion": promotion,
            "Price": price,
            "Promotional price": promotional_price
        })
    sorted_results = sorted(results, key=lambda x: x["Price"])  # Sorting final list by the "Price" value of each dict.
    return sorted_results


def get_prices(x: str) -> Tuple[bool, float, float]:
    """
    Function to process raw pricing and convert it from string to float.

    :param x: BeautifulSoup string which holds pricing data.
    :return: Tuple of three values: Bool and two Float prices.
    """

    prices = x.replace("лв", " ").split()  # Replacing (if present) "лв" with space,
    # to ensure there will always be a properly split list and a number alone,
    # e.g. "xx 9.99лв xx" won't split properly,
    # while "xx 9.99  xx" will gives us "clean" string value of "9.99" to operate with.

    caught_prices: List = list()
    for value in prices:  # For each split value,

        if "," in value:
            value = value.replace(',', '.')  # replacing (if present) decimal points to ensure possible proper type cast,
            # from String to Float afterwards.
        try:
            price = float(value)  # Trying to cast "cleaned" String data to Float.
            caught_prices.append(price)  # Add it to the final results if successful.
            # The only failed casts will be the ones holding non-float/int values,
            # such as special characters and letters, left in the original prices list after the splitting.
            # This way they drop-out at this point.
        except ValueError:
            continue  # Move to the next split value if the cast were unsuccessful.

    promotion = True if len(caught_prices) > 1 else False  # If we caught 2 prices per certain result,
    # then there is an ongoing promotion for this product, thus we set "Promotion" Bool to True.

    if promotion:  # If promotional price were previously detected,
        caught_prices: sorted(List) = sorted(caught_prices)  # we assume the promotional price is always less in value,
        # therefore we sort the two prices inside the list by ascending order,
        promotional_price, price = caught_prices  # then unpack and assign them to their respective variables.
    else:
        promotional_price, price = 0.00, caught_prices[0]  # Setting "promotional price" to a zero Float value,
        # if there were no promotion for this product,
        # to ensure there is always correct amount of values to be returned from the function.
    return promotion, price, promotional_price


def validate_user_quantity() -> int:
    """
    Function to validate the quantity for the product search is always a whole number.

    :return: int (if the input is valid)
    """

    while True:  # We will keep asking for a whole number to be the input if other value is present.
        quantity = input("Количество: ")
        try:
            return int(quantity)  # Trying to cast the string value to int,
            # returns it if the cast is successful and terminates the loop.
        except ValueError:
            print("Невалидно количество, моля въведете цяло число!")  # If the cast is unsuccessful,
            # we print an error and continue the loop by asking for another input.


def validate_user_input() -> str:
    """
    Function to validate the searched product string contains allowed characters with a simple Regex.

    REGEX PATTERN: No empty string (But can contain spaces between words).
    Starting with OR be at least 3 letters long.
    If longer, can contain any count of letters, numbers, spaces, "_", "%" and "." symbols afterwards.
    It provides basic and loose validation on purpose, considering the wide range of product titles.

    :return: str (if the input is valid)
    """

    while True:  # We will keep asking for a valid input if invalid value is present.
        search_input = input("Търсене за: ")
        if re.match(r"^[а-яА-Яa-zA-Z]{3,}[\w%. ]*$", search_input):  # Trying to match the input value to the pattern,
            return search_input  # returns the input value if pass the validation and terminates the loop.
        print("Непозволени символи, моля опитайте отново!")  # If the cast is unsuccessful,
        # we print an error and continue the loop by asking for another input.
