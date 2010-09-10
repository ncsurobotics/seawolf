PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE config (option VARCHAR PRIMARY KEY, value VARCHAR);
INSERT INTO "config" VALUES('password','');
INSERT INTO "config" VALUES('log_file','seawolf.log');

CREATE TABLE variables (id INT AUTO_INCREMENT UNIQUE PRIMARY KEY, time TIMESTAMP, precisetime DOUBLE, name CHAR(20), value FLOAT);

CREATE TABLE variable_definitions (name CHAR(64) UNIQUE PRIMARY KEY, default_value DOUBLE, persistent BOOL, readonly BOOL);
COMMIT;
