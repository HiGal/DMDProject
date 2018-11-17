from flask import Flask
import sqlite3
import os

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
                                            GPS_location varchar(25) NOT NULL 
                            );"""

sql_create_charging_plugs = """CREATE TABLE IF NOT EXISTS charging_plugs(
                                plug_id integer PRIMARY KEY ,
                                shape_plug varchar(20) not null  ,
                                size_plug int(10) not null 
                            );"""

#Так вообще можно делать?
sql_create_have_charging_relation = """CREATE TABLE IF NOT EXISTS have_charging(
                                            UID integer NOT NULL,
                                            plug_id integer NOT NULL,
                                            FOREIGN KEY (UID)  references charging_station(UID),
                                            FOREIGN KEY (plug_id)  references charging_plugs(plug_id),
                                            PRIMARY KEY (UID, plug_id)
                                );"""


sql_create_provider_table = """CREATE TABLE IF NOT EXISTS provider(
                                    company_id integer PRIMARY KEY,
                                    address varchar(25) NOT NULL,
                                    phone_number varchar(25),
                                    name_company varchar(25)

                        );"""

sql_create_customers_table = """CREATE TABLE IF NOT EXISTS customers (
                                  username  varchar(20) PRIMARY KEY ,
                                  email  varchar(20) not null ,
                                  cardnumber    varchar(20) not null,
                                  fullname   varchar(50) not null,
                                  phone_number varchar(15),
                                  zip integer not null ,
                                  city varchar(20) not null ,
                                  country varchar(50) not null 

                                  
                        );"""

# cost and duration?
# st_point, pick location same?
sql_create_orders = """CREATE TABLE IF NOT EXISTS orders (
                        order_id integer PRIMARY KEY,
                        date text not null ,
                        time text not null ,
                        date_closed text not null,
                        duration integer,
                        status varchar(10) not null ,
                        cost integer,
                        st_point varchar(50) not null ,
                        destination varchar(50) not null ,
                        pick_location varchar(50) not null ,
                        car_location varchar(50) not null, 
                        
                        foreign key (order_id) references customers(username)
                        
                    );"""

sql_create_cars = """CREATE TABLE IF NOT EXISTS cars(
                        car_id integer primary key ,
                        gps_location varchar(25) not null ,
                        year varchar(4),
                        reg_num varchar(11) not null ,
                        charge int(1) not null ,
                        available int(1) not null ,
                        
                        foreign key (car_id) references orders(order_id)
    
                    );"""

# Availability of timing( What the type?)
sql_create_workshop_table = """CREATE TABLE IF NOT EXISTS workshop(
                                    WID integer PRIMARY KEY ,
                                    availability_of_timing time NOT NULL,
                                    location varchar(25) NOT NULL

                        );"""

sql_create_repair_car = """CREATE TABLE IF NOT EXISTS repair_car(
                                WID integer,
                                car_id integer, 
                                report_id integer PRIMARY KEY,
                                date date,
                                prograss_status varchar(10),
                                FOREIGN KEY (WID) references workshop(WID),
                                FOREIGN KEY (car_id) references cars(car_id)
                    );"""


sql_create_models = """CREATE TABLE IF NOT EXISTS models(
                        model_id integer PRIMARY KEY ,
                        name varchar(20) not null,
                        type varchar(30) not null ,
                        service_class varchar(30) not null ,
                        
                        foreign key (model_id) references cars(car_id),
                        foreign key (model_id) references charging_plugs(plug_id)
                    );"""

sql_create_part_order_table = """CREATE TABLE IF NOT EXISTS part_order(
                                    date date,
                                    amount integer,
                                    cost double,
                                    order_id integer PRIMARY KEY 
                        );"""

sql_create_parts_table = """CREATE TABLE IF NOT EXISTS parts(
                                part_id integer PRIMARY KEY, 
                                type_of_detail varchar(25) NOT NULL

                        );"""

sql_create_have_parts_table = """CREATE TABLE IF NOT EXISTS have_parts(
                                    
                        );"""

sql_create_fit_table = """CREATE TABLE IF NOT EXISTS fit(
                                part_id integer PRIMARY KEY,
                                model_id integer PRIMARY KEY,
                                FOREIGN KEY (part_id) references parts(part_id),
                                FOREIGN KEY (model_id) references models(model_id)
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
    create_table(conn,'sql_create_tasks_table')
    close_connection(conn)
    app.run()
