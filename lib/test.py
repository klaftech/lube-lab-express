import ipdb

from __init__ import CONN, CURSOR
from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service

def build_tables():
    Customer.drop_table()
    Customer.create_table()
    Vehicle.drop_table()
    Vehicle.create_table()

#build_tables()
#print("tables have been reset")

# Create seed data
#customer_1 = Customer.create("George McMaster", "123 Sesame St")
#vehicle_1 = Vehicle.create("Toyota", "Camry", 2025, "ABC123", customer_1)





ipdb.set_trace()