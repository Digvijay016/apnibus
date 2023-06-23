-- SQLite
SELECT created_on, updated_on, is_deleted, id, bus_number, pos_serial_no, pos_dsn_number, gps_sim_image
FROM bus_bus;

SELECT sql
FROM sqlite_master
WHERE type = 'table' AND name = 'route_historicalcity';

sql
CREATE TABLE "bus_historicalbusroute" 
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

Create Table bus_busroute (
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

SELECT * FROM bus_busroute

Drop Table bus_historicalbusroute
Drop Table bus_busroute