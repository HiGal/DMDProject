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


def fill_db_with_data(conn):
    geolocator = Nominatim(user_agent="dmd_project")
    users = []
    plugs = []
    cars = []
    models =[]
    colors = ["red", "yellow", "green", "blue", "black", "white"]
    reg_name = ["AN", "ER", "TC", "NZ", "FG", "AZ", "MG"]
    type_car = ["Hatchback", "Sedan", "Crossover", "Coupe", "Convertible"]
    service_class_car = ["comfort", "economy", "business "]
    name_car = ["Chevy Sonic", "Ford Fiesta", "Honda Fit", "Mitsubishi Mirage", "Kia Rio"]

    # create parameters for plugs
    for i in range(5):
        shape_of_plugs = random.randint(100, 999)
        size_of_plug = random.randint(100, 999)
        task = (shape_of_plugs, size_of_plug)
        plugs.append(i)
        print(task)
        # insert_into_plugs(conn, task)

    #create parameters of models
    for i in range(5):
        type = type_car[random.randint(0,len(type_car) - 1)]
        service_of_class = service_class_car[random.randint(0, len(service_class_car) - 1)]
        name = name_car[random.randint(0, len(name_car) - 1)]
        task = (plugs[i // len(plugs)], name, type, service_of_class)
        models.append(i)
        print(task)
        #insert_into_models(conn, task)

    #fill car table
    for i in range(10):
        location = geolocator.reverse(random.uniform(40.1, 41.1), random.uniform(-74.4, -73.8))
        gps_location = str(location.latitude) + " " + str(location.longitude)
        year = random.randint(1985,2012)
        regnum = reg_name[i//len(reg_name)] + str(random.randint(1000, 9999))
        task = (gps_location,
                year,
                colors[i//len(colors)],
                regnum,
                random.randint(10,99),
                "available",
                models[i // len(models)])
        print(task)
        # insert_into_cars(conn, task)

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
        # insert_into_customers(conn, task)

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
                start, finish, car_loc, users[i // len(users)][0], users[i // len(cars)][0])
        print(task)
        # insert_into_orders(conn, task)
    pass
