# Cache Types Distribution (Pie Chart)

This directory contains the scripts required to produce a pie chart with the distribution of the different cache types across all the not archived caches.

## Usage

### Requirements

Make sure you have

* Python 3 (at least version 3.7)
* [Jinja2](https://palletsprojects.com/p/jinja/)
* [requests](https://github.com/requests/requests)
* [make](https://www.gnu.org/software/make/)
* LaTeX (PdfLaTeX)
* [ImageMagick](https://imagemagick.org/)

installed on your device.

### Running

1. Retrieve an OKAPI key and [download a database snapshot](https://www.opencaching.de/okapi/services/replicate/fulldump.html).
2. Unpack the downloaded file into a directory starting with `fulldump` (to ignore it on commit by default).
3. Open the Opencaching site, log in into your account (to allow doing a full search for all caches) and save two queries from the [search results](https://www.opencaching.de/search.php):
    1. A query with all caches having the "Drive-In" type.
    2. A query with all caches having the "Math/Physics" type.

   These types are mapped to alternative types inside the OKAPI and therefore have to be retrieved in a second step. Please make sure to not hide ignored or archived caches to avoid incorrect data. Keep record of the IDs assigned to both queries on the [saved queries page](https://www.opencaching.de/query.php).
4. Rename the `configuration-example.py` file to `configuration.py`. Edit the file and change the parameters to match your setup.
5. Run `python3 -m load_dump` to load the data from the fulldump into the database and retrieve additional details from the regular search page.
6. Run `python3 -m create_chart` to create a pie chart for the distribution of the currently active caches per cache type.
7. Switch to the output directory and run `make all cleant` to create the PDF and PNG files and delete the auxiliary files afterwards.
