from models.customer import Customer
from models.vehicle import Vehicle
from models.service import Service
from datetime import datetime
import calendar

def service_add():
    while True:
        plate = input("Enter the vehicle's license plate (Z to cancel): ")
        if plate.lower() == "z":
            break
        else:
            vehicle = Vehicle.find_by_plate(plate)
            if vehicle:
                mileage = input("Enter the vehicle's current mileage: ")
                if not mileage:
                    print("You must enter vehicle's current mileage")
                    continue
                print('Service record created.')
                confirm = input("Press Y to save, Z to cancel: ")
                if confirm.lower() == "y":
                    service_date = datetime.now().strftime("%m-%d-%Y")
                    try:
                        service = Service.create(vehicle.id,int(mileage),service_date)
                        print(' ')
                        print(f'Service record #{service.id} successfully saved')
                        print(' ')
                        service_invoice(service)
                        print(' ')
                        break
                    except Exception as e:
                        print('Error adding service record: ',e)
            else:
                print(
                    f'Vehicle with license plate "{plate}" not found')

def service_invoice(service):
    # credits: https://gist.github.com/defuse/01a9d0ba5ce3b4083810
    
    service = Service.find_by_id(service.id)
    if not service:
        print("Error loading service record")
    
    vehicle = Vehicle.find_by_id(service.vehicle_id)
    customer = Customer.find_by_id(vehicle.customer_id)
    
    #convert service.service_date to datetime object
    sd = datetime.strptime(service.service_date,'%m-%d-%Y').date()

    print(f"""
          
  Lube Lab Express                                         INVOICE
  New York, NY                               Date: {calendar.month_name[sd.month]} {sd.day}, {sd.year}

  To:                                                  Service #{service.id}
      {customer.name}
      {customer.address}

  +-----------------------------------------------------------------+
  | Quantity |         Description         | Unit Price |   Total   |
  +-----------------------------------------------------------------+
  | 1        | Express Oil Change          | $74.99     | $74.99    |
  | 2        | Replaced Filters            | $14.99     | $29.98    |
  +-----------------------------------------------------------------+

                                                SUB-TOTAL: $104.97
                                                      TAX:   $7.08
                                                    TOTAL: $112.05

  Payment Instructions:

    Sale is final, to refunds or credits.
    Payment is due within 30 days.

  Thank you for your business!
""")