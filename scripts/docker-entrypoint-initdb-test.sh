#!/bin/bash

# Check if the user exists, create it if not
psql -U testuser -tc "SELECT 1 FROM pg_roles WHERE rolname='testuser'" | grep -q 1 || psql -U testuser -c "CREATE USER testuser WITH PASSWORD 'testpassword'"

# Check if the database exists, create it if not
psql -U testuser -tc "SELECT 1 FROM pg_database WHERE datname='test_db'" | grep -q 1 || psql -U testuser -c "CREATE DATABASE test_db"

# Grant privileges to testuser on the test_db
psql -U testuser -c "GRANT ALL PRIVILEGES ON DATABASE test_db TO testuser"
