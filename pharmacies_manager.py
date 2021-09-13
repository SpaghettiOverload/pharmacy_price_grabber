import sys
import json
from typing import NoReturn, List

from colorama import init, Fore, Style

from pharmacy import Pharmacy


class PharmaciesManager:
    """
    This is a driver class responsible for the start and final results printed of the program.

    Attributes:

    - :class:`list` __pharmacies --> An empty list to hold the Pharmacy class instances for all pharmacies in the DB.
    - :class:`num` __best_price --> Number representing the lowest price found after scraping.
    - :class:`str` __best_pharmacy --> The name of the best pharmacy based on __best_price.
    - :class:`str` __best_delivery --> Delivery rate used for calculation of best price only.

    Methods:

    - :class:`func` activate --> Fills the "__pharmacies" list with Pharmacy class instances for all pharmacies in the DB.
    - :class:`func` determine_best_price_and_pharmacy --> Calculates "__best_price" and "__best_pharmacy" attributes.
    - :class:`func` print --> Prints stylized results.

    Properties:

    - :class:`func` pharmacies --> Returns a list with all Pharmacy objects.
    """

    def __init__(self) -> NoReturn:
        self.__pharmacies: List[Pharmacy] = []
        self.__best_price = sys.maxsize
        self.__best_pharmacy = None
        self.__best_delivery = sys.maxsize
        init()  # Initializing "colorama" library in order to colorize the printed results.

    def activate(self) -> NoReturn:
        with open("pharmacies_data.json", encoding="utf8") as input_file:
            data = json.load(input_file)
            for pharmacy in data["Pharmacies"]:
                self.__pharmacies.append(Pharmacy(*pharmacy.values()))

    def determine_best_price_and_pharmacy(self, quantity: int) -> NoReturn:
        for pharmacy in self.pharmacies:
            if pharmacy.stock:
                if not pharmacy.results_found[0]["Promotion"]:
                    price = pharmacy.results_found[0]["Price"]
                else:
                    price = pharmacy.results_found[0]["Promotional price"]
                delivery_cost = pharmacy.delivery_terms["Delivery cost"] \
                    if price * quantity < pharmacy.delivery_terms["Free delivery threshold"] \
                    else 0.00

                if price + delivery_cost < self.__best_price + self.__best_delivery:
                    self.__best_price = price
                    self.__best_pharmacy = pharmacy.name
                    self.__best_delivery = delivery_cost

    def print(self, search_input: str, quantity: int) -> NoReturn:
        for pos, pharmacy in enumerate(self.pharmacies):
            delivery = f'{pharmacy.delivery_terms["Delivery cost"]:.2f}'
            free_delivery = f'{pharmacy.delivery_terms["Free delivery threshold"]:.2f}'

            print(f"\n{Fore.LIGHTCYAN_EX + f'({pos+1}) {pharmacy.name}'}{Style.RESET_ALL}:")
            print(f"{Fore.LIGHTBLACK_EX + f'Доставка: {delivery} лв  /  Безплатна над: {free_delivery} лв' + Style.RESET_ALL}")
            if pharmacy.stock:
                for stock in pharmacy.results_found:
                    print(stock["Name"], end=" // ")
                    price = stock["Price"]
                    promotional_price = stock["Promotional price"]
                    if promotional_price:
                        print(f"Цена: {price:.2f} лв/бр {Fore.RED + 'ПРОМОЦИЯ >> '}"
                              f"{Fore.LIGHTGREEN_EX + str(promotional_price)} лв/бр{Style.RESET_ALL}")
                        continue
                    print(f"Цена: {price:.2f} лв/бр" if price > 0
                          else f"{Fore.LIGHTBLACK_EX + 'НЯМА НАЛИЧНОСТ'}{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTBLACK_EX + 'НЯМА НАЛИЧНОСТ'}{Style.RESET_ALL}")

        if any([pharmacy.stock for pharmacy in self.pharmacies]):
            delivery = "БЕЗПЛАТНА" if not self.__best_delivery else f'{self.__best_delivery:.2f}'
            string = f"Най-добрата цена за: {quantity} бр {search_input.upper()} - e в аптека: {self.__best_pharmacy} " \
                     f"= {self.__best_price * quantity:.2f} лв + {delivery} доставка"
            print(f"\n{Fore.RED + string + Style.RESET_ALL}")

    @property
    def pharmacies(self) -> List:
        return self.__pharmacies
