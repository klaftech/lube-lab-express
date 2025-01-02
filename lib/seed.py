#!/usr/bin/env python3
from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service

import random

from car_api import get_makes_and_models
vehicle_master = get_makes_and_models()

from faker import Faker
from faker.providers import DynamicProvider
from faker.providers import automotive
from faker.providers import date_time

car_make_provider = DynamicProvider(
     provider_name="car_make",
     elements=[f'{makes}' for makes in vehicle_master],
)
fake = Faker()
# then add new provider to faker instance
fake.add_provider(car_make_provider)

def rebuild_tables():
    Customer.drop_table()
    Vehicle.drop_table()
    Service.drop_table()
    print("database cleared")

    Customer.create_table()
    Vehicle.create_table()
    Service.create_table()
    print("tables have been reset")

def seed_database():
    rebuild_tables()
    
    for i in range(0,random.randint(5,20)):
        customer = Customer.create(fake.name(), fake.street_address())
        
        for i in range(0,random.randint(0,5)):
            car_make = fake.car_make()
            models_list = vehicle_master[car_make]
            choose_model = random.randint(0,len(models_list)-1)
            car_model = models_list[choose_model]

            vehicle = Vehicle.create(customer.id, car_make, car_model, int(fake.year()), fake.license_plate())
        
            for i in range(0,random.randint(0,10)):
                service = Service.create(vehicle.id, random.randint(10000,100000), fake.date("%m-%d-%Y"))

    print("Seeded database")   

#   def static_seed_database():
#     rebuild_tables()

#     # seed customers
#     customer_1 = Customer.create("George McMaster", "123 Sesame St")
#     customer_2 = Customer.create("Harvey Limm", "455 Main St")
#     customer_3 = Customer.create("John Doe", "5000 Dunn Blvd")
#     print("Customers seeded")
    
#     # seed vehicles
#     vehicle_1 = Vehicle.create(customer_1.id, "Toyota", "Camry", 2025, "ABC123")
#     vehicle_2 = Vehicle.create(customer_1.id, "Honda", "Civic", 2021, "DO82SK")
#     vehicle_3 = Vehicle.create(customer_2.id, "Toyota", "Tundra", 2019, "CAT84BB")
#     vehicle_4 = Vehicle.create(customer_3.id, "Rolls Royce", "Phantom", 2024, "VIP")
#     vehicle_5 = Vehicle.create(customer_3.id, "Porsche", "Cayenne", 2024, "MYCAR1")
#     print("Vehicles seeded")

#     # seed services
#     service_1 = Service.create(vehicle_1.id, 20000, '01-03-2024')
#     service_2 = Service.create(vehicle_1.id, 24000, '04-12-2024')
#     service_3 = Service.create(vehicle_1.id, 28000, '06-19-2024')
#     service_4 = Service.create(vehicle_2.id, 12038, '09-28-2024')
#     service_5 = Service.create(vehicle_2.id, 17494, '10-02-2024')
#     service_6 = Service.create(vehicle_4.id, 83928, '05-12-2024')
#     service_7 = Service.create(vehicle_4.id, 90283, '09-10-2024')
#     service_8 = Service.create(vehicle_4.id, 93029, '04-21-2024')
#     service_9 = Service.create(vehicle_5.id, 4028, '01-22-2024')
#     service_10 = Service.create(vehicle_5.id, 6034, '09-03-2024')
#     print("Services seeded")

seed_database() 