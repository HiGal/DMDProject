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
        if insert_into_customers(conn, task) == -1:
            return -1
    return 0


def fill_orders_table(conn):
    geolocator = Nominatim(user_agent="d_project")
    for j in range(1, 30):
        date = datetime.date(2018, 10, j)
        for i in range(3):
            status = "closed"
            a = random.randint(12, 21)
            b = random.randint(10, 52)
            timestart = str(a) + ":" + str(b)
            timefinish = str(a + 1) + ":" + str(b + 5)
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
            if insert_into_orders(conn, task) == -1:
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
        if insert_into_plugs(conn, task) == -1:
            return -1
    return 0


def fill_charging_stations(conn):
    geolocator = Nominatim(user_agent="m_project")
    # create parameters of models
    for i in range(5):
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        GPS = str(location.latitude) + " " + str(location.longitude)
        task = (random.randint(5, 15), GPS)
        stations.append(i + 1)
        print(task)
        if insert_into_charging_stations(conn, task) == -1:
            return -1
    return 0

def fill_stations_have_plugs(conn):
    for i in range(30):
        amount_of_available_slots = random.randint(3, 10)
        task = (stations[random.randint(0,len(stations)-1)],
                plugs[random.randint(0,len(plugs)-1)],
                amount_of_available_slots)
        print(task)
        if insert_into_stations_have_plugs(conn,task) == -1:
            return -1
    return 0

def fill_charge_car_history(conn):
    for j in range(1,30):
        date = datetime.date(2018, 10, j)
        for i in  range(5):
            cost = random.uniform(100, 999)
            task = (cost, date, cars[random.randint(0, len(cars) - 1)], 1)
            print(task)
            if insert_into_car_history(conn, task) == -1:
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
        if insert_into_models(conn, task) == -1:
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
        if insert_into_cars(conn, task) == -1:
            return -1
    return 0

def fill_db_with_data(conn):
    fill_plugs_table(conn)
    fill_charging_stations(conn)
    fill_stations_have_plugs(conn)
    fill_models_table(conn)
    fill_cars_table(conn)
    fill_charge_car_history(conn)
    fill_customer_table(conn)
    fill_orders_table(conn)
    pass
