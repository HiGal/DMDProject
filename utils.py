import faker
import random
import datetime
from db_management import *

fake = faker.Faker("en_US")
logging.getLogger().setLevel(logging.INFO)

# Lists for storing data
users = []
plugs = []
cars = []
models = []
stations = []
parts = []
workshops = []
company = []
orders = []
# Lists for generation data
colors = ["red", "yellow", "green", "blue", "black", "white"]
reg_name = ["AN", "ER", "TC", "NZ", "FG", "AZ", "MG"]
type_car = ["Hatchback", "Sedan", "Crossover", "Coupe", "Convertible"]
service_class_car = ["comfort", "economy", "business "]
name_car = ["Chevy Sonic", "Ford Fiesta", "Honda Fit", "Mitsubishi Mirage", "Kia Rio"]


def generate_time():
    """
    Method to generate random time
    :return: Two variables of type date: star rime of order and time of destination
    """
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
    time_start = a + ":" + str(b)
    time_finish = a1 + ":" + b1
    return time_start, time_finish


def fill_customer_table(conn):
    """
    Method for filling the customer table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
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
        # print(task)
        param = "customers(username, email, cardnumber, fullname, phone_number, zip, address)"
        number = "(?,?,?,?,?,?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_orders_table(conn):
    """
    Method for filling orders table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    num = 0
    for k in range(8, 11):
        for j in range(1, 30):
            date = datetime.date(2018, k, j)
            for i in range(10):
                status = "closed"
                timestart, time = generate_time()
                start = fake.local_latlng(country_code="US", coords_only=True)
                finish = fake.local_latlng(country_code="US", coords_only=True)
                task = (date, timestart,
                        random.randint(5, 75),
                        random.randint(5, 69),
                        status,
                        random.randint(1000, 9999),
                        start[0] + " " + start[1],
                        finish[0] + " " + finish[1],
                        random.randint(1, 16),
                        users[random.randint(0, len(users) - 1)][0],
                        cars[random.randint(0, len(cars) - 1)])
                # print(task)
                orders.append((num + 1, date))
                num = num + 1
                param = "orders(date, time, duration, order_distance, status, cost, starting_point, destination, car_distance, username,car_id )"
                number = "(?,?,?,?,?,?,?,?,?,?,?)"
                insert_into_table(conn, task, param, number)
    return 0


def fill_transactions_table(conn):
    """
    Method for filling the table of payments
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for ord in orders:
        task = (ord[0], ord[1], "closed")
        param = "transactions(order_id, date, status)"
        number = "(?,?,?)"
        if insert_into_table(conn, task, param, number) == -1:
            return -1
        if random.randint(0, 4) == 1:
            insert_into_table(conn, task, param, number)
    return 0


def fill_plugs_table(conn):
    """
    Method for filling plugs table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    # create parameters for plugs
    for i in range(5):
        shape_of_plugs = random.randint(100, 999)
        size_of_plug = random.randint(100, 999)
        task = (shape_of_plugs, size_of_plug)
        plugs.append(i + 1)
        # print(task)
        param = "charging_plugs(shape_plug, size_plug)"
        number = "(?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_providers_table(conn):
    """
    Method for filling providers table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for i in range(5):
        address = str(fake.address()).replace('\n', '')
        phone_number = random.randint(1000000000000000, 9999999999999999)
        name_company = fake.company()
        task = (address, phone_number, name_company)
        # print(task)
        param = "provider(address, phone_number, name_company)"
        number = "(?,?,?)"
        company.append(i + 1)
        insert_into_table(conn, task, param, number)
    return 0


def fill_parts_table(conn):
    """
    Method for filling parts table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for i in range(5):
        type_of_detail = random.randint(100, 999)
        cost = random.randint(100, 1200)
        task = (type_of_detail, cost)
        # print(task)
        parts.append(i + 1)
        param = "parts(type_of_detail,cost)"
        number = "(?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_workshops_table(conn):
    """
    Method for filling workshop table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for i in range(5):
        availability_of_timing = random.randint(0, 8)
        location = fake.local_latlng(country_code="US", coords_only=True)
        task = (availability_of_timing,
                location[0] + " " + location[1])
        # print(task)
        workshops.append(i + 1)
        param = "workshop(availability_of_timing, location)"
        number = "(?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_workshops_have_part(conn):
    """
    Method for filling table of relation: workshops have parts
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for wshop in workshops:
        for par in parts:
            amount = random.randint(3, 25)
            amount_week_ago = random.randint(23, 50)
            task = (par,
                    wshop,
                    amount,
                    amount_week_ago)
            # print(task)
            param = "workshop_have_parts(part_id, WID, amount, amount_week_ago)"
            number = "(?,?,?,?)"
            insert_into_table(conn, task, param, number)
    return 0


def fill_charging_stations(conn):
    """
    Method for filling the charging stations table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for i in range(5):
        gps = fake.local_latlng(country_code="US", coords_only=True)
        task = (random.randint(5, 15),
                gps[0] + " " + gps[1])
        stations.append(i + 1)
        # print(task)
        param = "charging_station(time_of_charging, GPS_location)"
        number = "(?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_stations_have_plugs(conn):
    """
    Method for filling the table of relation: charging stations have plugs
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for j in stations:
        for i in plugs:
            amount_of_available_slots = random.randint(3, 10)
            task = (j, i, amount_of_available_slots)
            # print(task)
            param = "stations_have_plugs(UID, plug_id,amount_of_available_slots)"
            number = "(?,?,?)"
            insert_into_table(conn, task, param, number)
    return 0


def fill_charge_car_history(conn):
    """
    Method for filling the charge car history table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for k in range(8, 11):
        for j in range(1, 30):
            date = datetime.date(2018, k, j)
            for i in range(20):
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
                # print(task)
                param = "charge_car_history(cost, date, start_time, finish_time, car_id, UID)"
                number = "(?,?,?,?,?,?)"
                insert_into_table(conn, task, param, number)
    return 0


def fill_models_table(conn):
    """
    Method for filling the models table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
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
        # print(task)
        param = "models(plug_id, name, type, service_class) "
        number = "(?,?,?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_cars_table(conn):
    """
    Method for filling the cars table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    # create parameters of cars
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
        # print(task)
        param = "cars(gps_location, year, colour, reg_num, charge, available, model_id)"
        number = "(?,?,?,?,?,?,?)"
        insert_into_table(conn, task, param, number)
    return 0


def fill_part_order_history(conn):
    """
    Method for filling part order history
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for i in range(8, 11):
        for j in range(1, 30):
            date = datetime.date(2018, i, j)
            for k in range(10):
                amount = random.randint(0, 15)
                cost = random.randint(100, 650)
                task = (date,
                        amount,
                        cost,
                        parts[random.randint(0, len(parts) - 1)],
                        workshops[random.randint(0, len(workshops) - 1)],
                        company[random.randint(0, len(company) - 1)])
                # print(task)
                param = "part_order_history(date,amount,cost,part_id, WID, CID)"
                number = "(?,?,?,?,?,?)"
                insert_into_table(conn, task, param, number)
    return 0


def fill_repair_car_table(conn):
    """
    Method for filling the reparation car table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for k in range(8, 11):
        for j in range(1, 30):
            date = datetime.date(2018, k, j)
            for i in range(10):
                wid = workshops[random.randint(0, len(workshops) - 1)]
                car_id = cars[random.randint(0, len(cars) - 1)]
                cost = random.randint(150, 450)
                task = (wid, car_id, date, cost, "closed")
                # print(task)
                param = "repair_car(WID, car_id, date, cost, progress_status)"
                number = "(?,?,?,?,?)"
                insert_into_table(conn, task, param, number)
    return 0


def fill_fit_table(conn):
    """
    Method for filling the fit parts to models table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for mod in models:
        for par in parts:
            task = (par, mod)
            # print(task)
            param = "fit(part_id, model_id)"
            number = "(?, ?)"
            insert_into_table(conn, task, param, number)
    return 0


def fill_providers_have_parts(conn):
    """
    Method for filling relation: providers have parts table
    :param conn: Database connection
    :return: 0: table has filled, otherwise -1
    """
    for pro in company:
        for par in parts:
            task = (pro, par)
            param = "providers_have_parts(CID, part_id)"
            number = "(?, ?)"
            insert_into_table(conn, task, param, number)
    return 0


def fill_db_with_data(conn):
    """
        Method for filling database of the system
        :param conn: Database connection
        """
    try:
        fill_plugs_table(conn)
        fill_charging_stations(conn)
        fill_stations_have_plugs(conn)
        fill_models_table(conn)
        fill_cars_table(conn)
        fill_charge_car_history(conn)
        fill_customer_table(conn)
        fill_orders_table(conn)
        fill_transactions_table(conn)
        fill_parts_table(conn)
        fill_providers_table(conn)
        fill_workshops_table(conn)
        fill_workshops_have_part(conn)
        fill_part_order_history(conn)
        fill_repair_car_table(conn)
        fill_fit_table(conn)
        fill_providers_have_parts(conn)
        return 0
    except sqlite3.Error:
        logging.info("Filling database failed")
        drop_table(conn, "to_drop.sql")
        logging.info("Drop all tables")
    return -1
