import sys
from logging.handlers import RotatingFileHandler

from flask import Flask
import sqlite3
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

db_file = 'carsharing.sqlite'

sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks(
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                priority integer,
                                status_id integer NOT NULL,
                                project_id integer NOT NULL,
                                begin_date text NOT NULL,
                                end_date text NOT NULL,
                                FOREIGN KEY (project_id) REFERENCES projects (id)
                            );"""

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        logging.info("Successfully created table in database")
    except sqlite3.DatabaseError as e:
        print(e)

def close_connection(conn):
    conn.close()
    logging.info("Successfully closed connection to database")
    return None

@app.before_first_request
def init_db():
    logging.info("Try to connect to database")
    conn = create_connection(db_file)
    logging.info("Try to initialise tables in database")
    create_table(conn, sql_create_tasks_table)
    conn.commit()
    logging.info("Try to close connection to database")
    close_connection(conn)

@app.route('/')
def hello_world():
    return'Hello World!'



if __name__ == '__main__':
    app.run()

