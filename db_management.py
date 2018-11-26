from faker import Faker
import sqlite3
import logging

fake = Faker()

DB_FILE = 'carsharing.sqlite'
logging.getLogger().setLevel(logging.INFO)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        logging.error("Successfully connected to database")
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


def drop_table(conn, to_drop_file):
    """ drop a table from the to_drop_sql statement
    :param conn: Connection object
    :param to_drop_file: a DROP TABLE statement
    :return:
    """
    try:
        with open(to_drop_file) as f:
            script = f.read()
        c = conn.cursor()
        c.executescript(script)
        conn.commit()
        logging.info("Successfully flushed tables in database")

    except sqlite3.DatabaseError as e:
        print(e)


def insert_into_table(conn, task, param, number):
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO " + param + " VALUES" + number
        cursor.execute(sql, task)
        conn.commit()
        return 0
    except sqlite3.DatabaseError:
        logging.info("Error while inserting into customers occurs")
    return -1
