# Most Found Caches

This directory contains the scripts required to get the most found caches, allowing additional filters for the status and the German region (*Bundesland*).

## Usage

### Requirements

Make sure you have

* Python 3 (at least version 3.6)
* [pyshp](https://github.com/GeospatialPython/pyshp)
* [Shapely](https://github.com/Toblerity/Shapely)

installed on your device.

### Running

1. Retrieve an OKAPI key and [download a database snapshot](https://www.opencaching.de/okapi/services/replicate/fulldump.html).
2. Unpack the downloaded file into a directory starting with `fulldump` (to ignore it on commit by default).
3. Download the files `plz-gebiete.shp.zip` and `zuordnung_plz_ort.csv` from https://www.suche-postleitzahl.org/downloads, based upon OpenStreetMap data. Unpack them.
4. Rename the `configuration-example.py` file to `configuration.py`. Edit the file and change the parameters to match your setup.
5. Run `python3 -m load_dump` to load the data from the fulldump into the database.
6. Run `python3 -m get_most_found` to retrieve the requested opencaches.
