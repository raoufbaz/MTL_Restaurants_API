#!/bin/bash
# script pour creer une bd et importer la table
sqlite3 database.db ".read creation_table_violations.sql"
