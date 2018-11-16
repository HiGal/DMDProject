from flask import Flask
import sqlite3

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

sql_create_charging_station_table = """CREATE TABLE IF NOT EXISTS charging_station(
                                  UID integer PRIMARY KEY,
                                  amount_of_available_slots integer NOT NULL,
                                  time_of_charging time NOT NULL, 
                                  price double
                            );"""

sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts(
                                part_id integer PRIMARY KEY, 
                                type_of_detail varchar(25) NOT NULL
                                
                        );"""

sql_create_workshop_table = """CREATE TABLE IF NOT EXISTS workshop(
                                    WID integer PRIMARY KEY ,
                                    availability_of_timing time NOT NULL,
                                    location varchar(25) NOT NULL
                           
                        );"""

sql_create_provider_table = """CREATE TABLE IF NOT EXISTS provider(
                                    company_id integer PRIMARY KEY,
                                    address varchar(25) NOT NULL,
                                    phone_number varchar(25),
                                    name varchar(25)
                                     
                        );"""



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        print("succ")
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
#        c.execute(sql_create_charging_station_table)

    except sqlite3.DatabaseError as e:
        print(e)

def close_connection(conn):
    conn.close()
    return None

@app.route('/')
def hello_world():
    return 'Hello World!'



if __name__ == '__main__':
    conn = create_connection(db_file)
    print(conn)
    create_table(conn, sql_create_tasks_table)
    close_connection(conn)
    app.run()
