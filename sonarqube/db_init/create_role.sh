#!/usr/bin/env bash
set -e

psql -U postgres <<-EOSQL
    CREATE ROLE sonarqube WITH PASSWORD 'qwerty' LOGIN CREATEDB;
EOSQL

psql -U sonarqube -d postgres <<-EOSQL
    CREATE DATABASE sonarqube;
EOSQL

psql -U sonarqube <<-EOSQL
    CREATE SCHEMA AUTHORIZATION sonarqube;
EOSQL

