from db_management import create_connection, close_connection
import datetime
import logging

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
                       '''.format(date,date)
        cursor.execute(sql_cnt_cars)
        cnt = cursor.fetchall()[0][0] * 7
        morning_load = len(cursor.execute(morning_load).fetchall())/cnt*100
        afternoon_load = len(cursor.execute(afternoon_load).fetchall())/cnt*100
        evening_load = len(cursor.execute(evening_load).fetchall())/cnt*100
        response = {'Morning' : morning_load,
                    'Afternoon': afternoon_load,
                    'Evening': evening_load}
        return response
    except Exception:
        logging.info("Error")
    return "There is no orders for such period"
