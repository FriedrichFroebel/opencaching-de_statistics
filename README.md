# Statistics for Opencaching.de

This is a collection of tools to create statistics for the German opencaching site.

**Disclaimer:** These tools make use of the fulldump feature of the OKAPI. If you want retrieve new data regularly to create updated statistics, you should use the replicate feature after the first download by running it about every week. This feature is not implemented in the current version of these tools as I do only occassionally use them with longer periods in between. See the [OKAPI documentation](https://www.opencaching.de/okapi/services/replicate/fulldump.html) for more information. Please respect the copyright of the downloaded data as well.

## Available Statistics Tools

Usage instructions are available inside the single directories.

### Cache Type Distribution (Pie Chart)

The directory `cache_types_pie_chart` contains the scripts required to produce a pie chart with the distribution of the different cache types across all the not archived caches.

### Most Found Caches

The directory `most_found_caches` contains the scripts required to get the most found caches, allowing additional filters for the status and the German region (*Bundesland*).

## Development Tasks

### Code Style

After installing [black](https://github.com/psf/black), you should be able to run `black .` from the root directory of this repository to apply auto-formatting.

To check formatting itself, use `flake8 --max-line-length 88 *.py` after installing [flake8](https://gitlab.com/pycqa/flake8).

## License

The tools inside this repository are licensed under the MIT License (see the `LICENSE.md` file for details).

Some of the files are based upon external sources and therefore may have a different license:

* `cache_types_pie_chart/opencaching_de_search_query.py` is based on https://github.com/flopp/safari/blob/master/py/query.py, which has been published by Florian Pigorsch. The original license is the MIT license, the modified file follows the same license.
* `output/pie-chart.sty` is based on https://tex.stackexchange.com/a/180371/, which has been published by the user Tarass. The original license is CC BY-SA 4.0, the modified file follows the same license.
