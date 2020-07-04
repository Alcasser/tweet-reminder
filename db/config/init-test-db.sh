#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $TEST_DB;
    GRANT ALL PRIVILEGES ON DATABASE $TEST_DB TO $POSTGRES_USER;
EOSQL