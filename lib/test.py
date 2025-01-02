import ipdb

from __init__ import CONN, CURSOR
from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service

#import vehicle_makes
# from vehicle_makes import get_makes_and_models
# print(get_makes_and_models())

import requests
from car_api import get_makes_and_models


print(get_makes_and_models())
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }

# _BASE_URI = 'https://www.autotrader.co.uk'

# url = f'{_BASE_URI}/json/search/options?advertising-location=at_cars'
# resp = requests.get(url, headers=headers)
# print(resp)
#build_tables()
#print("tables have been reset")

# Create seed data
#customer_1 = Customer.create("George McMaster", "123 Sesame St")
#vehicle_1 = Vehicle.create("Toyota", "Camry", 2025, "ABC123", customer_1)





ipdb.set_trace()