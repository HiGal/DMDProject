from geopy.geocoders import Nominatim
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from faker import Faker
from api import *
import random
import datetime
import sqlite3
import logging
fake = Faker()
api = Flask(__name__)
rest_api = Api(api)


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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        with open(create_table_sql) as f:
            script = f.read()
        c = conn.cursor()
        c.executescript(script)
        conn.commit()
        logging.info("Successfully created table in database")

    except sqlite3.DatabaseError as e:
        print(e)


def insert_into_customers(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO customers(username, email, cardnumber, fullname, phone_number,
                zip, address) VALUES(?,?,?,?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting into customers occurs")
    return -1


def insert_into_orders(conn, task):
    cursor = conn.cursor()
    try:
        sql = ''' INSERT INTO orders(date, time, date_closed, status,
  cost, st_point, destination, car_location, username,car_id ) VALUES(?,?,?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_plugs(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO charging_plugs(shape_plug, size_plug) VALUES (?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_models(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO models(model_id, plug_id, name, type, service_class) VALUES (?,?,?,?,? )'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_cars(conn, GPS_location, reg_num, color, year, charge, available):
    task = (GPS_location, year, color, reg_num, charge, available)
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO cars(gps_location, year, colour, reg_num, charge, available) VALUES (?,?,?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

if __name__ == '__main__':
    api.run()
