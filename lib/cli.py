#!/usr/bin/env python3
from helpers import exit_program
from helpers_customer import customer_menu
from helpers_vehicle import vehicle_menu
from helpers_service import service_add

def main_menu():
    while True:
        print("********************************************")
        print("***************** Main Menu ****************")
        print("********************************************")
        print("1. Customer Management")
        print("2. Vehicle Management")
        print("3. Add Service Record")
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
    print(' ')
    print('Welcome to Lube Lab Express, the quickest & easiest oil change shop on Python')
    print(' ')
    main_menu()