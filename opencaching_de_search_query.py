#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################################
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

import requests
import re


def download_query(user, password, queryid):
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
