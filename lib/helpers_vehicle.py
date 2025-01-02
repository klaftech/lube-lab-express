from models.vehicle import Vehicle
from helpers import exit_program

def vehicle_list_all():
    while True:
        vehicles = Vehicle.get_all()
        for vehicle in vehicles:
            print(vehicle)
        
        choice = input("Enter id to see details or Z to return ")
        if choice.lower() == "z":
            break
        else:
            vehicle = Vehicle.find_by_id(choice)
            if vehicle:
                vehicle_details(vehicle)
            else:
                print(' ')
                print(f'Vehicle #{choice} not found. ')
                print(' ')


def vehicle_find_by_plate():
    # TO DO: show matching results and allow selection by ID
    while True:
        plate = input("Enter the vehicle's license plate (Z to cancel): ")
        if plate.lower() == "z":
            break
        else:
            vehicle = Vehicle.find_by_plate(plate)
            print(vehicle) if vehicle else print(
                f'Vehicle with license plate "{plate}" not found')

def vehicle_add():
    import os
    from car_api import get_makes_and_models
    from simple_term_menu import TerminalMenu
    
    while True:
        customer_id = input("Enter owner's ID: ")
        # since we must convert inputs to integers before creating instance, must validate value
        if not customer_id:
            print("You must enter the owner's ID")
            continue
        
        print("Loading vehicle list...")
        vehicle_master = get_makes_and_models()
        vehicle_makes = [f'{makes}' for makes in vehicle_master]
        
        makes_menu = TerminalMenu(vehicle_makes, search_key=None, search_highlight_style=None, title="Vehicle Make")
        makes_menu_entry_index = makes_menu.show()
        make = makes_menu.chosen_menu_entry
        print(f'Make: {make}')
        
        models_menu = TerminalMenu(vehicle_master[make], search_key=None, search_highlight_style=None, title="Vehicle Model")
        models_menu_entry_index = models_menu.show()
        model = models_menu.chosen_menu_entry
        print(f'Model: {model}')

        year = input("Enter vehicle's year: ")
        if not year:
            print("You must enter the vehicle's year")
            continue
        plate = input("Enter vehicle's license plate: ")
        try:
            customer = Vehicle.create(int(customer_id), make, model, int(year), plate)
            print(' ')
            print(f'Vehicle #{customer.id} successfully saved')
            print(' ')
            print(' ')
            break
        except Exception as e:
            print('Error adding vehicle: ',e)

def vehicle_details(vehicle):
    from models.customer import Customer

    while True:
        print(' ')
        print('Vehicle Profile: ')
        print(f'    Owner: {Customer.find_by_id(vehicle.customer_id).name}')
        print(f'    Year: {vehicle.year}')
        print(f'    Make: {vehicle.make}')
        print(f'    Model: {vehicle.model}')
        print(f'    License Plate: {vehicle.plate}')
        print(f' ')
        
        services = vehicle.services()
        if services:
            print(f'Service History:')
            for service in services:
                print(service)

        choice = input("press any key to return to vehicle list ")
        print(' ')
        if choice:
            break

def vehicle_menu():
    while True:
        print("********************************************")
        print("*************** Vehicle Menu ***************")
        print("********************************************")
        print("1. Find vehicle by license plate")
        print("2. List all vehicles")
        print("3. Add new vehicle")
        print("z. Return to main menu")
        print("x. Exit the program")
        menu_input = input('> ')
        if menu_input == "1":
            vehicle_find_by_plate()
        elif menu_input == "2":
            vehicle_list_all()
        elif menu_input == "3":
            vehicle_add()
        elif menu_input.lower() == "z":
            break
        elif menu_input.lower() == "x":
            exit_program()