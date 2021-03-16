#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pie chart with the distribution of the different cache types across all the not
archived caches.
"""

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


class CacheType:
    """
    Container for the cache type data.
    """

    database_name = None
    """
    The name of the cache type inside the database.

    :type: :class:`str`
    """

    german_name = None
    """
    The German name of the cache type.

    :type: :class:`str`
    """

    count_absolute = 0
    """
    The absolute number of caches with this type.

    :type: :class:`int`
    """

    count_relative = 0
    """
    The relative amount of caches with this type in percent.

    :type: :class:`float`
    """

    def __init__(self, database_name, german_name, count_absolute, count_relative):
        """
        :param database_name: The name inside the database to set.
        :type database_name: str

        :param german_name: The German name to set.
        :type german_name: str

        :param count_absolute: The absolute number to set.
        :type count_absolute: int

        :param count_relative: The relative amount in percent to set.
        :type count_relative: float
        """
        self.database_name = database_name
        self.german_name = german_name
        self.count_absolute = count_absolute
        self.count_relative = count_relative


# Determine the relative values and create the ouput list with the cache types being
# in ascending order sorted by their popularity.
counts = []
for key in sorted(type_counts, key=type_counts.get, reverse=True):
    value = type_counts.get(key)
    value_relative_percent = value / total_count * 100
    instance = CacheType(key, CACHE_TYPE_NAMES[key], value, value_relative_percent)
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
