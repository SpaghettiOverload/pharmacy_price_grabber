from tqdm import tqdm as progress_bar

from functions import validate_user_input, validate_user_quantity
from driver import Driver


driver = Driver()
driver.activate()

search_input = validate_user_input()
quantity = validate_user_quantity()

for pharmacy in progress_bar(driver.pharmacies):
    result = pharmacy.search_for(search_input)
    pharmacy.add_found(result)

driver.determine_best_price_and_pharmacy(quantity)
driver.print(search_input, quantity)  # Printing results from within print function.
