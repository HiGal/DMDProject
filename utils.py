from faker import Faker
import random
import certifi
import ssl
from geopy.geocoders import Nominatim
import geopy.geocoders
import datetime
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

fake = Faker()


def fill_db_with_data(conn):
    users = []
    plugs = []
    cars = []
    # create parameters for plugs
    for i in range(5):
        shape_of_plugs = random.randint(100, 999)
        size_of_plug = random.randint(100, 999)
        task = (shape_of_plugs, size_of_plug)
        plugs.append(task)
        print(task)
        # insert_into_plugs(conn, task)

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
        # insert_into_customers(conn, task)
    geolocator = Nominatim(user_agent="dmd_project")
    for i in range(10):
        date = datetime.date.today()
        status = "closed"
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        start = str(location.latitude) + " " + str(location.longitude)
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        finish = str(location.latitude) + " " + str(location.longitude)
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        car_loc = str(location.latitude) + " " + str(location.longitude)
        task = (date, timestamp, timestamp, status,
                random.randint(1000, 9999),
                start, finish, car_loc, users[i // len(users)][0], 1)
        print(task)
        # insert_into_customers(conn, task)
    pass
