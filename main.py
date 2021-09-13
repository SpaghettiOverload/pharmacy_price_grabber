from tqdm import tqdm as progress_bar

from functions import validate_user_input, validate_user_quantity
from pharmacies_manager import PharmaciesManager


manager = PharmaciesManager()
manager.activate()

search_input = validate_user_input()
quantity = validate_user_quantity()

for pharmacy in progress_bar(manager.pharmacies):
    result = pharmacy.search_for(search_input)
    pharmacy.add_found(result)

manager.determine_best_price_and_pharmacy(quantity)
manager.print(search_input, quantity)
