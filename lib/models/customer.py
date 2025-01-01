from __init__ import CURSOR, CONN

class Customer:
    # Dictionary of objects saved to the database
    all = {}
    
    def __init__(self, name, address, id=None):
        self.id = id
        self.name = name
        self.address = address
    
    def __repr__(self):
        return f'<Customer {self.id} | {self.name} | {self.address}>'
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )
    
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if isinstance(address, str) and len(address):
            self._address = address
        else:
            raise ValueError(
                "Address must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def create(cls, name, address):
        """ Initialize a new Customer instance and save the object to the database """
        instance = cls(name, address)
        instance.save()
        return instance

    def save(self):
        sql = """
            INSERT INTO customers (name, address) 
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name,self.address))
        CONN.commit()

        self.id = CURSOR.lastrowid
        self.__class__.all[self.id] = self

    def update(self):
        sql = """
            UPDATE customers 
            SET name = ?, address = ? 
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name,self.address,self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM customers 
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
        """Return a Customer object having the attribute values from the table row."""
        # Check the dictionary for an existing instance using the row's primary key
        if instance := cls.all.get(row[0]):
            # ensure attributes match row values in case local instance was modified
            instance.name = row[1]
            instance.address = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            instance = cls(row[1], row[2])
            instance.id = row[0]
            cls.all[instance.id] = instance
        return instance
    
    @classmethod
    def get_all(cls):
        """Return a list containing a Customer object per row in the table"""
        sql = """
            SELECT * 
            FROM customers
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * 
            FROM customers 
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM customers 
            WHERE name is ? 
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def vehicles(self):
        """Return list of vehicles associated with current customer"""
        from models.vehicle import Vehicle
        sql = """
            SELECT * FROM vehicles 
            WHERE customer_id = ?
        """
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [
            Vehicle.instance_from_db(row) for row in rows
        ]