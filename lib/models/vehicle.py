from __init__ import CURSOR, CONN
from models.customer import Customer

class Vehicle:
    # Dictionary of objects saved to the database
    all = {}
    
    def __init__(self, customer_id, make, model, year, plate, id=None):
        self.id = id
        self.customer_id = customer_id
        self.make = make
        self.model = model
        self.year = year
        self.plate = plate
    
    def __repr__(self):
        return (
            f'<Vehicle {self.id} | {self.year} {self.make} {self.model} | {self.plate} | ' + 
            f'Owner: {self.customer_id}>'
        )
    
    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        if isinstance(customer_id, int) and Customer.find_by_id(customer_id):
            self._customer_id = customer_id
        else:
            raise ValueError(
                "customer_id must reference a customer in the database"
            )

    @property
    def make(self):
        return self._make

    @make.setter
    def make(self, make):
        if isinstance(make, str) and len(make) > 0:
            self._make = make
        else:
            raise ValueError(
                "Vehicle Make must be a non-empty string"
            )
        
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if isinstance(model, str) and len(model) > 0:
            self._model = model
        else:
            raise ValueError(
                "Vehicle Model must be a non-empty string"
            )
        
    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if type(year) is int:
            self._year = year
        else:
            raise ValueError(
                "Vehicle Year must be an integer"
            )
        
    @property
    def plate(self):
        return self._plate
    
    @plate.setter
    def plate(self, plate):
        self._plate = plate
        ##results in RecursionError
        # existing_plate = self.__class__.find_by_plate(plate)
        # if existing_plate and existing_plate.id is not self.id:
        #     raise ValueError(
        #         f"Vehicle with Plate {plate} already exists"
        #     )
        # else:
        #     self._plate = plate
    
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER, 
            make TEXT, 
            model TEXT, 
            year INTEGER, 
            plate TEXT, 
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS vehicles;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def create(cls, customer_id, make, model, year, plate):
        """ Initialize a new Vehicle instance and save the object to the database """
        instance = cls(customer_id, make, model, year, plate)
        instance.save()
        return instance

    def save(self):
        sql = """
            INSERT INTO vehicles (customer_id, make, model, year, plate) 
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.customer_id, self.make, self.model, self.year, self.plate))
        CONN.commit()

        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    def update(self):
        sql = """
            UPDATE vehicles 
            SET customer_id = ?, make = ?, model = ?, year = ?, plate = ? 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.customer_id, self.make, self.model, self.year, self.plate, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM vehicles 
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del self.__class__.all[self.id]

        # Set the id to None
        self.id = None

    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Vehicle object having the attribute values from the table row."""
        # Check the dictionary for an existing instance using the row's primary key
        vehicle = cls.all.get(row[0])
        if vehicle:
            # ensure attributes match row values in case local instance was modified
            vehicle.customer_id = row[1]
            vehicle.make = row[2]
            vehicle.model = row[3]
            vehicle.year = row[4]
            vehicle.plate = row[5]
        else:
            # not in dictionary, create new instance and add to dictionary
            vehicle = cls(row[1], row[2], row[3], row[4], row[5])
            vehicle.id = row[0]
            cls.all[vehicle.id] = vehicle
        return vehicle
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Vehicle object per row in the table"""
        sql = """
            SELECT * 
            FROM vehicles
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM vehicles 
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_plate(cls, plate):
        sql = """
            SELECT * 
            FROM vehicles 
            WHERE plate is ? 
        """
        row = CURSOR.execute(sql, (plate,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def services(self):
        """Return list of Services associated with current vehicle"""
        from models.service import Service
        sql = """
            SELECT * FROM services 
            WHERE vehicle_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [
            Service.instance_from_db(row) for row in rows
        ]