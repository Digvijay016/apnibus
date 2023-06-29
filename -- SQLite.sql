-- SQLite
SELECT created_on, updated_on, is_deleted, id, bus_number, pos_serial_no, pos_dsn_number, gps_sim_image
FROM bus_bus;

SELECT sql
FROM sqlite_master
WHERE type = 'table' AND name = 'route_historicalcity';

sql
CREATE TABLE "bus_historicalBusRoute" 
(
"created_on" datetime NOT NULL, 
"updated_on" datetime NOT NULL, 
"is_deleted" bool NOT NULL, 
id char(255) NOT NULL ,
    bus_number varchar(255) NOT NULL UNIQUE,
    from_town varchar(255) DEFAULT 'from_town',
    to_town varchar(255) DEFAULT 'to_town',
    departure_time TIME DEFAULT '00:00:00',
    arrival_time TIME DEFAULT '00:00:00', 
"history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
"history_date" datetime NOT NULL, 
"history_change_reason" varchar(100) NULL, 
"history_type" varchar(1) NOT NULL, 
"history_user_id" integer NULL REFERENCES 
"auth_user" ("id") DEFERRABLE INITIALLY DEFERRED)

Create Table bus_BusRoute (
    created_on time NOT NULL,
    updated_on time NOT NULL,
    is_deleted bool NOT NULL,
    id char(255) NOT NULL PRIMARY KEY,
    bus_number varchar(255) NOT NULL UNIQUE,
    from_town varchar(255) DEFAULT 'from_town',
    to_town varchar(255) DEFAULT 'to_town',
    departure_time TIME DEFAULT '00:00:00',
    arrival_time TIME DEFAULT '00:00:00'
)

SELECT * FROM bus_BusRoute

Drop Table bus_historicalBusRoute
Drop Table bus_BusRoute
Drop Table bus_BusRoutetown
Drop Table bus_historicalBusRoutetownstoppage
Drop Table bus_historicalBusRoutetown

DELETE FROM pricing_pricematrix
WHERE bus_route_id = '4fc94192-14c8-11ee-9aae-7e44607f8f04';


Create Table bus_BusRoutetown (
    created_on time NOT NULL,
    updated_on time NOT NULL,
    is_deleted bool NOT NULL,
    id char(255) NOT NULL PRIMARY KEY,
    bus_route_id UUID REFERENCES bus_BusRoute (id) ON DELETE CASCADE,
    route_town_id UUID REFERENCES bus_routetown (id) ON DELETE CASCADE,
    duration INTEGER,
    calculated_duration INTEGER,
    day INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    eta_status VARCHAR(20) DEFAULT 'active',
    created TIMESTAMP,
    modified TIMESTAMP,
)

SELECT sqlite3_cwd()

ATTACH DATABASE '../dummy_4.sqlite3' AS source;

CREATE TABLE bus_BusRoutetown AS SELECT * FROM source.bus_BusRoutetown WHERE 0;

.open dummy.sqlite3
ATTACH 'dummy_3.sqlite3' AS target;

BEGIN;
INSERT INTO target.bus_busroute
SELECT * FROM bus_busroute;

COMMIT;

.close

-- Connect to the source database
ATTACH '/Users/diggy/Desktop/Ind/operator_bd/dummy_2.sqlite3' AS source_db;

-- Connect to the target database
ATTACH '/Users/diggy/Desktop/Ind/operator_bd/dummy_3.sqlite3' AS target_db;

-- Clone the table
CREATE TABLE IF NOT EXISTS target_db.bus_busroutetownstoppage AS
SELECT * FROM source_db.bus_busroutetownstoppage;

-- Detach the databases
DETACH source_db;
DETACH target_db;

ALTER TABLE bus_busroute RENAME COLUMN departure_time TO start_time;

ALTER TABLE bus_busroute ADD COLUMN route_ids TEXT;
ALTER TABLE bus_busroute ADD COLUMN bus_id INTEGER;
ALTER TABLE bus_busroute ADD COLUMN via TEXT;
ALTER TABLE bus_historicalbusroute ADD COLUMN via TEXT;
ALTER TABLE bus_busroutetownstoppage ADD COLUMN calculated_duration INTEGER;
PRAGMA table_info(bus_busroute);



