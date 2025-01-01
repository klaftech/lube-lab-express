#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service

def dump_customer_database():
    print("Dumping Customer Database")
    for i in Customer.get_all():
        print(i)

def dump_vehicle_database():
    print("Dumping Vehicle Database")
    for i in Vehicle.get_all():
        print(i)

def dump_service_database():
    print("Dumping Service Database")
    for i in Service.get_all():
        print(i)

dump_customer_database()
dump_vehicle_database()
dump_service_database()