from faker import Faker
import sqlite3
import logging

fake = Faker()

DB_FILE = 'carsharing.sqlite'


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


def insert_into_table(conn, task, param, number):
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO " + param + " VALUES"+number
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting into customers occurs")
    return -1


def insert_into_orders(conn, task):
    cursor = conn.cursor()
    try:
        sql = ''' INSERT INTO orders(date, time, date_closed, status,
  cost, st_point, destination, car_location, username,car_id ) VALUES(?,?,?,?,?,?,?,?,?,?) '''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1


def insert_into_plugs(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO charging_plugs(shape_plug, size_plug) VALUES (?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_parts(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO parts(type_of_detail,cost, amount, amount_week_ago) VALUES (?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_providers(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO provider(address, phone_number, name_company) VALUES (?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1

def insert_into_charging_stations(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO charging_station(time_of_charging, GPS_location) VALUES (?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1


def insert_into_stations_have_plugs(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO stations_have_plugs(UID, plug_id,amount_of_available_slots) VALUES (?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1


def insert_into_models(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO models(plug_id, name, type, service_class) VALUES (?,?,?,? )'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1


def insert_into_cars(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO cars(gps_location, year, colour, reg_num, charge, available, model_id) VALUES (?,?,?,?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1


def insert_into_car_history(conn, task):
    cursor = conn.cursor()
    try:
        sql = '''INSERT INTO charge_car_history(cost, date, car_id, UID) VALUES (?,?,?,?)'''
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except Exception:
        logging.info("Error while inserting occurs")
    return -1
