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

ATTACH DATABASE '/Users/diggy/Desktop/Ind/operator_bd/dummy_10.sqlite3' AS source;

CREATE TABLE route_routemissingtown AS SELECT * FROM source.route_routemissingtown WHERE 0;

.open dummy.sqlite3
ATTACH 'dummy_3.sqlite3' AS target;

BEGIN;
INSERT INTO target.route_routemissingtown
SELECT * FROM route_routemissingtown;

COMMIT;

.close

-- Connect to the source database
ATTACH '/Users/diggy/Desktop/Ind/operator_bd/dummy_10.sqlite3' AS source_db;

-- Connect to the target database
ATTACH '/Users/diggy/Desktop/Ind/operator_bd/dummy_3.sqlite3' AS target_db;

-- Clone the table
CREATE TABLE IF NOT EXISTS target_db.route_routemissingtown AS
SELECT * FROM source_db.route_routemissingtown;

-- Detach the databases
DETACH source_db;
DETACH target_db;

ALTER TABLE bus_busroute RENAME COLUMN departure_time TO start_time;

ALTER TABLE bus_busroute ADD COLUMN route_ids TEXT;
ALTER TABLE bus_busroute ADD COLUMN bus_id INTEGER;
ALTER TABLE bus_historicalbusroutetown ADD COLUMN bus_route_id CHAR(32);
ALTER TABLE bus_historicalbusroutetown ADD COLUMN town_status VARCHAR(20) DEFAULT 'active';
ALTER TABLE bus_historicalbusroutetown ADD COLUMN town_stoppage_status VARCHAR(20) DEFAULT 'active';
ALTER TABLE bus_historicalbusroutetown DROP COLUMN status;
ALTER TABLE bus_busroute ADD COLUMN via TEXT;
ALTER TABLE bus_historicalbusroute ADD COLUMN via TEXT;
ALTER TABLE bus_busroutetownstoppage ADD COLUMN calculated_duration INTEGER;
ALTER TABLE bus_busroutetown ADD COLUMN missing_towns TEXT;
ALTER TABLE bus_historicalbusroutetown ADD COLUMN missing_towns TEXT;
PRAGMA table_info(route_routemissingtown);

DELETE FROM account_user;
DELETE FROM account_salesteamuser;
DELETE FROM authtoken_token;
DELETE FROM account_operator;
DELETE FROM bus_bus;
DELETE FROM bus_busroutereturn;
ALTER TABLE account_historicalsalesteamuser ADD COLUMN password TEXT; 
ALTER TABLE account_historicalsalesteamuser ADD COLUMN last_login datetime;
ALTER TABLE account_historicalsalesteamuser ADD COLUMN is_superuser bool;
ALTER TABLE account_historicalsalesteamuser ADD COLUMN username varchar(150);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN first_name varchar(150);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN last_name varchar(150);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN email varchar(254);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN is_staff bool;
ALTER TABLE account_historicalsalesteamuser ADD COLUMN date_joined datetime;
ALTER TABLE account_historicalsalesteamuser ADD COLUMN user_type varchar(25);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN preferred_language varchar(255);
ALTER TABLE account_historicalsalesteamuser ADD COLUMN is_active bool;
find . -type d -name '__pycache__' -exec rm -rf {} +

INSERT INTO account_salesteamuser (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, date_joined, user_type, preferred_language, is_active)
SELECT password, last_login, is_superuser, username, first_name, last_name, email, is_staff, date_joined, user_type, preferred_language, is_active
FROM account_user;

DELETE FROM account_salesteamuser LIMIT 10;

Create Table route_routemissingtown(
    created_on DATETIME NOT NULL DEFAULT NULL,
    updated_on DATETIME NOT NULL DEFAULT NULL,
    is_deleted BOOL NOT NULL DEFAULT NULL,
    id CHAR(32) NOT NULL PRIMARY KEY DEFAULT NULL,
    route_id CHAR(32) DEFAULT NULL,
    missing_town CHAR(255) DEFAULT NULL
)

CREATE TABLE route_historicalroutemissingtown (
    created_on DATETIME NOT NULL DEFAULT NULL,
    updated_on DATETIME NOT NULL DEFAULT NULL,
    is_deleted BOOL NOT NULL DEFAULT NULL,
    id CHAR(32) NOT NULL DEFAULT NULL,
    history_id INTEGER DEFAULT NULL,
    history_date DATETIME NOT NULL DEFAULT NULL,
    history_change_reason VARCHAR(100) DEFAULT NULL,
    history_type VARCHAR(1) NOT NULL DEFAULT NULL,
    history_user_id CHAR(32) DEFAULT NULL,
    route_id CHAR(32) DEFAULT NULL,
    missing_town CHAR(255) DEFAULT NULL
);

CREATE TABLE temp_table (
    created_on DATETIME NOT NULL DEFAULT NULL,
    updated_on DATETIME NOT NULL DEFAULT NULL,
    is_deleted BOOL NOT NULL DEFAULT NULL,
    id CHAR(32) NOT NULL DEFAULT NULL,
    history_id INTEGER DEFAULT NULL,
    history_date DATETIME NOT NULL DEFAULT NULL,
    history_change_reason VARCHAR(100) DEFAULT NULL,
    history_type VARCHAR(1) NOT NULL DEFAULT NULL,
    history_user_id CHAR(32) DEFAULT NULL,
    route_id CHAR(32) DEFAULT NULL,
    missing_town CHAR(255) DEFAULT NULL
);

INSERT INTO temp_table SELECT * FROM route_historicalroutemissingtown;

DROP TABLE route_historicalroutemissingtown;
DROP TABLE route_routemissingtown;

-- Step 4: Rename the temporary table to the original table name
ALTER TABLE temp_table RENAME TO route_historicalroutemissingtown;

find . -type d -name '__pycache__' -exec rm -rf {} +

find . -type d -name 'migrations' -exec rm -rf {} +


ALTER TABLE route_historicalroutemissingtown ALTER COLUMN history_id DROP NOT NULL;

ALTER TABLE route_routemissingtown ADD COLUMN town_id varchar(25);

ALTER TABLE route_routemissingtown ADD CONSTRAINT fk_routemissingtown_town FOREIGN KEY (town_id) REFERENCES Town(id)ON DELETE CASCADE;

ALTER TABLE route_routemissingtown ADD COLUMN town_id varchar(25) REFERENCES route_town(id) ON DELETE CASCADE;
ALTER TABLE route_historicalroutemissingtown ADD COLUMN town_id varchar(25) REFERENCES route_town(id) ON DELETE CASCADE;
ALTER TABLE route_routemissingtown DROP COLUMN town_id;
ALTER TABLE route_historicalroutemissingtown DROP COLUMN town_id;


DELETE FROM bus_townsearch LIMIT 500;
DELETE FROM account_historicaloperator where history_user_id='dc6a158e18b211ee99e17e44607f8f04';

alter table route_routemissingtown drop constraint route_id;
ALTER TABLE route_routemissingtown DROP COLUMN route_id;

SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = route_routemissingtown;

.schema route_routemissingtown;
select * from sqlite_master where type='table' and name='bus_historicalbusroutetown';

CREATE TABLE "route_historicalroutemissingtown" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" char(32) NULL REFERENCES "account_user" ("id") DEFERRABLE INITIALLY DEFERRED, "route_id" char(32) NULL REFERENCES "route_route" ("id") DEFERRABLE INITIALLY DEFERRED, "duration" integer NULL, "missing_town" varchar(255) NULL);
CREATE TABLE "route_routemissingtown" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL PRIMARY KEY, "route_id" char(32) NULL REFERENCES "route_route" ("id") DEFERRABLE INITIALLY DEFERRED, "duration" integer NULL, "missing_town" varchar(255) NULL);

CREATE TABLE "bus_townsearch" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL PRIMARY KEY, "towns" Text);
CREATE TABLE "bus_historicaltownsearch" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" char(32) NULL REFERENCES "account_user" ("id") DEFERRABLE INITIALLY DEFERRED, "towns" Text);

DROP TABLE bus_townsearch;
DROP TABLE bus_historicaltownsearch;
-- CREATE TABLE "bus_townsearch" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL PRIMARY KEY, "town_id" char(32) NULL REFERENCES "route_route" ("id") DEFERRABLE INITIALLY DEFERRED, "towns" Text);

CREATE TABLE "bus_townsearch" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL PRIMARY KEY, "town_id" char(32) NULL REFERENCES "route_town" ("id") DEFERRABLE INITIALLY DEFERRED, "district_id" char(32) NULL REFERENCES "route_district" ("id") DEFERRABLE INITIALLY DEFERRED , town_name varchar(255), district_name varchar(255))
CREATE TABLE "bus_historicaltownsearch" ("created_on" datetime NOT NULL, "updated_on" datetime NOT NULL, "is_deleted" bool NOT NULL, "id" char(32) NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" char(32) NULL REFERENCES "account_user" ("id") DEFERRABLE INITIALLY DEFERRED, "town_id" char(32) NULL REFERENCES "route_town" ("id") DEFERRABLE INITIALLY DEFERRED, "district_id" char(32) NULL REFERENCES "route_district" ("id") DEFERRABLE INITIALLY DEFERRED , town_name varchar(255), district_name varchar(255))
ALTER TABLE bus_townsearch ADD COLUMN town_name varchar(255);
ALTER TABLE bus_townsearch ADD COLUMN district_name varchar(255);
ALTER TABLE bus_historicaltownsearch ADD COLUMN town_name varchar(255);
ALTER TABLE bus_historicaltownsearch ADD COLUMN district_name varchar(255);