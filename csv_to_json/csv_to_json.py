#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert CSV to JSON."""

try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO
import csv
import string


def _remove_commented_rows(rows, comment_character):
    uncommented_rows = list()
    for row in rows:
        if not row[0].startswith(comment_character):
            uncommented_rows.append(row)
    return uncommented_rows


def convert(csv_string, delimiter=',', comment_character='#', heading_row=None):
    """Convert CSV data to json."""
    formatted_json = list()

    f = StringIO(csv_string)
    csv_reader = csv.reader(f, delimiter=delimiter)
    rows = [row for row in csv_reader]
    uncommented_rows = _remove_commented_rows(rows, comment_character)

    # get the keys for the json
    if heading_row is not None:
        heading_row = int(heading_row) - 1
        keys = uncommented_rows[heading_row]
        del uncommented_rows[heading_row]
    else:
        keys = list()
        available_keys = string.ascii_lowercase
        length = len(uncommented_rows[0])
        if length > 26:
            raise RuntimeError("There are more than 26 columns in the CSV ({} columns found) and the conversion system is designed to handle no more than 26.".format(length))
        else:
            for i in range(0, length):
                keys.append(available_keys[i])

    for row in uncommented_rows:
        row_data = dict()
        if not row[0].startswith(comment_character):
            for index, value in enumerate(row):
                row_data[keys[index]] = value
        formatted_json.append(row_data)

    return formatted_json
