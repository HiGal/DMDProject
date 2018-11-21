from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
import json
from faker import Faker
from api import *

api = Flask(__name__)
rest_api = Api(api)

DB_FILE = 'carsharing.sqlite'

test = rest_api.model('Test', {'condition': fields.String("Condition...")})


# Example
# ____________________________________________________________#
@rest_api.route("/select_fake_data")
class TestSelectFake(Resource):

    @rest_api.expect(test)
    def post(self):
        cond = request.get_json(silent=True)
        conn = create_connection(DB_FILE)
        response = select_fake_data(conn, cond['condition'])
        close_connection(conn)
        return jsonify(response)


@rest_api.route("/modify")
class ModifyFake(Resource):

    def get(self):
        conn = create_connection(DB_FILE)
        response = modify_fake_data(conn)
        close_connection(conn)
        return jsonify(response)


@rest_api.route("/insert")
class InsertFakeData(Resource):

    def get(self):
        conn = create_connection(DB_FILE)
        response = insert_fake_data(conn)
        close_connection(conn)
        return jsonify(response)


# ______________________________________________________________#

@api.before_first_request
def init_db():
    logging.info("Try to connect to database")
    conn = create_connection(DB_FILE)
    logging.info("Try to initialise tables in database")
    json_data = open("sql_to_create.json").read()
    list_tables_to_create = json.loads(json_data)
    for sql_to_create in list_tables_to_create.keys():
        print(sql_to_create)
        create_table(conn, list_tables_to_create[sql_to_create])
    logging.info("Try to close connection to database")
    close_connection(conn)


if __name__ == '__main__':
    api.run()