CREATE TABLE IF NOT EXISTS charging_station (
  UID                       integer PRIMARY KEY,
  amount_of_available_slots integer     NOT NULL,
  time_of_charging          time        NOT NULL,
  price                     double,
  GPS_location              varchar(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS charging_plugs (
  plug_id    integer PRIMARY KEY,
  shape_plug varchar(20) not null,
  size_plug  int(10)     not null
);

CREATE TABLE IF NOT EXISTS stations_have_plugs (
  station_have_plugs_id integer NOT NULL,
  UID                  integer NOT NULL,
  plug_id              integer NOT NULL,
  FOREIGN KEY (UID) references charging_station (UID) ON UPDATE  cascade ON DELETE cascade ,
  FOREIGN KEY (plug_id) references charging_plugs (plug_id) ON UPDATE cascade ON DELETE cascade ,
  PRIMARY KEY (station_have_plugs_id)

);

CREATE TABLE IF NOT EXISTS provider (
  company_id   integer PRIMARY KEY,
  address      varchar(25) NOT NULL,
  phone_number varchar(25),
  name_company varchar(25)

);
CREATE TABLE IF NOT EXISTS customers (
  username     varchar(20) PRIMARY KEY,
  email        varchar(20) not null,
  cardnumber   varchar(20) not null,
  fullname     varchar(50) not null,
  phone_number varchar(15),
  zip          integer     not null,
  address varchar(50) not null


);
/* TODO cost and duration?
 TODO st_point, pick location same?*/

CREATE TABLE IF NOT EXISTS orders (
  order_id     integer PRIMARY KEY,
  date         date        not null,
  time         date        not null,
  date_closed  date        not null,
  duration     integer,
  status       varchar(10) not null,
  cost         integer,
  st_point     varchar(50) not null,
  destination  varchar(50) not null,
  car_location varchar(50) not null,
  username     varchar(50) not null,
  car_id       integer     not null,
  foreign key (username) references customers (username) ON UPDATE cascade ON DELETE cascade ,
  foreign key (car_id) references cars (car_id) ON UPDATE cascade ON DELETE cascade
);
/*TODO car_id is model_id???*/
CREATE TABLE IF NOT EXISTS cars (
  car_id       integer primary key,
  gps_location varchar(25) not null,
  year         varchar(4),
  colour       varchar(20) not null,
  reg_num      varchar(11) not null,
  charge       int(1)      not null,
  available    int(1)      not null,
  model_id     int         not null,
  foreign key (model_id) references models (model_id) ON UPDATE cascade ON DELETE set default
);

CREATE TABLE IF NOT EXISTS charge_car_history (
  charge_car_id integer PRIMARY KEY,
  cost          double,
  date          date,
  car_id        integer,
  UID           integer,
  FOREIGN KEY (car_id) references cars (car_id) ON UPDATE cascade,
  FOREIGN KEY (UID) references charging_station (UID) ON UPDATE cascade ON DELETE cascade
);
/*TODO Availability of timing( What the type?)*/
CREATE TABLE IF NOT EXISTS workshop (
  WID                    integer PRIMARY KEY,
  availability_of_timing time        NOT NULL,
  location               varchar(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS repair_car (
  report_id       integer PRIMARY KEY,
  WID             integer,
  car_id          integer unique,
  date            date,
  progress_status varchar(10),
  FOREIGN KEY (WID) references workshop (WID) ON UPDATE cascade ON DELETE cascade ,
  FOREIGN KEY (car_id) references cars (car_id) ON UPDATE cascade ON DELETE cascade
);
/*TODO: Model_id refers(ссылается) to the car_id???*/

CREATE TABLE IF NOT EXISTS models (
  model_id      integer PRIMARY KEY,
  plug_id       integer,
  name          varchar(20) not null,
  type          varchar(30) not null,
  service_class varchar(30) not null,
  foreign key (plug_id) references charging_plugs (plug_id) ON UPDATE cascade
);
CREATE TABLE IF NOT EXISTS part_order (
  date       date,
  amount     integer,
  cost       double,
  order_id   integer PRIMARY KEY,
  part_id    integer,
  WID        integer,
  company_id integer,
  FOREIGN KEY (part_id) references parts (part_id) ON UPDATE cascade ON DELETE cascade ,
  FOREIGN KEY (WID) references workshop (WID) ON UPDATE cascade ON DELETE cascade ,
  FOREIGN KEY (company_id) references provider (company_id) ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS parts (
  part_id         integer PRIMARY KEY,
  WID             integer,
  type_of_detail  varchar(25),
  cost            double,
  amount          integer,
  amount_week_ago integer,
  FOREIGN KEY (WID) references workshop (WID) ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS fit (
  fit_id   integer PRIMARY KEY,
  part_id  integer,
  model_id integer,
  FOREIGN KEY (part_id) references parts (part_id) ON UPDATE cascade ON DELETE cascade ,
  FOREIGN KEY (model_id) references models (model_id) ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS providers_have_parts (
  providers_have_parts_id integer PRIMARY KEY,
  company_id              integer,
  part_id                 integer,
  FOREIGN KEY (company_id) references provider (company_id) ON UPDATE cascade ON DELETE cascade,
  FOREIGN KEY (part_id) references parts (part_id) ON UPDATE cascade ON DELETE cascade
);