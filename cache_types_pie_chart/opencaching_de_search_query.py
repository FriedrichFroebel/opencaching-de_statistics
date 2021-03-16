#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################################################
# This file is a modified version of the original version residing at
# https://github.com/flopp/safari/blob/80a77a7fc1dd63d8c33cec92e5e93384d48c7938/py/query.py
#
# Original license:
#########################################################################
# MIT License
#
# Copyright (c) 2016-2018 Florian Pigorsch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#########################################################################

import io
import re
from xml.etree import ElementTree
import zipfile

import requests


def download_query(user, password, queryid):
    """
    Download the given query.

    :param user: The name of the user to log in with.
    :type user: str

    :param password: The password to use for the login.
    :type password: str

    :param queryid: The ID of the search query to retrieve the cache codes for.
    :type queryid: int

    :return: The list of cache codes retrieved from the query.
    :rtype: list[str]
    """
    headers = {
        "User-agent": "opencaching-de_statistics "
        + "[https://github.com/FriedrichFroebel/opencaching-de_statistics]"
    }
    s = requests.Session()
    r = s.post(
        "https://www.opencaching.de/login.php",
        data={
            "action": "login",
            "target": "query.php",
            "email": user.encode("utf-8"),
            "password": password.encode("utf-8"),
        },
        headers=headers,
    )

    if "32x32-search.png" not in r.text:
        print("ERROR: failed to log in (bad response)")
        return []

    oc_codes = []
    batch_size = 20
    batch_start = 0
    while True:
        url = (
            f"https://www.opencaching.de/search.php?queryid={queryid}&output=loc"
            + f"&startat={batch_start}&count={batch_size}&zip=0"
        )
        r = s.get(url, headers=headers)
        if r.status_code != 200:
            print(f"-- Terminating due to bad status code: {r.status_code}")
            break
        new_oc_codes = []
        for m in re.finditer(r'<name id="([^"]+)">', r.text):
            new_oc_codes.append(m.groups()[0])
        if not new_oc_codes:
            break
        oc_codes = oc_codes + new_oc_codes
        batch_start += batch_size

    return oc_codes


def download_query_alternative(user, password, queryid, batch_size=500):
    """
    This is an alternative implementation of the query downloader.

    The original implementation only used a batch size of 20 as this allowed for using
    plain LOC files. Unfortunately this is a bit slow and causes more load on the web
    server due to a lot of small requests.

    With the modified implementation, the batch size can be chosen by the user. This
    is accomplished by using an in-memory extraction of the downloaded ZIP file.

    Additionally this code uses an XML parser instead of a regex to retrieve the data.

    :param user: The name of the user to log in with.
    :type user: str

    :param password: The password to use for the login.
    :type password: str

    :param queryid: The ID of the search query to retrieve the cache codes for.
    :type queryid: int

    :param batch_size: The batch size to use for the requests. This must at least be 1
                       and cannot exceed 500. The upper bound is due to the limits used
                       by the Opencaching.de site.
    :type batch_size: int

    :return: The list of cache codes retrieved from the query.
    :rtype: list[str]

    :raises ValueError: Some of the input values are invalid.
    """
    # Check the specified batch size.
    if not 0 < batch_size <= 500:
        raise ValueError("Invalid batch size.")

    # Use a custom header.
    headers = {
        "User-agent": "opencaching-de_statistics "
        + "[https://github.com/FriedrichFroebel/opencaching-de_statistics]"
    }

    # Try to log in.
    session = requests.Session()
    response = session.post(
        "https://www.opencaching.de/login.php",
        data={
            "action": "login",
            "target": "query.php",
            "email": user.encode("utf-8"),
            "password": password.encode("utf-8"),
        },
        headers=headers,
    )

    # Check if the login has been successful.
    if "32x32-search.png" not in response.text:
        raise ValueError("Login failed (bad response).")

    # Prepare our status variables.
    oc_codes = []
    batch_start = 0

    while True:
        # Build the current URL, then retrieve the data.
        # In contrast to the original version, we enforce ZIP files here.
        url = (
            f"https://www.opencaching.de/search.php?queryid={queryid}&output=loc"
            + f"&startat={batch_start}&count={batch_size}&zip=1"
        )
        response = session.get(url, headers=headers)

        # Check if the request has been successful.
        # If there has been an error, return the list of OC codes found until now.
        if response.status_code != 200:
            print(f"-- Terminating due to bad status code: {response.status_code}")
            break

        # Check if we got a ZIP file (in fact this should always be the case).
        # The first check uses the magic number for non-empty ZIP archives.
        if response.text.startswith("PK\x03\x04") and not response.text.startswith(
            "<?xml"
        ):
            # This is a zip file, so uncompress it.
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))

            # The ZIP files normally have one file only, so we just retrieve the first
            # one here.
            files = zip_file.namelist()
            if files:
                filename = files[0]
                xml_data = zip_file.read(filename)

        # If this is not a ZIP file or the ZIP file has no content, assume that it has
        # been a plain XML file.
        if not xml_data:
            xml_data = response.text

        # Parse the XML data.
        tree = ElementTree.fromstring(xml_data)

        # Get the name tags from the XML tree and retrieve the ID attribute for this
        # tag.
        # If the ID attribute is missing, the corresponding entry will be `None`.
        new_oc_codes = [name.get("id") for name in tree.iter("name")]

        # Remove all the `None` elements.
        new_oc_codes = list(filter(None, new_oc_codes))

        # We have reached the end of the results.
        if not new_oc_codes:
            break

        # Add the new codes to the existing list and move on to the next request.
        oc_codes = oc_codes + new_oc_codes
        batch_start += batch_size

    return oc_codes
