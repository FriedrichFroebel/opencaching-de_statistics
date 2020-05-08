# LaTeX Makefile

# Temporary files.
TMPFILES	= *.log *.aux *.toc *.out *.lof *.lot *.snm *.nav *.vrb *.bak *.gz

# Detect Windows systems to avoid problems with ImageMagick.
# On Windows systems `make` might detect the `convert` command from `system32`
# which is used for converting filesystems.
# On Linux systems the `magick` command is not available as it has been introduced with
# ImageMagick 7, while some distributions still ship version 6 (like in Ubuntu 18.04).
# PDF support might be restricted on Linux, see https://stackoverflow.com/questions/52861946/
# on how to fix this for example.
ifeq ($(OS),Windows_NT)
	imagemagick=magick convert
else
	imagemagick=convert
endif

# Handle default call.
.PHONY: default
default:    all

# Handle all calls.
.PHONY: all
all:    cache_types_pie_chart

# Handle the corresponding file.
cache_types_pie_chart: 	cache_types_pie_chart.pdf \
			cache_types_pie_chart.png

# Execute `pdflatex` three times to produce a PDF from the TeX source file.
%.pdf: %.tex
	pdflatex $<
	pdflatex -interaction=batchmode $<
	pdflatex -interaction=batchmode $<

# Execute ImageMagick to produce a PNG from a PDF file.
%.png: %.pdf
	$(imagemagick) -density 300 $< $@

# Catch missing input files instead of throwing an error.
%.pdf:
	@echo "Skipped" $@
%.png:
	@echo "Skipped" $@

# Clean temporary files including PDF files.
clean:
	rm -f $(TMPFILES)
	rm -f *.pdf
	rm -f *.png

# Clean temporary files excluding PDF files.
cleant:
	rm -f $(TMPFILES)
