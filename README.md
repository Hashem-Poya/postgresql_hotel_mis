# POSTGRESQL HOTEL MIS
The **Postgresql Hotel MIS** is a MIS which written in Python programming language & Flask Framework and Postgresql which is a kind of DBMS.
## Features
- Store Customer Data like: name, address, check-in-date, check-out-date
- Store Room Date like: Room no, and room price and currency
- Store Food data like: food name, food price and currency
- after we can asign room and food for the specific customer
- finally user can generate report for the customer as PDF
## Getting started
- python interpreter must be installed in your computer
- Go to requirments.txt and install all the library
- Your have to install Postgresql in order to work with this project
### Running App
- First off all you have to install Git version controll in your OS
- The clone the Source code from this repo: 
```
    git clone https://github.com/Hashem-Poya/postgresql_hotel_mis.git
```
- after clone this project in postgresql create database by name of hotel_db
- then migrate the tables by these three commands
```
python3 manage.db init
```
```
python3 manage.db migrate
```
```
python3 manage.db upgrade
```
- after this step if passed without errors run this command to start with the project
```
flask run
```
- or
```
python3 manage.db runserver
```
## Contributing
- for any suggestion and problem in this program you can share your idea through this email poya.kpu.2020@gmail.com