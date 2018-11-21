from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
import json
from faker import Faker
from api import *

api = Flask(__name__)
rest_api = Api(api)

fake_data_generator = Faker()


# sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks(
#                                 id integer UNIQUE PRIMARY KEY,
#                                 name varchar(50) NOT NULL,
#                                 priority integer,
#                                 end_date date NOT NULL
#                             );"""

# sql_create_charging_station_table = """CREATE TABLE IF NOT EXISTS charging_station(
#                                             UID integer UNIQUE PRIMARY KEY,
#                                             amount_of_available_slots integer NOT NULL,
#                                             time_of_charging time NOT NULL,
#                                             price double
#                                             GPS_location varchar(25) NOT NULL
#                             );"""

# sql_create_charging_plugs = """CREATE TABLE IF NOT EXISTS charging_plugs(
#                                 plug_id integer PRIMARY KEY ,
#                                 shape_plug varchar(20) not null  ,
#                                 size_plug int(10) not null
#                             );"""
#
# sql_create_charging_have_plugs = """CREATE TABLE IF NOT EXISTS charging_have_plugs(
#                                             charge_have_plugs_id integer NOT NULL,
#                                             UID integer NOT NULL,
#                                             plug_id integer NOT NULL,
#                                             FOREIGN KEY (UID)  references charging_station(UID),
#                                             FOREIGN KEY (plug_id)  references charging_plugs(plug_id),
#                                             PRIMARY KEY (charge_have_plugs_id)
#                                 );"""
#
# sql_create_provider_table = """CREATE TABLE IF NOT EXISTS provider(
#                                     company_id integer PRIMARY KEY,
#                                     address varchar(25) NOT NULL,
#                                     phone_number varchar(25),
#                                     name_company varchar(25)
#
#                         );"""
#
# sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers (
#                                   username  varchar(20) UNIQUE PRIMARY KEY ,
#                                   email  varchar(20) not null ,
#                                   cardnumber    varchar(20) not null,
#                                   fullname   varchar(50) not null,
#                                   phone_number varchar(15),
#                                   zip integer not null ,
#                                   city varchar(20) not null ,
#                                   country varchar(50) not null
#
#
#                         );"""
#
# #TODO cost and duration?
# #TODO st_point, pick location same?
# sql_create_orders = """CREATE TABLE IF NOT EXISTS orders (
#                         order_id integer UNIQUE PRIMARY KEY,
#                         date text not null ,
#                         time text not null ,
#                         date_closed text not null,
#                         duration integer,
#                         status varchar(10) not null ,
#                         cost integer,
#                         st_point varchar(50) not null ,
#                         destination varchar(50) not null ,
#                         car_location varchar(50) not null,
#
#                         foreign key (order_id) references customers(username)
#
#                     );"""

# sql_create_cars = """CREATE TABLE IF NOT EXISTS cars(
#                         car_id integer primary key ,
#                         gps_location varchar(25) not null ,
#                         year varchar(4),
#                         colour varchar(20) not null,
#                         reg_num varchar(11) not null ,
#                         charge int(1) not null ,
#                         available int(1) not null ,
#
#                         foreign key (car_id) references orders(order_id),
#                         foreign key (car_id) references models(model_id)
#                     );"""

# sql_create_charge_car_table = """CREATE TABLE IF NOT EXISTS charge_car(
#                                     charge_car_id integer PRIMARY KEY,
#                                     cost double,
#                                     date date,
#                                     car_id integer,
#                                     UID integer,
#                                     FOREIGN KEY (car_id) references cars(car_id),
#                                     FOREIGN KEY (UID) references charging_station(UID)
#                         );"""
#
# #TODO Availability of timing( What the type?)
# sql_create_workshop_table = """CREATE TABLE IF NOT EXISTS workshop(
#                                     WID integer PRIMARY KEY ,
#                                     availability_of_timing time NOT NULL,
#                                     location varchar(25) NOT NULL
#                         );"""
#
# sql_create_repair_car = """CREATE TABLE IF NOT EXISTS repair_car(
#                                 WID integer,
#                                 car_id integer unique,
#                                 report_id integer PRIMARY KEY,
#                                 date date,
#                                 progress_status varchar(10),
#                                 FOREIGN KEY (WID) references workshop(WID),
#                                 FOREIGN KEY (car_id) references cars(car_id)
#                     );"""
## TODO: Model_id refers(ссылается) to the car_id???
# sql_create_models = """CREATE TABLE IF NOT EXISTS models(
#                         model_id integer PRIMARY KEY ,
#                         name varchar(20) not null,
#                         type varchar(30) not null ,
#                         service_class varchar(30) not null ,
#                         foreign key (model_id) references cars(car_id),
#                         foreign key (model_id) references charging_plugs(plug_id)
#                     );"""

# sql_create_part_order_table = """CREATE TABLE IF NOT EXISTS part_order(
#                                     date date,
#                                     amount integer,
#                                     cost double,
#                                     order_id integer PRIMARY KEY ,
#                                     part_id integer,
#                                     WID integer,
#                                     company_id integer,
#                                     FOREIGN KEY (part_id) references parts(part_id),
#                                     FOREIGN KEY (WID) references workshop(WID),
#                                     FOREIGN KEY (company_id) references provider(company_id)
#                         );"""
#
# sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts(
#                                 part_id integer PRIMARY KEY,
#                                 type_of_detail varchar(25),
#                                 cost double,
#                                 amount integer,
#                                 amount_week_ago integer,
#                                 FOREIGN KEY (WID) references workshop(WID)
#                         );"""

# sql_create_workshop_have_parts_table = """CREATE TABLE IF NOT EXISTS workshop_have_parts(
#                                     amount integer,
#                                     amount_week_ago integer,
#                                     WID integer PRIMARY KEY,
#                                     part_id integer PRIMARY KEY,
#                                     FOREIGN KEY (WID) references workshop(WID),
#                                     FOREIGN KEY (part_id) references parts(part_id)
#                         );"""
#
# sql_create_fit_table = """CREATE TABLE IF NOT EXISTS fit(
#                                 fit_id integer PRIMARY KEY,
#                                 part_id integer,
#                                 model_id integer,
#                                 FOREIGN KEY (part_id) references parts(part_id),
#                                 FOREIGN KEY (model_id) references models(model_id)
#                 );"""

# sql_create_providers_have_parts_table = """CREATE TABLE IF NOT EXISTS providers_have_parts(
#                                                 providers_have_parts_id integer PRIMARY KEY,
#                                                 company_id integer,
#                                                 part_id integer,
#                                                 FOREIGN KEY (company_id) references provider(company_id),
#                                                 FOREIGN KEY (part_id) references parts(part_id)
#                                 );"""
# list_tables_to_create=[sql_create_charging_station_table,
#                        sql_create_charging_have_plugs,
#                        sql_create_provider_table,
#                        sql_create_customers_table,
#                        sql_create_orders,
#                        sql_create_cars,
#                        sql_create_charge_car_table,
#                        sql_create_workshop_table,
#                        sql_create_repair_car,
#                        sql_create_models,
#                        sql_create_part_order_table,
#                        sql_create_parts_table,
#                        sql_create_workshop_have_parts_table,
#                        sql_create_fit_table,
#                        sql_create_providers_have_parts_table]

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

DB_FILE = 'carsharing.sqlite'

test = rest_api.model('Test', {'condition': fields.String("Condition...")})


# Example
# ____________________________________________________________#
# @rest_api.route("/select_fake_data")
# class TestSelectFake(Resource):
#
#     @rest_api.expect(test)
#     def post(self):
#         cond = request.get_json(silent=True)
#         conn = create_connection(DB_FILE)
#         response = select_fake_data(conn, cond['condition'])
#         close_connection(conn)
#         return jsonify(response)
#
#
# @rest_api.route("/modify")
# class ModifyFake(Resource):
#
#     def get(self):
#         conn = create_connection(DB_FILE)
#         response = modify_fake_data(conn)
#         close_connection(conn)
#         return jsonify(response)
#
#
# @rest_api.route("/insert")
# class InsertFakeData(Resource):
#
#     def get(self):
#         conn = create_connection(DB_FILE)
#         response = insert_fake_data(conn)
#         close_connection(conn)
#         return jsonify(response)


# ______________________________________________________________#

@api.before_first_request
def init_db():
    logging.info("Try to connect to database")
    conn = create_connection(DB_FILE)
    logging.info("Try to initialise tables in database")
    create_table(conn, "tables_to_create.sql")
    logging.info("Try to close connection to database")
    close_connection(conn)

def fill_db_with_data():
    pass

if __name__ == '__main__':
    api.run()