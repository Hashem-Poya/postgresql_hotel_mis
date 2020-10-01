from flask import Flask, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from sqlalchemy import func
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER


import os

app = Flask(__name__)


app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


from models import User, Customer, Food, Room, Customer_Room, Customer_Food


@app.route("/")
def hello():
    return render_template('dashboard.html')


# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/add-customer-form')
def add_customer_form():
    food_data = Food.query.all()
    rooms = Room.query.filter(Room.room_available_status == True).all()
    return render_template('add_customer.html', foods=food_data, rooms=rooms)


@app.route('/register-customer', methods=['POST'])
def register_customer():

    customer_name = request.form.get('customer_name')
    customer_address = request.form.get('customer_address')
    asigned_rooms_id = request.form.getlist('asigned_room')
    asigned_foods_id = request.form.getlist('asigned_food')
    customer_check_in_date = request.form.get('customer_check_in_date')
    customer_check_out_date = request.form.get('customer_check_out_date')

    try:
        customer = Customer(
            customer_id=None,
            customer_name=customer_name,
            customer_address=customer_address,
            customer_check_in_date=customer_check_in_date,
            customer_check_out_date=customer_check_out_date
        )

        db.session.add(customer)
        db.session.commit()

        for room_id in asigned_rooms_id:
            cust_room = Customer_Room(
                id=None,
                cust_id=customer.customer_id,
                room_id=int(room_id)
            )

            db.session.add(cust_room)
            room = Room.query.filter(Room.room_id == int(room_id)).update(
                {'room_available_status': False})
            db.session.commit()

        for food_id in asigned_foods_id:
            cust_food = Customer_Food(
                id=None,
                cust_id=customer.customer_id,
                food_id=int(food_id)
            )
            db.session.add(cust_food)
            db.session.commit()

        return redirect('/add-customer-form')

    except Exception as e:
        return (str(e))


@app.route('/all-customers')
def all_customers():
    customer_data = Customer.query.all()
    return render_template('list_customer.html', customers=customer_data)


@app.route('/show-customer/id/<int:customer_id>')
def show_customer_details(customer_id):
    customer_data = Customer.query.get(customer_id)
    customer_food_data = db.session.query(Food).join(Customer_Food, Food.food_id == Customer_Food.food_id).add_columns(
    ).filter(Customer_Food.cust_id == customer_id).all()
    customer_room_data = db.session.query(Room).join(
        Customer_Room, Room.room_id == Customer_Room.room_id).filter(Customer_Room.cust_id == customer_id).all()
    return render_template('customer_details.html', customer=customer_data, customer_room=customer_room_data, customer_food=customer_food_data)


@app.route('/add-room-form')
def add_room_form():
    return render_template('add_room.html')


@app.route('/register-room', methods=['POST'])
def register_room():
    room_no = request.form.get('room_no')
    room_price = request.form.get('room_price')
    currency = request.form.get('currency')
    try:
        room = Room(
            room_id=None,
            room_no=str(room_no),
            room_price=room_price,
            currency=currency,
            room_available_status=True
        )
        db.session.add(room)
        db.session.commit()
        return redirect('/add-room-form')
    except Exception as e:
        return (str(e))


@app.route('/all-rooms')
def all_rooms():
    try:

        rooms = Room.query.all()
        return render_template('list_room.html', all_rooms=rooms)

    except Exception as e:
        return (str(e))


@app.route('/add-food-form')
def add_food_form():
    return render_template('add_food.html')


@app.route('/register-food', methods=['POST'])
def register_food():
    food_name = request.form.get('food_name')
    food_price = request.form.get('food_price')
    currency = request.form.get('currency')
    try:
        food = Food(
            food_id=None,
            food_name=food_name,
            food_price=food_price,
            currency=currency
        )
        db.session.add(food)
        db.session.commit()
        return redirect('/add-food-form')

    except Exception as e:
        return (str(e))


@app.route('/all-foods')
def all_foods():
    try:
        foods = Food.query.all()
        return render_template('list_foods.html', all_foods=foods)

    except Exception as e:
        return (str(e))






def pdf_generator(customer_id, customer_name, customer_address, customer_check_in_date, customer_check_out_date, customer_room_price, customer_food_price):

    total_days = (customer_check_out_date - customer_check_in_date).days + 1
    total_room_price = customer_room_price * total_days

    total_to_pay = str(total_room_price + customer_food_price)

    canvas = Canvas('{}.pdf'.format(customer_name))
    canvas.setFont('Times-Roman', 16)
    canvas.drawString(
        50, 820, '******************** Hotel Bill ***********************')
    canvas.drawString(70, 780, 'Customer ID: {}'.format(str(customer_id)))
    canvas.drawString(70, 750, 'Customer Name: {}'.format(customer_name))
    canvas.drawString(70, 720, 'Customer Address: {}'.format(customer_address))
    canvas.drawString(
        70, 690, 'Customer Check-In-Date: {}'.format(str(customer_check_in_date)))
    canvas.drawString(
        70, 660, 'Customer Check-out-Date: {}'.format(str(customer_check_out_date)))
    canvas.drawString(
        70, 630, 'Customer Room Rent: {} AF'.format(str(total_room_price)))
    canvas.drawString(70, 600, 'Customer Food price: {} AF'.format(
        str(customer_food_price)))
    canvas.drawString(70, 570, 'Service Charge: {} AF'.format(str(50)))

    canvas.drawString(
        50, 530, '*****************************************************')
    canvas.drawString(200, 480, 'Total To Pay: {} AF'.format(total_to_pay))

    canvas.save()


@app.route('/generate-report/id/<int:customer_id>')
def generate_report(customer_id):

    current_customer = Customer.query.filter(
        Customer.customer_id == customer_id).all()
    customer_room = Customer_Room.query.filter(
        Customer_Room.cust_id == customer_id).all()  # 1
    customer_food = Customer_Food.query.filter(
        Customer_Food.cust_id == customer_id).all()  # 1

    room_price = 0
    total_food_price = 0

    for cf in customer_food:
        food_res = Food.query.filter(Food.food_id == cf.food_id).first()
        total_food_price += int(food_res.food_price)

    for cr in customer_room:
        room_res = Room.query.filter(Room.room_id == cr.room_id).first()
        room_price += int(room_res.room_price)
        Room.query.filter(cr.room_id == Room.room_id).update(
            {'room_available_status': True})
        db.session.commit()

    Customer_Food.query.filter(Customer_Food.cust_id == customer_id).delete()
    Customer.query.filter(Customer.customer_id == customer_id).delete()
    Customer_Room.query.filter(Customer_Room.cust_id == customer_id).delete()
    db.session.commit()

    pdf_generator(current_customer[0].customer_id, current_customer[0].customer_name, current_customer[0].customer_address,
                  current_customer[0].customer_check_in_date, current_customer[0].customer_check_out_date, room_price, total_food_price)

    return redirect('/all-customers')

