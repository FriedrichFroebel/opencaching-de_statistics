# Statistics for Opencaching.de

This is a collection of tools to create statistics for the German opencaching site.

**Disclaimer:** These tools make use of the fulldump feature of the OKAPI. If you want retrieve new data regularly to create updated statistics, you should use the replicate feature after the first download by running it about every week. This feature is not implemented in the current version of these tools as I do only occassionally use them with longer periods in between. See the [OKAPI documentation](https://www.opencaching.de/okapi/services/replicate/fulldump.html) for more information. Please respect the copyright of the downloaded data as well.

## Usage

### Requirements

Make sure you have

* Python 3 (at least version 3.6)
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
6. Run `python3 -m cache_types_pie_chart` to create a pie chart for the distribution of the currently active caches per cache type.
7. Switch to the output directory and run `make all cleant` to create the PDF and PNG files and delete the auxiliary files afterwards.

## Development Tasks

### Code Style

After installing [black](https://github.com/psf/black), you should be able to run `black .` from the root directory of this repository to apply auto-formatting.

To check formatting itself, use `flake8 --max-line-length 88 *.py` after installing [flake8](https://gitlab.com/pycqa/flake8).

## License

The tools inside this repository are licensed under the MIT License (see the `LICENSE.md` file for details).

Some of the files are based upon external sources and therefore may have a different license:

* `opencaching_de_search_query.py` is based on https://github.com/flopp/safari/blob/master/py/query.py, which has been published by Florian Pigorsch. The original license is the MIT license, the modified file follows the same license.
* `output/pie-chart.sty` is based on https://tex.stackexchange.com/a/180371/, which has been published by the user Tarass. The original license is CC BY-SA 4.0, the modified file follows the same license.
