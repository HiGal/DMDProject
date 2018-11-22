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
        insert_into_customers(conn, task)


def fill_orders_table(conn):
    geolocator = Nominatim(user_agent="d_project")
    for i in range(10):
        date = datetime.date.today()
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
        insert_into_orders(conn, task)


def fill_db_with_data(conn):
    fill_customer_table(conn)
    fill_orders_table(conn)
    pass
