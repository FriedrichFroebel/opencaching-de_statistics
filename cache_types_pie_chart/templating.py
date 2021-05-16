#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Templating functionality.
"""

from pathlib import Path

import jinja2

"""
Jinja2 environment configuration for LaTeX templates.
"""
JINJA_ENVIRONMENT_LATEX = jinja2.Environment(
    block_start_string="\\BLOCK{",
    block_end_string="}",
    variable_start_string="\\VAR{",
    variable_end_string="}",
    comment_start_string="\\#{",
    comment_end_string="\\#{",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(str(Path.cwd() / ".." / "templates")),
)


def apply_latex_template(template_file, variables, output_file=None):
    """
    Apply the data for the given LaTeX template file and write the output to the given
    file if needed.

    :param template_file: The name of the template file to use.
    :type template_file: str

    :param variables: The variables to put into the template.
    :type variables: dict[str, object]

    :param output_file: The file to write the rendered data to. If this is is
                        :code:`None`, no output will be written.
    :type output_file: str or None

    :return: The rendered result (LaTeX source code).
    :rtype: str
    """
    # Retrieve the template.
    template = JINJA_ENVIRONMENT_LATEX.get_template(template_file)

    # Render the template.
    result = template.render(variables)

    # Write the output to the given file (if requested) and return the result.
    if output_file:
        with open(output_file, encoding="utf8", mode="w") as outfile:
            outfile.write(result)
    return result
