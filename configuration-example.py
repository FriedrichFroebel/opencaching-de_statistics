#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration parameters.
"""

# The name of the database file (SQLite3).
# The content of this file will be cleared when loading the dump.
DATABASE_FILE = "cachedata_20200101-1200.db"

# The datetime the database/fulldump has been created at.
# Format: %Y-%m-%d %H:%M
DATABASE_CREATED_DATETIME = "2020-01-01 12:00"

# The directory containing the unpacked fulldump.
FULLDUMP_DIRECTORY = "fulldump_20200101-1200"

# The username for Opencaching.de to use for retrieving additional data.
OPENCACHING_DE_USERNAME = "user"

# The password for Opencaching.de to use for retrieving additional data.
OPENCACHING_DE_PASSWORD = "password"

# The query ID to search for Drive-In caches.
# Go to
#     https://www.opencaching.de/search.php?searchto=searchall&showresult=1&expert=0&output=HTML&utf8=1&sort=bydistance&orderRatingFirst=0&f_userowner=0&f_userfound=0&f_inactive=0&f_disabled=0&f_ignored=0&f_otherPlatforms=0&f_geokrets=0&country=&language=&difficultymin=0&difficultymax=0&terrainmin=0&terrainmax=0&cachetype=10&cachesize=1%3B2%3B3%3B4%3B5%3B6%3B7%3B8&cache_attribs=&cache_attribs_not=&submit_all=Suchen
# and use "Save options" ("Optionen speichern"). Set a list name and retrieve the
# query ID from
#     https://www.opencaching.de/query.php
# (end of the URL when clicking the list name).
OPENCACHING_DE_QUERY_ID_DRIVE_IN = 0

# The query ID to search for Math/Physics caches.
# Go to
#     https://www.opencaching.de/search.php?searchto=searchall&showresult=1&expert=0&output=HTML&utf8=1&sort=bydistance&orderRatingFirst=0&f_userowner=0&f_userfound=0&f_inactive=0&f_disabled=0&f_ignored=0&f_otherPlatforms=0&f_geokrets=0&country=&language=&difficultymin=0&difficultymax=0&terrainmin=0&terrainmax=0&cachetype=10&cachesize=1%3B2%3B3%3B4%3B5%3B6%3B7%3B8&cache_attribs=&cache_attribs_not=&submit_all=Suchen
# and use "Save options" ("Optionen speichern"). Set a list name and retrieve the
# query ID from
#     https://www.opencaching.de/query.php
# (end of the URL when clicking the list name).
OPENCACHING_DE_QUERY_ID_MATH_PHYSICS = 0
