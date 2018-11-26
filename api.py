from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from scenarios import *
from utils import *
import certifi
import ssl

DB_FILE = 'carsharing.sqlite'

ctx = ssl.create_default_context(cafile=certifi.where())

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
    'date': fields.String('enter date in format YYYY-MM-DD'),
    'colour': fields.String('enter colour'),
    'username': fields.String('enter username'),
    'reg_num': fields.String('enter registration number or it part')
})

cars_load_model = rest_api.model('Statistic of cars load for given week', {
    'date': fields.String("Enter a start date in format YYYY-MM-DD")
})

efficiency_ch_stations_model = rest_api.model('Efficiency of charging station utilization', {
    'date': fields.String("Enter a date which you want to get statistic")
})

searach_duplicates_model = rest_api.model('Searching duplicates of orders for user', {
    'username': fields.String("Enter username")
})

trip_statistics_model = rest_api.model('Statistics of average car distance and trip duration', {
    'date': fields.String("Enter date to get statistics")
})

chst_utilization_model = rest_api.model('Statistic of charging station utilization by user', {
    'start_date': fields.String("Enter a date in given format YYYY-MM-DD")
})


@rest_api.route('/stat_util')
class EfficiencyUtilization(Resource):

    @rest_api.expect(efficiency_ch_stations_model)
    @rest_api.doc("Second scenario")
    def post(self):
        data = request.get_json()
        response = efficiency_ch_stations(data)
        answer = defaultdict(dict)
        for data in response.keys():
            for list_e in response[data]:
                answer[data][list_e[0]] = list_e[1]

        return jsonify(answer)


@rest_api.route('/find_car')
class FindCar(Resource):

    @rest_api.expect(find_car_model)
    @rest_api.doc("first scenario for finding a car")
    def post(self):
        data = request.get_json()
        response = find_car(data)
        if response is None:
            return "Not such a car"
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
    @rest_api.doc("3rd scenario for getting statistic of load of car")
    def post(self):
        data = request.get_json(silent=True)
        response = stat_of_busy_cars(data)
        return jsonify(response)


@rest_api.route('/search_duplicates')
class SearchDuplicates(Resource):

    @rest_api.expect(searach_duplicates_model)
    @rest_api.doc("4nd scenario for searching duplicates of user's orders")
    def post(self):
        data = request.get_json()
        response = search_duplicates(data)
        search_res = {}
        i = 0
        for answer in response:
            search_res[i] = {'date': answer[1],
                             'cost': answer[0]}
            i += 1
        return jsonify(search_res)


@rest_api.route('/trip_statistics')
class SearchDuplicates(Resource):

    @rest_api.expect(trip_statistics_model)
    @rest_api.doc("5th scenario for trip statistics")
    def post(self):
        data = request.get_json()
        response1 = average_distance(data)
        response2 = trip_duration(data)
        search_res = {'distance': response1,
                      'duration': response2}
        return jsonify(search_res)


@rest_api.route('/stats_of_chst_utilization')
class ChStUtilization(Resource):

    @rest_api.expect(chst_utilization_model)
    @rest_api.doc('8th scenario for charging station utilization by user')
    def post(self):
        data = request.get_json()
        response = times_using_ch_station(data)
        return jsonify(response)


@rest_api.route('/most_relevant_part')
class MostRelevantPart(Resource):

    @rest_api.doc('9th scenario / returns Workshop ID and type of most relevant detail')
    def get(self):
        return jsonify(most_relevant_part_by_workshop())


@rest_api.route("/most_expensive_car_type")
class ExpensiveCar(Resource):

    @rest_api.doc("10th scenario / returns most expensive car type and it's average cost per day")
    def get(self):
        return jsonify(most_expensive_car())

@rest_api.route("/top_locations_search")
class ExpensiveCar(Resource):

    @rest_api.doc("6th scenario")
    def get(self):
        response = top_locations_search()
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
