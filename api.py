from db_management import create_connection, close_connection
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from faker import Faker
from db_management import *
from utils import fill_db_with_data

fake = Faker()
api = Flask(__name__)
rest_api = Api(api)



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
    # create_table(conn, "tables_to_create.sql")
    fill_db_with_data(conn)
    logging.info("Try to close connection to database")
    close_connection(conn)





if __name__ == '__main__':
    api.run()
