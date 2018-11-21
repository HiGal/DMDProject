from flask import Flask, jsonify, request
import sqlite3
import logging
import re
from flask_restplus import Api, Resource, fields
import json

logging.basicConfig(level=logging.DEBUG)


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


def insert_into_customers(conn,task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO customers(username, email, cardnumber, fullname, phone_number,
                zip, address) VALUES(?,?,?,?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_orders(conn, order_id, date, time, date_closed, duration, status,
  cost, st_point, destination, car_location, customer_username):
    task = (order_id, date, time, date_closed, duration, status,
  cost, st_point, destination, car_location, customer_username)
    cursor = conn.cursor()
    try:
        sql = ''' INSERT INTO orders(order_id, date, time, date_closed, duration, status,
  cost, st_point, destination, car_location, username) VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
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

def insert_into_models(conn, name, type, serviece_class):
    task = ()



# def insert_fake_data(conn):
#     cursor = conn.cursor()
#     try:
#         for i in range(10):
#             name = str(fake_data.name())
#             num = str(fake_data.random_number(digits=3))
#             date = str(fake_data.date())
#             sql = ''' INSERT INTO tasks(name,priority,end_date)
#                           VALUES(?,?,?) '''
#             task = (name, num, date)
#             cursor.execute(sql, task)
#             conn.commit()
#         return "Successful"
#     except Exception:
#         logging.info("Error while inserting occurs")
#     return "Error while inserting occurs"
#
#
# def modify_fake_data(conn):
#     cursor = conn.cursor()
#     try:
#         sql = '''UPDATE tasks SET name = 'AAAAAAAAAAAAA' WHERE priority < 10000'''
#         cursor.execute(sql)
#         conn.commit()
#         return "Successfully modified"
#     except Exception:
#         logging.info("Error while updating occurs")
#     return "Error while updating occurs"
#
#
# def select_fake_data(conn, cond):
#     cursor = conn.cursor()
#     diction = {}
#     try:
#         sql = "SELECT name FROM tasks WHERE " + cond + " BETWEEN 5005 and 15600"
#         cursor.execute(sql)
#         i = 0
#         for row in cursor.fetchall():
#             diction[i] = row[0]
#             i += 1
#         return diction
#     except Exception as e:
#         print(e)
#         logging.info("Error while selecting occurs")
#     return "Error while updating occurs"
