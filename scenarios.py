from db_management import create_connection, close_connection
from collections import defaultdict
import logging

DB_FILE = 'carsharing.sqlite'


def find_car(data):
    """
    Method that search a car for given parameters
    :param data: json file which contains date of the order, colour and registration
                 number  of the car and username
    :return: list of tuples of the car id, colour, registration number
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    try:
        sql = '''SELECT cars.car_id,colour,reg_num 
        from cars,orders 
        where cars.car_id=orders.car_id and  date = '{}' AND colour = '{}' 
        AND username = '{}' AND reg_num LIKE '%{}%';''' \
        .format(data['date'], data['colour'], data['username'], data['reg_num'])

        cursor.execute(sql)
        response = cursor.fetchall()
        close_connection(conn)
        return response
    except Exception:
        logging.info("Error")
    return "Error while searching was occured"

def stat_least_amount_cars():
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    try:
        cars_id =[]
        least_car_id = '''SELECT car_id FROM orders GROUP BY (car_id) 
        ORDER BY count(*) LIMIT (SELECT DISTINCT count(car_id)/10 FROM cars)'''
        cursor.execute(least_car_id)
        cars = cursor.fetchall()
        close_connection(conn)

        for car in cars:
            cars_id.append(car[0])
        response = {"cars_id": cars_id}
        return response
    except Exception:
        logging.info("Error")
    return "Error while searching was occured"

def stat_of_busy_cars(data):
    """
    :param data: json file which contains start date to calculate statistic
    :return: load of cars in percentage by 1 week in different daytime periods
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    date = data['date']

    try:
        sql_cnt_cars = '''SELECT count(DISTINCT cars.car_id)
                 from cars
              '''
        morning_load = '''SELECT DISTINCT car_id,date, date('{}','+7 day') as date_end
                          FROM orders where time >='07:00' and time <= '10:00' 
                          AND date>='{}' AND date <= date_end
                       '''.format(date, date)
        afternoon_load = '''
                          SELECT DISTINCT car_id, date, date('{}','+7 day') as date_end
                          FROM orders where time >='12:00' and time <= '14:00' 
                          AND date>='{}' AND date <= date_end
                         '''.format(date, date)
        evening_load = '''
                          SELECT DISTINCT car_id, date, date('{}','+7 day') as date_end
                          FROM orders where time >='17:00' and time <= '19:00' 
                          AND date='{}' AND date <= date_end
                       '''.format(date, date)
        cursor.execute(sql_cnt_cars)
        close_connection(conn)
        cnt = cursor.fetchall()[0][0] * 7
        morning_load = len(cursor.execute(morning_load).fetchall()) / cnt * 100
        afternoon_load = len(cursor.execute(afternoon_load).fetchall()) / cnt * 100
        evening_load = len(cursor.execute(evening_load).fetchall()) / cnt * 100
        response = {'Morning': morning_load,
                    'Afternoon': afternoon_load,
                    'Evening': evening_load}
        return response
    except Exception:
        logging.info("Error")
    return "Error while searching was occured"

def top_locations_search():
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    try:

        morning_start_load = '''SELECT starting_point FROM orders WHERE time >= '07:00' and time <= '10:00' 
        GROUP BY starting_point ORDER BY count(starting_point) DESC LIMIT 3 '''

        morning_finish_load = '''SELECT destination FROM orders WHERE time >= '07:00' and time <= '10:00'
         GROUP BY destination ORDER BY count(destination) DESC LIMIT 3'''

        afternoon_start_load = '''SELECT starting_point FROM orders WHERE time >= '12:00' and time <= '14:00' 
                GROUP BY starting_point ORDER BY count(starting_point) DESC LIMIT 3 '''

        afternoon_finish_load = '''SELECT destination FROM orders WHERE time >= '12:00' and time <= '14:00' 
                        GROUP BY destination ORDER BY count(destination) DESC LIMIT 3 '''

        evening_start_load = '''SELECT starting_point FROM orders WHERE time >= '17:00' and time <= '19:00' 
                        GROUP BY starting_point ORDER BY count(starting_point) DESC LIMIT 3 '''

        evening_finish_load = '''SELECT destination FROM orders WHERE time >= '17:00' and time <= '19:00' 
                                GROUP BY destination ORDER BY count(destination) DESC LIMIT 3 '''

        def fetch_load(query):
            cursor.execute(query)
            return [x[0] for x in cursor.fetchall()]

        top_morning_start_point = fetch_load(morning_start_load)

        top_morning_finish_point = fetch_load(morning_finish_load)

        top_afternoon_start_point = fetch_load(afternoon_start_load)

        top_afternoon_finish_point = fetch_load(afternoon_finish_load)

        top_evening_start_point = fetch_load(evening_start_load)

        top_evening_finish_point = fetch_load(evening_finish_load)

        close_connection(conn)

        response = {
            "Morning": {
                "Start": top_morning_start_point,
                "Finish": top_morning_finish_point,
            },
            "Afternoon": {
                "Start": top_afternoon_start_point,
                "Finish": top_afternoon_finish_point,
            },
            "Evening": {
                "Start": top_evening_start_point,
                "Finish": top_evening_finish_point,
            },
        }
        return response
    except Exception:
        logging.info("Error")
    return "Error while searching was occured"

def efficiency_ch_stations(data):
    """
    Method that calculate efficiency of charging station utilization for given date
    :param data: json file which contains date
    :return: returns list of charging stations and how many times they were used hourly
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    date = data['date']
    response = defaultdict(dict)
    for i in range(0, 24):
        st_time = ''
        end_time = ''
        if i < 9:
            st_time = '0{}:00'.format(i)
            end_time = '0{}:00'.format(i + 1)
            sql = '''SELECT UID,count(charge_car_id)
                     FROM charge_car_history where start_time >= '{}'  and start_time< '{}'
                     and date='{}'
                     group by UID;
                  '''.format(st_time, end_time, date)
        elif i == 9:
            st_time = '0{}:00'.format(i)
            end_time = '{}:00'.format(i + 1)
            sql = '''SELECT UID,count(charge_car_id)
                     FROM charge_car_history where start_time>='09:00' and start_time<'10:00'
                     and date='{}'
                     group by UID;
                  '''.format(date)
        else:
            st_time = '{}:00'.format(i)
            end_time = '{}:00'.format(i + 1)
            sql = '''SELECT UID,count(charge_car_id)
                     FROM charge_car_history where start_time >= '{}' and start_time<'{}' 
                     and date='{}'
                     group by UID;
                  '''.format(st_time, end_time, date)
        cursor.execute(sql)
        data = cursor.fetchall()

        for value in data:
            response[value[0]][st_time + "-" + end_time] = value[1]

    close_connection(conn)
    for i in range(0, 24):
        st_time = ''
        end_time = ''
        s = defaultdict(dict)
        if i < 9:
            st_time = '0{}:00'.format(i)
            end_time = '0{}:00'.format(i + 1)
        elif i == 9:
            st_time = '0{}:00'.format(i)
            end_time = '{}:00'.format(i + 1)
        else:
            st_time = '{}:00'.format(i)
            end_time = '{}:00'.format(i + 1)
        for residual in response.keys():
            if (st_time + "-" + end_time) not in response[residual].keys():
                response[residual][st_time + "-" + end_time] = 0
    for residual in response.keys():
        s[residual] = sorted(response[residual].items())
    return s


def search_duplicates(data):
    username = data['username']
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    import datetime

    date_month_ago = '2018-09-29'

    # It's also work but for well-looked (big table) result we defined month by our hands
    # date_month_ago = (datetime.datetime.now() - datetime.timedelta(30)).date()

    try:
        sql = '''SELECT b.date, b.cost
                  FROM (select order_id from 
                  (SELECT order_id, COUNT(*) FROM transactions GROUP BY order_id HAVING COUNT(*) > 1))as a
                  inner join
                   (select order_id, date, cost from orders where username = '{}' and date > '{}') as b 
                   on a.order_id = b.order_id;'''.format(username, date_month_ago)
        cursor.execute(sql)
        response = cursor.fetchall()
        close_connection(conn)
        return response
    except Exception:
        logging.info("Error")
    return "No such username"


def trip_duration(data):
    date = data['date']
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    try:
        sql = "select avg(duration) from orders where date = '{}'".format(date)
        cursor.execute(sql)
        response = cursor.fetchall()[0]
        close_connection(conn)
        return response
    except Exception:
        logging.info("Error")
    return "There is no orders for such period"


def average_distance(data):
    date = data['date']
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    try:
        sql = "select avg(car_distance) from orders where date = '{}'".format(date)
        cursor.execute(sql)
        response = cursor.fetchall()[0]
        close_connection(conn)
        return response
    except Exception:
        logging.info("Error")
    return "There is no orders for such period"


def times_using_ch_station(data):
    """
    Method that calculate how many times charging station was used by user
    :param data: json file which contain start date
    :return: how many times user used charging station in his orders
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    sql = '''select count(car_id) as charging_times,username
             from(select charge_car_history.date, date('{}','+1 month') as end_period,orders.car_id,username
             from charge_car_history,orders
             where orders.car_id = charge_car_history.car_id and charge_car_history.date = orders.date
             and start_time between orders.time and time(orders.time,'+'|| cast(orders.duration as text)||' minutes'))
             group by username;'''.format(data['start_date'])
    cursor.execute(sql)
    response = {}
    for info in cursor.fetchall():
        response[info[1]] = info[0]
    close_connection(conn)
    return response


def most_relevant_part_by_workshop():
    """
    Method that returns the most relevant part that workshop needs
    :return: type of detail that separate workshop needs mostly.
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    sql = '''select type_of_detail, WID
            from(select part_id, WID , MAX(amount_week_ago - amount) as diff
            from workshop_have_parts
            group by  WID) as s, parts
            where s.part_id = parts.part_id
          '''
    cursor.execute(sql)
    response = {}
    for info in cursor.fetchall():
        response[info[1]] = info[0]
    close_connection(conn)
    return response


def most_expensive_car():
    """
    Method that can help to decide which type of car is the most expensive
    :return: the most expensive type of car in usage
    """
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()
    sql = '''select AVG(average_per_day) as average,type
            from (select AVG(repair_avg) + AVG(charge_avg) as average_per_day, charge.car_id from
              (select AVG(repair_car.cost) as repair_avg, date, car_id
              from repair_car
              group by date,car_id )as repair
            join
              (select AVG(charge_car_history.cost) as charge_avg,date, car_id
              from charge_car_history
              group by date,car_id ) as charge
            on repair.car_id = charge.car_id
            group by charge.car_id) as s,cars, models
            where cars.car_id = s.car_id and cars.model_id = models.model_id
            group by type
            order by average desc
    '''
    cursor.execute(sql)
    s = cursor.fetchall()
    response = {s[0][1]: s[0][0]}
    close_connection(conn)
    return response
