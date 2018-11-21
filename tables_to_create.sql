CREATE TABLE IF NOT EXISTS tasks (
  id       integer UNIQUE PRIMARY KEY,
  name     varchar(50) NOT NULL,
  priority integer,
  end_date date        NOT NULL
);

CREATE TABLE IF NOT EXISTS charging_station (
  UID                       integer UNIQUE PRIMARY KEY,
  amount_of_available_slots integer                  NOT NULL,
  time_of_charging          time                     NOT NULL,
  price                     double
                            GPS_location varchar(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS charging_plugs (
  plug_id    integer PRIMARY KEY,
  shape_plug varchar(20) not null,
  size_plug  int(10)     not null
);

CREATE TABLE IF NOT EXISTS charging_have_plugs (
  charge_have_plugs_id integer NOT NULL,
  UID                  integer NOT NULL,
  plug_id              integer NOT NULL,
  FOREIGN KEY (UID) references charging_station (UID),
  FOREIGN KEY (plug_id) references charging_plugs (plug_id),
  PRIMARY KEY (charge_have_plugs_id)
);

CREATE TABLE IF NOT EXISTS provider (
  company_id   integer PRIMARY KEY,
  address      varchar(25) NOT NULL,
  phone_number varchar(25),
  name_company varchar(25)

);