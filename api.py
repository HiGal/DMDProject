from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from scenarios import *
from utils import *
import certifi
import ssl
import geopy.geocoders

DB_FILE = 'carsharing.sqlite'

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

fake = Faker()
api = Flask(__name__)
rest_api = Api(api)

api.config.SWAGGER_UI_OPERATION_ID = True
api.config.SWAGGER_UI_REQUEST_DURATION = True

test = rest_api.model('Test', {'condition': fields.String("Condition...")})


@api.before_first_request
def init_db():
    logging.info("Try to connect to database")
    conn = create_connection(DB_FILE)
    logging.info("Try to initialise tables in database")
    create_table(conn, "tables_to_create.sql")
    fill_db_with_data(conn)
    logging.info("Try to close connection to database")
    close_connection(conn)


find_car_model = rest_api.model('Find a Car', {
    'colour': fields.String('enter colour'),
    'username': fields.String('enter username'),
    'reg_num': fields.String('enter registration number or it part')
})

cars_load_model = rest_api.model('Statistic of cars load for given week', {
    'date': fields.String("Enter a start date in format YYYY-MM-DD")
})


@rest_api.route('/find_car')
class FindCar(Resource):

    @rest_api.expect(find_car_model)
    @rest_api.doc("first scenario for finding a car")
    def post(self):
        data = request.get_json()
        response = find_car(data)
        search_res = {}
        i = 0
        for answer in response:
            search_res[i] = {'car_id': answer[0],
                             'colour': answer[1],
                             'registration_number': answer[2]}
            i += 1
        return jsonify(search_res)


@rest_api.route('/cars_load')
class CarsLoad(Resource):

    @rest_api.expect(cars_load_model)
    @rest_api.doc("2nd scenario for getting statistic of load of car")
    def post(self):
        data = request.get_json(silent=True)
        response = stat_of_busy_cars(data)
        return jsonify(response)


if __name__ == '__main__':
    api.run()

# Example
# ____________________________________________________________#
# @rest_api.route("/select_fake_data")
# class TestSelectFake(Resource):
#
#     @rest_api.doc(id="put something")
#     @rest_api.doc()
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
