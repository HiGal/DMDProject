import logging
import sqlite3
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from utils import *
import certifi
import ssl
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

fake = Faker()
api = Flask(__name__)
rest_api = Api(api)

DB_FILE = 'carsharing.sqlite'

test = rest_api.model('Test', {'condition': fields.String("Condition...")})

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




@api.before_first_request
def init_db():
    logging.info("Try to connect to database")
    conn = create_connection(DB_FILE)
    logging.info("Try to initialise tables in database")
    # create_table(conn, "tables_to_create.sql")
    #fill_db_with_data(conn)
    logging.info("Try to close connection to database")
    close_connection(conn)




if __name__ == '__main__':
    api.run()



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

