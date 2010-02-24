#!/bin/sh

if ! sqlite3 -version > /dev/null 2>&1; then
    echo "Please install the sqlite3 command line utility before running this command"
    exit 1
fi

if [ -f seawolf.db ]; then
    echo "Database already exists, cowardly refusing to initalize"
    exit 1
fi

sqlite3 seawolf.db < seawolf_db_init.sql
