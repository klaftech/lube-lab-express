from models.customer import Customer
from helpers import exit_program

def customer_list_all():
    while True:
        customers = Customer.get_all()
        for customer in customers:
            print(customer)
        
        choice = input("Enter id to see details or Z to return ")
        if choice.lower() == "z":
            break
        else:
            customer = Customer.find_by_id(choice)
            if customer:
                customer_details(customer)
            else:
                print(' ')
                print(f'Customer #{choice} not found. ')
                print(' ')


def customer_find_by_name():
    # TO DO: show matching results and allow selection by ID
    while True:
        name = input("Enter the customers's name (Z to cancel): ")
        if name.lower() == "z":
            break
        else:
            customer = Customer.find_by_name(name)
            print(customer) if customer else print(
                f'Customer {name} not found')

def customer_add():
    while True:
        name = input("Enter customer's full name: ")
        address = input("Enter full address: ")
        try:
            customer = Customer.create(name, address)
            print(' ')
            print(f'Customer #{customer.id} successfully saved')
            print(' ')
            print(' ')
            break
        except Exception as e:
            print('Error adding customer: ',e)

def customer_details(customer):
    while True:
        print(' ')
        print('Customer Profile: ')
        print(f'    Name: {customer.name}')
        print(f'    Address: {customer.address}')
        print(f' ')
        
        vehicles = customer.vehicles()
        if vehicles:
            print('Vehicles:')
            for vehicle in vehicles:
                print(vehicle)
                
                services = vehicle.services()
                if services:
                    print(f'    Service History:')
                    for service in services:
                        print(f'        {service}')
                    print(' ')
        else:
            print('No vehicles.')

        choice = input("press any key to return to customer list ")
        if choice:
            break

def customer_menu():
    while True:
        print("********************************************")
        print("*************** Customer Menu **************")
        print("********************************************")
        print("1. Find customer by name")
        print("2. List all customers")
        print("3. Add new customer")
        print("z. Return to main menu")
        print("x. Exit the program")
        menu_input = input('> ')
        if menu_input == "1":
            customer_find_by_name()
        elif menu_input == "2":
            customer_list_all()
        elif menu_input == "3":
            customer_add()
        elif menu_input.lower() == "z":
            break
        elif menu_input.lower() == "x":
            exit_program()