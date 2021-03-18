#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get the most found caches, allowing additional filters for the status and the German
region (*Bundesland*).
"""

from pathlib import Path
import sqlite3

import configuration


if configuration.RESTRICT_REGION:
    # The restrictions are implemented by checking the PLZ of the current coordinate.

    import csv

    import shapefile
    from shapely.geometry import Point, shape as Shape

    # Load the data files.
    shp = shapefile.Reader(configuration.PLZ_GEBIETE_SHP_PATH)

    with open(
        configuration.ZUORDNUNG_PLZ_ORT_PATH, mode="r", encoding="utf8"
    ) as infile:
        reader = csv.reader(infile)
        mapping_plz_bundesland = {row[2]: row[3] for row in reader}

    # Filter for the selected region.
    plzs = {
        plz
        for plz, bundesland in mapping_plz_bundesland.items()
        if bundesland == configuration.RESTRICT_REGION
    }

    # Only keep the geometries for the selected region.
    # Afterwards cache the shape data to avoid repeated conversions.
    geometries = shp.shapeRecords()
    geometries_filtered = [
        geometry for geometry in geometries if geometry.record[0] in plzs
    ]
    for geometry in geometries_filtered:
        setattr(geometry, "boundary", Shape(geometry.shape))

    def is_in_region(lat, lon):
        point = Point(lon, lat)
        for geometry in geometries_filtered:
            if point.within(geometry.boundary):
                return True
        return False


else:
    # No restrictions requested, so provide a dummy implementation.

    def is_in_region(lat, lon):
        return True


# Create the output directory.
output_path = Path("../output")
if not output_path.exists():
    output_path.mkdir(parents=True)

# Connect to the database in read-only mode.
connection = sqlite3.connect(f"file:{configuration.DATABASE_FILE}?mode=ro", uri=True)
cursor = connection.cursor()

# Build the query.
query = f"""
    SELECT code, founds, lat, lon, cache_type FROM `found_counts`
    {"WHERE status = 'Available'" if configuration.ACTIVE_ONLY else ""}
    ORDER BY founds DESC;
"""

result_count = 0

with open(
    output_path / configuration.OUTPUT_FILE, mode="w", encoding="utf8"
) as outfile:
    # Write the header row.
    outfile.write("code,type,founds\n")

    # Execute the query.
    for row in cursor.execute(query):
        code, founds, lat, lon, type_ = row
        lat, lon = float(lat), float(lon)
        if is_in_region(lat, lon):
            outfile.write(f"{code},{type_},{founds}\n")
            result_count += 1
        if result_count == configuration.RESULT_COUNT:
            break

connection.close()
