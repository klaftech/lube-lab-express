#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service

def build_tables():
    Customer.drop_table()
    Customer.create_table()
    Vehicle.drop_table()
    Vehicle.create_table()
    Service.drop_table()
    Service.create_table()

def seed_database():
    build_tables()
    print("tables have been reset")

    # seed customers
    customer_1 = Customer.create("George McMaster", "123 Sesame St")
    customer_2 = Customer.create("Harvey Limm", "455 Main St")
    customer_3 = Customer.create("John Doe", "5000 Dunn Blvd")
    print("Customers seeded")
    
    # seed vehicles
    vehicle_1 = Vehicle.create(customer_1.id, "Toyota", "Camry", 2025, "ABC123")
    vehicle_2 = Vehicle.create(customer_1.id, "Honda", "Civic", 2021, "DO82SK")
    vehicle_3 = Vehicle.create(customer_2.id, "Toyota", "Tundra", 2019, "CAT84BB")
    vehicle_4 = Vehicle.create(customer_3.id, "Rolls Royce", "Phantom", 2024, "VIP")
    vehicle_5 = Vehicle.create(customer_3.id, "Porsche", "Cayenne", 2024, "MYCAR1")
    print("Vehicles seeded")

    # seed services
    service_1 = Service.create(vehicle_1.id, 20000, '01-03-2024')
    service_2 = Service.create(vehicle_1.id, 24000, '04-12-2024')
    service_3 = Service.create(vehicle_1.id, 28000, '06-19-2024')
    service_4 = Service.create(vehicle_2.id, 12038, '09-28-2024')
    service_5 = Service.create(vehicle_2.id, 17494, '10-02-2024')
    service_6 = Service.create(vehicle_4.id, 83928, '05-12-2024')
    service_7 = Service.create(vehicle_4.id, 90283, '09-10-2024')
    service_8 = Service.create(vehicle_4.id, 93029, '04-21-2024')
    service_9 = Service.create(vehicle_5.id, 4028, '01-22-2024')
    service_10 = Service.create(vehicle_5.id, 6034, '09-03-2024')
    print("Services seeded")


seed_database()
print("Seeded database")    