
from geopy.geocoders import Nominatim
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from faker import Faker
from app import *
import random
import datetime
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
    fill_db_with_data(conn)
    logging.info("Try to close connection to database")
    close_connection(conn)


def fill_db_with_data(conn):
    users = []
    plugs = []
    cars = []
    # create parameters for plugs
    for i in range(5):
        shape_of_plugs = random.randint(100, 999)
        size_of_plug = random.randint(100, 999)
        task = (shape_of_plugs, size_of_plug)
        plugs.append(task)
        print(task)
        # insert_into_plugs(conn, task)


    for i in range(5):
        address = str(fake.address()).replace('\n', '')
        name = fake.name()
        username = str(name).replace(' ', '').lower()
        email = username + "@gmail.com"
        task = (username,
                email,
                random.randint(1000000000000000, 9999999999999999),
                name,
                random.randint(10000000000, 99999999999),
                random.randint(100000, 999999),
                address
                )
        users.append(task)
        print(task)
        # insert_into_customers(conn, task)

    geolocator = Nominatim(user_agent="dmd_project")
    for i in range(10):
        date = datetime.date.today()
        status = "closed"
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        start = str(location.latitude) + " " + str(location.longitude)
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        finish = str(location.latitude) + " " + str(location.longitude)
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        car_loc = str(location.latitude) + " " + str(location.longitude)
        task = (date, timestamp, timestamp, status,
                random.randint(1000, 9999),
                start, finish, car_loc, users[i // len(users)][0], 1)
        print(task)
        # insert_into_customers(conn, task)

    pass


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

