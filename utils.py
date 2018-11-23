from faker import Faker
import random
import certifi
import ssl
from geopy.geocoders import Nominatim
import geopy.geocoders
import datetime
from db_management import *

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
geolocator = Nominatim(user_agent="d_project")
fake = Faker()

users = []
plugs = []
cars = []
models = []
stations = []
colors = ["red", "yellow", "green", "blue", "black", "white"]
reg_name = ["AN", "ER", "TC", "NZ", "FG", "AZ", "MG"]
type_car = ["Hatchback", "Sedan", "Crossover", "Coupe", "Convertible"]
service_class_car = ["comfort", "economy", "business "]
name_car = ["Chevy Sonic", "Ford Fiesta", "Honda Fit", "Mitsubishi Mirage", "Kia Rio"]


def fill_customer_table(conn):
    # fill customer table
    for i in range(5):
        address = str(fake.address()).replace('\n', '')
        name = fake.name()
        username = str(name).replace(' ', '').lower()
        email = username + "@gmail.com"
        task = (username,
                email,
                random.randint(1000000000000000, 9999999999999999),
                name,
                random.randint(10000000000, 99999999999),
                random.randint(100000, 999999),
                address
                )
        users.append(task)
        print(task)
        param = "customers(username, email, cardnumber, fullname, phone_number, zip, address)"
        number = "(?,?,?,?,?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_orders_table(conn):
    for j in range(1, 30):
        date = datetime.date(2018, 10, j)
        for i in range(3):
            status = "closed"
            a = random.randint(0, 22)
            a1 = a + 1
            if a < 10:
                a = "0" + str(a)
            else:
                a = str(a)
            if a1 < 10:
                a1 = "0" + str(a1)
            else:
                a1 = str(a1)
            b = random.randint(10, 52)
            b1 = str(b + 5)
            timestart = a + ":" + str(b)
            timefinish = a1 + ":" + b1
            location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
            start = str(location.latitude) + " " + str(location.longitude)
            location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
            finish = str(location.latitude) + " " + str(location.longitude)
            location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
            car_loc = str(location.latitude) + " " + str(location.longitude)
            task = (date, timestart, timefinish, status,
                    random.randint(1000, 9999),
                    start, finish, car_loc, users[random.randint(0, len(users) - 1)][0],
                    cars[random.randint(0, len(cars) - 1)])
            print(task)
            param = "orders(date, time, date_closed, status, cost, st_point, destination, car_location, username,car_id )"
            number = "(?,?,?,?,?,?,?,?,?,?)"
            if insert_into_table(conn, task, param, number) == -1:
                return -1
    return 0


def fill_plugs_table(conn):
    # create parameters for plugs
    for i in range(5):
        shape_of_plugs = random.randint(100, 999)
        size_of_plug = random.randint(100, 999)
        task = (shape_of_plugs, size_of_plug)
        plugs.append(i + 1)
        print(task)
        param = "charging_plugs(shape_plug, size_plug)"
        number = "(?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_charging_stations(conn):
    for i in range(5):
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        GPS = str(location.latitude) + " " + str(location.longitude)
        task = (random.randint(5, 15), GPS)
        stations.append(i + 1)
        print(task)
        param = "charging_station(time_of_charging, GPS_location)"
        number = "(?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_stations_have_plugs(conn):
    for i in range(30):
        amount_of_available_slots = random.randint(3, 10)
        task = (stations[random.randint(0, len(stations) - 1)],
                plugs[random.randint(0, len(plugs) - 1)],
                amount_of_available_slots)
        print(task)
        param = "stations_have_plugs(UID, plug_id,amount_of_available_slots)"
        number = "(?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_charge_car_history(conn):
    for j in range(1, 30):
        date = datetime.date(2018, 10, j)
        for i in range(5):
            cost = random.randint(100, 1200)
            a = random.randint(0, 22)
            a1 = a + 1
            if a <10:
                a = "0" + str(a)
            else:
                a = str(a)
            if a1 < 10:
                a1 = "0" + str(a1)
            else:
                a1 = str(a1)
            b = random.randint(10, 52)
            b1 = str(b + 5)
            timestart = a + ":" + str(b)
            timefinish = a1 + ":" + b1
            task = (cost, date, timestart, timefinish, cars[random.randint(0, len(cars) - 1)],
                    stations[random.randint(0, len(stations) - 1)])
            print(task)
            param = "charge_car_history(cost, date, start_time, finish_time, car_id, UID)"
            number = "(?,?,?,?,?,?)"
            if insert_into_table(conn, task, param, number) == -1:
                return -1
    return 0


def fill_models_table(conn):
    # create parameters of models
    for i in range(5):
        type = type_car[random.randint(0, len(type_car) - 1)]
        service_of_class = service_class_car[random.randint(0, len(service_class_car) - 1)]
        name = name_car[random.randint(0, len(name_car) - 1)]
        task = (plugs[random.randint(0, len(plugs) - 1)], name, type, service_of_class)
        models.append(i + 1)
        print(task)
        param = "models(plug_id, name, type, service_class) "
        number = "(?,?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_cars_table(conn):
    geolocator = Nominatim(user_agent="dmd_project")
    # fill car table
    for i in range(10):
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        gps_location = str(location.latitude) + " " + str(location.longitude)
        year = random.randint(1990, 2012)
        regnum = reg_name[i // len(reg_name)] + str(random.randint(1000, 9999))
        task = (gps_location,
                year,
                colors[i // len(colors)],
                regnum,
                random.randint(10, 99),
                "available",
                models[random.randint(0, len(models) - 1)])
        cars.append(i + 1)
        print(task)
        param = "cars(gps_location, year, colour, reg_num, charge, available, model_id)"
        number = "(?,?,?,?,?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_parts(conn):
    pass


def fill_db_with_data(conn):
    fill_plugs_table(conn)
    fill_charging_stations(conn)
    fill_stations_have_plugs(conn)
    fill_models_table(conn)
    fill_cars_table(conn)
    fill_charge_car_history(conn)
    fill_customer_table(conn)
    fill_orders_table(conn)
    fill_parts(conn)
    pass
