#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Load the data from a fulldump into a database file.
"""

from collections import defaultdict
import json
from pathlib import Path
import sqlite3

import configuration


"""
The query to create the tables inside the database file.
"""
DATABASE_CREATION_QUERY = """CREATE TABLE `found_counts` (
    `code`          TEXT NOT NULL UNIQUE,
    `founds`        NUMERIC DEFAULT 0,
    `lat`           TEXT,
    `lon`           TEXT,
    `status`        TEXT,
    `cache_type`    TEXT,
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
query = "INSERT INTO `found_counts` (`code`,`lat`,`lon`,`status`,`cache_type`) VALUES (?,?,?,?,?);"

# Load the list of data files from the fulldump.
dump_path = Path(configuration.FULLDUMP_DIRECTORY)
with open(dump_path / "index.json", encoding="utf8") as infile:
    json_data = json.load(infile)
    files = json_data["data_files"]

# Dictionary with each entry being `0`.
founds_dict = defaultdict(int)

# Handle each data file from the fulldump.
for filename in files:
    print(f"Loading file {filename} into database ...")
    filename = dump_path / filename

    # Load the JSON data.
    with open(filename, encoding="utf8") as infile:
        json_data = json.load(infile)

    # Add to database.
    for line in json_data:
        object_type = line["object_type"]

        if object_type == "geocache":
            code = line["data"]["code"]
            lat, lon = line["data"]["location"].split("|")
            status = line["data"]["status"]
            type_ = line["data"]["type"]
            cursor.execute(query, (code, lat, lon, status, type_))
        elif object_type == "log":
            type_ = line["data"]["type"]
            if type_ != "Found it":
                continue
            code = line["data"]["cache_code"]
            founds_dict[code] += 1

# Add the found counts.
for code, founds in founds_dict.items():
    cursor.execute(
        "UPDATE `found_counts` SET founds = ? WHERE code = ?;", (founds, code)
    )

# Save the data.
connection.commit()

# Try to reduce the database size.
cursor.execute("VACUUM;")
connection.commit()

# Close the database connection.
connection.close()
