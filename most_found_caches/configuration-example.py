#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration parameters.
"""

# The name of the database file (SQLite3).
# The content of this file will be cleared when loading the dump.
DATABASE_FILE = "cachedata_20200101-1200.db"

# The directory containing the unpacked fulldump.
FULLDUMP_DIRECTORY = "fulldump_20200101-1200"

# The path to the `plz-gebiete.shp` file.
PLZ_GEBIETE_SHP_PATH = "plz-gebiete.shp/plz-gebiete.shp"

# The path to the `zuordnung_plz_ort.csv.csv` file.
ZUORDNUNG_PLZ_ORT_PATH = "zuordnung_plz_ort.csv"

# Whether to include only active caches.
ACTIVE_ONLY = True

# Restrict the results to some region.
# If empty, the results will be global.
# Example: `REGION = "Nordrhein-Westfalen"`
RESTRICT_REGION = None

# Number of results to return.
RESULT_COUNT = 100

# The name of the output file.
OUTPUT_FILE = f"top_{RESULT_COUNT}.csv"
