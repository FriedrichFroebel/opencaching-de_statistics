#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Load the data from a fulldump into a database file.
"""

import json
from pathlib import Path
import sqlite3

import configuration
import opencaching_de_search_query


"""
The query to create the tables inside the database file.
"""
DATABASE_CREATION_QUERY = """CREATE TABLE `opencaches` (
    `code`          TEXT NOT NULL UNIQUE,
    `name`          TEXT NOT NULL,
    `status`        TEXT NOT NULL,
    `cache_type`    TEXT NOT NULL,
    PRIMARY KEY(`code`)
)"""

# Delete the existing database file.
database_path = Path(configuration.DATABASE_FILE)
if database_path.exists():
    database_path.unlink()

# Connect to the database.
connection = sqlite3.connect(configuration.DATABASE_FILE)
cursor = connection.cursor()

# Create the database tables.
cursor.execute(DATABASE_CREATION_QUERY)
connection.commit()

# Prepare the query to insert the cache data.
query = (
    "INSERT INTO `opencaches` (`code`,`name`,`status`,`cache_type`) VALUES (?,?,?,?);"
)

# Load the list of data files from the fulldump.
dump_path = Path(configuration.FULLDUMP_DIRECTORY)
with open(str(dump_path / "index.json"), encoding="utf8") as infile:
    json_data = json.load(infile)
    files = json_data["data_files"]

# Handle each data file from the fulldump.
for filename in files:
    print(f"Loading file {filename} into database ...")
    filename = str(dump_path / filename)

    # Load the JSON data.
    with open(filename, encoding="utf8") as infile:
        json_data = json.load(infile)

    # Add to database.
    for line in json_data:
        # Only save geocaches.
        if line["object_type"] != "geocache":
            continue
        # As we are creating a fresh database, we can skip deletion requests.
        if line["change_type"] == "delete":
            continue

        # Retrieve the data from the JSON dictionary.
        data = line["data"]
        code = data["code"]
        name = data["names"]["de"]
        status = data["status"]
        type_ = data["type"]

        # Run the query with the current parameter set.
        cursor.execute(query, (code, name, status, type_))

# Save the data.
connection.commit()

# Fix some of the local types (Math/Physics and Drive-In) not being returned by the
# OKAPI. This requires the corresponding query IDs being set up at opencaching.de.
query = "UPDATE `opencaches` SET `cache_type` = ? WHERE `code` = ?;"
math_physics = opencaching_de_search_query.download_query(
    configuration.OPENCACHING_DE_USERNAME,
    configuration.OPENCACHING_DE_PASSWORD,
    configuration.OPENCACHING_DE_QUERY_ID_MATH_PHYSICS,
)
drive_in = opencaching_de_search_query.download_query(
    configuration.OPENCACHING_DE_USERNAME,
    configuration.OPENCACHING_DE_PASSWORD,
    configuration.OPENCACHING_DE_QUERY_ID_DRIVE_IN,
)
for code in math_physics:
    cursor.execute(query, ("Math/Physics", code))
for code in drive_in:
    cursor.execute(query, ("Drive-In", code))
connection.commit()

# Try to reduce the database size.
cursor.execute("VACUUM;")
connection.commit()

# Close the database connection.
connection.close()
