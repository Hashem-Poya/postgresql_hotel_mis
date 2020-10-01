from app import db


class User(db.Model):
    """
        Blueprint for the user table
    """
    
    
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String())
    user_email = db.Column(db.String())
    user_password = db.Column(db.String())
    user_role = db.Column(db.Integer)

    def __init__(self, user_id, user_name, user_email, user_password, user_role):
        
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.user_role = user_role

    def __repr__(self):
        return '<id {}>'.format(self.user_id)

    def serialize(self):
        return {
            'User ID': self.user_id,
            'User Name': self.user_name,
            'User Email': self.user_email,
            'User Password': self.user_password,
            'User Role': self.user_role
        }


class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String())
    customer_address = db.Column(db.String)
    customer_check_in_date = db.Column(db.Date)
    customer_check_out_date = db.Column(db.Date)

    def __init__(self, customer_id, customer_name, customer_address, customer_check_in_date, customer_check_out_date):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_check_in_date = customer_check_in_date
        self.customer_check_out_date = customer_check_out_date

    def __repr__(self):
        return '<id {}>'.format(self.customer_id)

    def serialize(self):
        return {
            'Customer ID': self.customer_id,
            'Customer Name': self.customer_name,
            'Customer Address': self.customer_address,
            'Customer Check-in-Date': self.customer_check_in_date,
            'Customer Check-out-Date': self.customer_check_out_date
        }


class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String())
    room_price = db.Column(db.Integer)
    currency = db.Column(db.String())
    room_available_status = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, room_id, room_no, room_price, currency, room_available_status):
        self.room_id = room_id
        self.room_no = room_no
        self.room_price = room_price
        self.currency = currency
        self.room_available_status = room_available_status

    def __repr__(self):
        return '<id {}>'.format(self.room_id)

    def serialize(self):
        return {
            'Room ID': self.room_id,
            'Room NO': self.room_no,
            'Room Price': self.room_price,
            'Currency': self.currency,
            'Available': self.room_available_status
        }


class Food(db.Model):
    __tablename__ = 'food'

    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String())
    food_price = db.Column(db.Integer)
    currency = db.Column(db.String())

    def __init__(self, food_id, food_name, food_price, currency):
        self.food_id = food_id
        self.food_name = food_name
        self.food_price = food_price
        self.currency = currency

    def __repr__(self):
        return '<id {}>'.format(self.food_id)

    def serialize(self):
        return {
            'Food ID': self.food_id,
            'Food Name': self.food_name,
            'Food Price': self.food_price,
            'Currency': self.currency
        }


class Customer_Room(db.Model):
    __tablename__ = 'cust_room'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    room_id = db.Column(db.Integer)

    def __init__(self, id, cust_id, room_id):
        self.id = id
        self.cust_id = cust_id
        self.room_id = room_id

    # def __repr__(self):
    #     return 'instance of customer room'

    def serialize(self):
        return {
            'ID': self.id,
            'Customer ID': self.cust_id,
            'Room ID': self.room_id
        }


class Customer_Food(db.Model):
    __tablename__ = 'cust_food'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    food_id = db.Column(db.Integer)

    def __init__(self, id, cust_id, food_id):
        self.id = id
        self.cust_id = cust_id
        self.food_id = food_id

    def __repr__(self):
        return '<id {}'.format(self.id)

    def serialize(self):
        return {
            'ID': self.id,
            'Customer ID': self.cust_id,
            'Food ID': self.food_id
        }
