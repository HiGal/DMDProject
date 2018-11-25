from db_management import create_connection, close_connection
from collections import defaultdict
import logging
import datetime

DB_FILE = 'carsharing.sqlite'


def find_car(data):
    conn = create_connection(DB_FILE)
    cursor = conn.cursor()

    try:
        sql = '''SELECT cars.car_id,colour,reg_num 
        from cars,orders 
        where cars.car_id=orders.car_id AND colour = '{}' AND username = '{}' AND reg_num LIKE '%{}%';''' \
            .format(data['colour'], data['username'], data['reg_num'])
        cursor.execute(sql)
        response = cursor.fetchall()
        close_connection(conn)
        return response
    except Exception:
        logging.info("Error")
    return "Not such car"


def stat_of_busy_cars(data):
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
    return "There is no orders for such period"


def efficiency_ch_stations(data):
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

    date_month_ago ='2018-09-29'

    #It's also work but for well-looked (big table) result we defined month by our hands
    #date_month_ago = (datetime.datetime.now() - datetime.timedelta(30)).date()

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
