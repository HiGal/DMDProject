from flask import Flask, jsonify, request
import sqlite3
import logging
from flask_restplus import Api, Resource, fields
import json

logging.basicConfig(level=logging.DEBUG)
from faker import Faker


datagen = Faker()


sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks(
                                id integer UNIQUE PRIMARY KEY,
                                name varchar(50) NOT NULL,
                                priority integer,
                                end_date date NOT NULL
                            );"""

sql_create_charging_station_table = """CREATE TABLE IF NOT EXISTS charging_station(
                                            UID integer UNIQUE PRIMARY KEY,
                                            amount_of_available_slots integer NOT NULL,
                                            time_of_charging time NOT NULL,
                                            price double
                                            GPS_location varchar(25) NOT NULL
                            );"""

sql_create_charging_plugs = """CREATE TABLE IF NOT EXISTS charging_plugs(
                                plug_id integer PRIMARY KEY ,
                                shape_plug varchar(20) not null  ,
                                size_plug int(10) not null
                            );"""

sql_create_charging_have_plugs = """CREATE TABLE IF NOT EXISTS charging_have_plugs(
                                            charge_have_plugs_id integer NOT NULL, 
                                            UID integer NOT NULL,
                                            plug_id integer NOT NULL,
                                            FOREIGN KEY (UID)  references charging_station(UID),
                                            FOREIGN KEY (plug_id)  references charging_plugs(plug_id),
                                            PRIMARY KEY (charge_have_plugs_id)
                                );"""

sql_create_provider_table = """CREATE TABLE IF NOT EXISTS provider(
                                    company_id integer PRIMARY KEY,
                                    address varchar(25) NOT NULL,
                                    phone_number varchar(25),
                                    name_company varchar(25)

                        );"""
#
sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers (
                                  username  varchar(20) UNIQUE PRIMARY KEY ,
                                  email  varchar(20) not null ,
                                  cardnumber    varchar(20) not null,
                                  fullname   varchar(50) not null,
                                  phone_number varchar(15),
                                  zip integer not null ,
                                  city varchar(20) not null ,
                                  country varchar(50) not null


                        );"""
#
# #TODO cost and duration?
# #TODO st_point, pick location same?
sql_create_orders = """CREATE TABLE IF NOT EXISTS orders (
                        order_id integer UNIQUE PRIMARY KEY,
                        date text not null ,
                        time text not null ,
                        date_closed text not null,
                        duration integer,
                        status varchar(10) not null ,
                        cost integer,
                        st_point varchar(50) not null ,
                        destination varchar(50) not null ,
                        car_location varchar(50) not null,

                        foreign key (order_id) references customers(username)

                    );"""

sql_create_cars = """CREATE TABLE IF NOT EXISTS cars(
                        car_id integer primary key ,
                        gps_location varchar(25) not null ,
                        year varchar(4),
                        colour varchar(20) not null,
                        reg_num varchar(11) not null ,
                        charge int(1) not null ,
                        available int(1) not null ,

                        foreign key (car_id) references orders(order_id),
                        foreign key (car_id) references models(model_id)
                    );"""

sql_create_charge_car_table = """CREATE TABLE IF NOT EXISTS charge_car(
                                    charge_car_id integer PRIMARY KEY, 
                                    cost double,
                                    date date,
                                    car_id integer,
                                    UID integer,
                                    FOREIGN KEY (car_id) references cars(car_id),
                                    FOREIGN KEY (UID) references charging_station(UID)
                        );"""
#
# #TODO Availability of timing( What the type?)
sql_create_workshop_table = """CREATE TABLE IF NOT EXISTS workshop(
                                    WID integer PRIMARY KEY ,
                                    availability_of_timing time NOT NULL,
                                    location varchar(25) NOT NULL
                        );"""

sql_create_repair_car = """CREATE TABLE IF NOT EXISTS repair_car(
                                WID integer,
                                car_id integer unique,
                                report_id integer PRIMARY KEY,
                                date date,
                                progress_status varchar(10),
                                FOREIGN KEY (WID) references workshop(WID),
                                FOREIGN KEY (car_id) references cars(car_id)
                    );"""
## TODO: Model_id refers(ссылается) to the car_id???
sql_create_models = """CREATE TABLE IF NOT EXISTS models(
                        model_id integer PRIMARY KEY ,
                        name varchar(20) not null,
                        type varchar(30) not null ,
                        service_class varchar(30) not null ,
                        foreign key (model_id) references cars(car_id),
                        foreign key (model_id) references charging_plugs(plug_id)
                    );"""

sql_create_part_order_table = """CREATE TABLE IF NOT EXISTS part_order(
                                    date date,
                                    amount integer,
                                    cost double,
                                    order_id integer PRIMARY KEY ,
                                    part_id integer,
                                    WID integer,
                                    company_id integer,
                                    FOREIGN KEY (part_id) references parts(part_id),
                                    FOREIGN KEY (WID) references workshop(WID),
                                    FOREIGN KEY (company_id) references provider(company_id)
                        );"""

sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts(
                                part_id integer PRIMARY KEY,
                                type_of_detail varchar(25),
                                cost double,
                                amount integer,
                                amount_week_ago integer,
                                FOREIGN KEY (WID) references workshop(WID)
                        );"""

# sql_create_workshop_have_parts_table = """CREATE TABLE IF NOT EXISTS workshop_have_parts(
#                                     amount integer,
#                                     amount_week_ago integer,
#                                     WID integer PRIMARY KEY,
#                                     part_id integer PRIMARY KEY,
#                                     FOREIGN KEY (WID) references workshop(WID),
#                                     FOREIGN KEY (part_id) references parts(part_id)
#                         );"""
#
sql_create_fit_table = """CREATE TABLE IF NOT EXISTS fit(
                                fit_id integer PRIMARY KEY, 
                                part_id integer,
                                model_id integer,
                                FOREIGN KEY (part_id) references parts(part_id),
                                FOREIGN KEY (model_id) references models(model_id)
                );"""

sql_create_providers_have_parts_table = """CREATE TABLE IF NOT EXISTS providers_have_parts(
                                                providers_have_parts_id integer PRIMARY KEY, 
                                                company_id integer,
                                                part_id integer,
                                                FOREIGN KEY (company_id) references provider(company_id),
                                                FOREIGN KEY (part_id) references parts(part_id)
                                );"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Successfully connected to database")
        return conn
    except sqlite3.DatabaseError as e:
        print(e)

    return None

def close_connection(conn):
    conn.close()
    logging.info("Successfully closed connection to database")
    return None

def insert_fake_data(conn):
    cursor = conn.cursor()
    try:
        for i in range(10):
            name = str(datagen.name())
            num = str(datagen.random_number(digits=3))
            date = str(datagen.date())
            sql = ''' INSERT INTO tasks(name,priority,end_date)
                          VALUES(?,?,?) '''
            task = (name, num, date)
            cursor.execute(sql, task)
            conn.commit()
        return "Successfull"
    except Exception:
        logging.info("Error while inserting occurs")
    return "Error while inserting occurs"


def modify_fake_data(conn):
    cursor = conn.cursor()
    try:
        sql = '''UPDATE tasks SET name = 'AAAAAAAAAAAAA' WHERE priority < 10000'''
        cursor.execute(sql)
        conn.commit()
        return "Successfully modified"
    except Exception:
        logging.info("Error while updating occurs")
    return "Error while updating occurs"


def select_fake_data(conn, cond):
    cursor = conn.cursor()
    diction = {}
    try:
        sql = "SELECT name FROM tasks WHERE " + cond + " BETWEEN 5005 and 15600"
        cursor.execute(sql)
        i = 0
        for row in cursor.fetchall():
            diction[i] = row[0]
            i += 1
        return diction
    except Exception as e:
        print(e)
        logging.info("Error while selecting occurs")
    return "Error while updating occurs"

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
        logging.info("Successfully created table in database")
    except sqlite3.DatabaseError as e:
        print(e)