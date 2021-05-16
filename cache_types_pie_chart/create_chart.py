#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pie chart with the distribution of the different cache types across all the not
archived caches.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sqlite3

import configuration
import templating


# Based upon
# https://github.com/OpencachingDeutschland/oc-server3/blob/ff940ae404b19ef5b70ef8d21a55a8d74e731eb3/sql/static-data/cache_type.sql
"""
The list of known cache types and their German names to use for the output.
"""
CACHE_TYPE_NAMES = {
    "Other": "Unbekannter Cachetyp",
    "Traditional": "Normaler Cache",
    "Multi": "Multicache",
    "Virtual": "Virtueller Cache",
    "Webcam": "Webcam Cache",
    "Event": "Event Cache",
    "Quiz": "Rätselcache",
    "Math/Physics": "Mathe-/Physikcache",
    "Moving": "Beweglicher Cache",
    "Drive-In": "Drive-In-Cache",
}

# Connect to the database in read-only mode.
connection = sqlite3.connect(f"file:{configuration.DATABASE_FILE}?mode=ro", uri=True)

# Retrieve the statistics from the database.
query = (
    "SELECT cache_type, COUNT(*) AS `count` FROM opencaches "
    + 'WHERE status != "Archived" GROUP BY cache_type;'
)
type_counts = {}
for row in connection.execute(query):
    cache_type, count = row
    type_counts[cache_type] = count
connection.close()

# Determine the total number of caches retrieved.
total_count = sum(type_counts.values())


@dataclass(frozen=True)
class CacheType:
    """
    Container for the cache type data.
    """

    database_name: str
    """
    The name of the cache type inside the database.
    """

    german_name: str
    """
    The German name of the cache type.
    """

    count_absolute: int
    """
    The absolute number of caches with this type.
    """

    count_relative: float
    """
    The relative amount of caches with this type in percent.
    """


# Determine the relative values and create the output list with the cache types being
# in ascending order sorted by their popularity.
counts = []
for key in sorted(type_counts, key=type_counts.get, reverse=True):
    value = type_counts.get(key)
    value_relative_percent = value / total_count * 100
    instance = CacheType(
        database_name=key,
        german_name=CACHE_TYPE_NAMES[key],
        count_absolute=value,
        count_relative=value_relative_percent,
    )
    counts.append(instance)

# Create the output directory.
output_path = Path("../output")
if not output_path.exists():
    output_path.mkdir(parents=True)

# Create the formatted creation datetime.
created_parsed = datetime.strptime(
    configuration.DATABASE_CREATED_DATETIME, "%Y-%m-%d %H:%M"
)
created_reformatted = created_parsed.strftime("%d.%m.%Y %H:%M")

# Set the parameters for the template.
parameters = {
    "total_count": total_count,
    "counts": counts,
    "created": created_reformatted,
}

# Render the content inside the Jinja2 template.
output_file = str(output_path / "cache_types_pie_chart.tex")
templating.apply_latex_template(
    "cache_types_pie_chart_template.tex", parameters, output_file
)
