#!/usr/bin/env python3

# from helpers import (
#     exit_program, 
#     list_customers
# )
# from models.customer import Customer
# from models.vehicle import Vehicle
# from models.service import Service

from helpers import exit_program
from helpers_customer import customer_menu


def vehicle_menu():
    pass
def service_add():
    pass

def main_menu():
    while True:
        print("********************************************")
        print("***************** Main Menu ****************")
        print("********************************************")
        print("1. Customer Management")
        print("2. Vehicle Management")
        print("3. Add Service Ticket")
        print("x. Exit the program")
        
        main_menu_choice = input("> ")
        if main_menu_choice == "1":
            customer_menu()
        elif main_menu_choice == "2":
            vehicle_menu()
        elif main_menu_choice == "3":
            service_add()
        elif main_menu_choice.lower() == "x":
            exit_program()
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_menu()