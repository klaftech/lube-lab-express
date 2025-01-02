from __init__ import CURSOR, CONN
from models.vehicle import Vehicle

# TO DO mileage setter, check that mileage moved forward

class Service:
    # Dictionary of objects saved to the database
    all = {}
    
    def __init__(self, vehicle_id, mileage, service_date, id=None):
        self.id = id
        self.vehicle_id = vehicle_id
        self.mileage = mileage
        self.service_date = service_date
    
    def __repr__(self):
        return f'<Service {self.id} | Vehicle {self.vehicle_id}, mileage: {self.mileage}, date: {self.service_date}>'
    
    @staticmethod
    def validate_date(date):
        from datetime import datetime
        #datetime.date(2020, 5, 17)
        #print(datetime.date(datetime.now()))
        format = "%m-%d-%Y"
        try:
            return bool(datetime.strptime(date, format))
        except ValueError:
            return False
        
    @property
    def vehicle_id(self):
        return self._vehicle_id

    @vehicle_id.setter
    def vehicle_id(self, vehicle_id):
        if isinstance(vehicle_id, int) and Vehicle.find_by_id(vehicle_id):
            self._vehicle_id = vehicle_id
        else:
            raise ValueError(
                "vehicle_id must reference a vehicle in the database"
            )

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, mileage):
        #if isinstance(mileage, str) and len(mileage):
        if type(mileage) is int:
            #check that mileage is not earlier than previous
            self._mileage = mileage
        else:
            raise ValueError(
                "Vehicle Mileage must be an integer"
            )
        
    @property
    def service_date(self):
        return self._service_date

    @service_date.setter
    def service_date(self, service_date):
        if isinstance(service_date, str) and len(service_date) > 0:
            if self.validate_date(service_date):
                self._service_date = service_date
            else:
                raise ValueError(
                    "Service Date must be formatted as mm-dd-yyyy"
                )
        else:
            raise ValueError(
                "Service Date must be a non-empty string"
            )
        
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY,
            vehicle_id INTEGER, 
            mileage INTEGER, 
            service_date TEXT, 
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
        )
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS services;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def create(cls, vehicle_id, mileage, service_date):
        """ Initialize a new Service instance and save the object to the database """
        instance = cls(vehicle_id, mileage, service_date)
        instance.save()
        return instance

    def save(self):
        sql = """
            INSERT INTO services (vehicle_id, mileage, service_date) 
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.vehicle_id, self.mileage, self.service_date))
        CONN.commit()

        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    def update(self):
        sql = """
            UPDATE services 
            SET vehicle_id = ?, mileage = ?, service_date = ? 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.vehicle_id, self.mileage, self.service_date, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM services 
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
        """Return a Service object having the attribute values from the table row."""
        # Check the dictionary for an existing instance using the row's primary key
        service = cls.all.get(row[0])
        if service:
            # ensure attributes match row values in case local instance was modified
            service.vehicle_id = row[1]
            service.mileage = row[2]
            service.service_date = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            service = cls(row[1], row[2], row[3])
            service.id = row[0]
            cls.all[service.id] = service
        return service
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Service object per row in the table"""
        sql = """
            SELECT * 
            FROM services
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM services 
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_vehicle(cls, vehicle_id):
        sql = """
            SELECT * 
            FROM services 
            WHERE vehicle_id is ? 
        """
        row = CURSOR.execute(sql, (vehicle_id,)).fetchone()
        return cls.instance_from_db(row) if row else None