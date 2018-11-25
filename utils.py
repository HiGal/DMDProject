import faker
import random
import datetime
from db_management import *

fake = faker.Faker("en_US")

users = []
plugs = []
cars = []
models = []
stations = []
parts = []
workshops = []
colors = ["red", "yellow", "green", "blue", "black", "white"]
reg_name = ["AN", "ER", "TC", "NZ", "FG", "AZ", "MG"]
type_car = ["Hatchback", "Sedan", "Crossover", "Coupe", "Convertible"]
service_class_car = ["comfort", "economy", "business "]
name_car = ["Chevy Sonic", "Ford Fiesta", "Honda Fit", "Mitsubishi Mirage", "Kia Rio"]

progress_status = ["in progress", "opened", "closed"]

def generate_time():
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
    b = random.randint(10, 30)
    b1 = str(b + random.randint(0, 25))
    timestart = a + ":" + str(b)
    timefinish = a1 + ":" + b1
    return timestart, timefinish


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
            timestart, timefinish = generate_time()
            start = fake.local_latlng(country_code="US", coords_only=True)
            finish = fake.local_latlng(country_code="US", coords_only=True)
            car_loc = fake.local_latlng(country_code="US", coords_only=True)
            task = (date, timestart, timefinish, status,
                    random.randint(1000, 9999),
                    start[0] + " " + start[1],
                    finish[0] + " " + finish[1],
                    car_loc[0] + " " + car_loc[1],
                    users[random.randint(0, len(users) - 1)][0],
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


def fill_providers_table(conn):
    for i in range(5):
        address = str(fake.address()).replace('\n', '')
        phone_number = random.randint(1000000000000000, 9999999999999999)
        name_company = fake.company()
        task = (address, phone_number, name_company)
        print(task)
        param = "provider(address, phone_number, name_company)"
        number = "(?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_parts_table(conn):
    for i in range(5):
        type_of_detail = random.randint(100, 999)
        cost = random.randint(100, 1200)
        task = (type_of_detail, cost)
        print(task)
        parts.append(i + 1)
        param = "parts(type_of_detail,cost)"
        number = "(?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
        return 0


def fill_workshops_table(conn):
    for i in range(5):
        availability_of_timing = random.randint(0, 8)
        location = fake.local_latlng(country_code="US", coords_only=True)
        task = (availability_of_timing,
                location[0] + " " + location[1])
        print(task)
        workshops.append(i + 1)
        param = "workshop(availability_of_timing, location)"
        number = "(?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_workshops_have_part(conn):
    for i in range(25):
        amount = random.randint(3, 25)
        amount_week_ago = random.randint(3, 25)
        task = (parts[random.randint(0, len(parts) - 1)],
                workshops[random.randint(0, len(workshops) - 1)],
                amount,
                amount_week_ago)
        param = "workshop_have_parts(part_id, WID, amount, amount_week_ago)"
        number = "(?,?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_charging_stations(conn):
    for i in range(5):
        GPS = fake.local_latlng(country_code="US", coords_only=True)
        task = (random.randint(5, 15),
                GPS[0] + " " + GPS[1])
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
            timestart, timefinish = generate_time()
            car_charging = cars[random.randint(0, len(cars) - 1)]
            station = stations[random.randint(0, len(stations) - 1)]
            task = (cost,
                    date,
                    timestart,
                    timefinish,
                    car_charging,
                    station)
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
        task = (plugs[random.randint(0, len(plugs) - 1)],
                name,
                type,
                service_of_class)
        models.append(i + 1)
        print(task)
        param = "models(plug_id, name, type, service_class) "
        number = "(?,?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0


def fill_cars_table(conn):
    # fill car table
    for i in range(10):
        gps_location = fake.local_latlng(country_code="US", coords_only=True)
        year = random.randint(1990, 2012)
        regnum = reg_name[i // len(reg_name)] + str(random.randint(1000, 9999))
        task = (gps_location[0] + " " + gps_location[1],
                year,
                colors[random.randint(0, len(colors) - 1)],
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
    for i in range(10):
        task = ()
        parts.append(i + 1)
        print(task)
        param = ""
        number = ""
        if insert_into_table(conn, task, param, number) == -1:
            return -1
    return 0

def fill_repair_car_table(conn):
    for j in range(1, 30):
        date = datetime.date(2018, 10, j)
        for i in range(5):
            WID = workshops[random.randint(0, len(workshops) - 1)]
            car_id = cars[random.randint(0, len(cars) - 1)]
            progress_status_car = progress_status[random.randint(0, len(progress_status) - 1)]
            task = (WID, car_id, date, progress_status_car)
            print(task)
            param = "repair_car(WID, car_id, date, progress_status)"
            number = "(?,?,?,?)"
            if insert_into_table(conn, task, param, number) == -1:
                return -1
    return 0


def fill_part_order_history():
    for i in range(0, 30):
        task = (date,
                amount,
                cost,
                part_id,
                WID,
                CID)


def fill_db_with_data(conn):
    fill_plugs_table(conn)
    fill_charging_stations(conn)
    fill_stations_have_plugs(conn)
    fill_models_table(conn)
    fill_cars_table(conn)
    fill_charge_car_history(conn)
    fill_customer_table(conn)
    fill_orders_table(conn)
    fill_parts_table(conn)
    fill_providers_table(conn)
    fill_workshops_table(conn)
    fill_repair_car_table(conn)
    pass
