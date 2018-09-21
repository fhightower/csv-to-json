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



def _debug(debug, message):
    """Print the given message if debugging is true."""
    if debug:
        print(message)
        # add a newline after every message
        print('')


def _remove_commented_rows(rows, comment_character):
    """Remove any rows that start with the comment character."""
    uncommented_rows = list()
    for row in rows:
        # if the row is empty, move on
        if len(row) == 0:
            continue
        # if the row does not start with the comment character, record it
        if not row[0].startswith(comment_character):
            uncommented_rows.append(row)
    return uncommented_rows


def convert(csv_string, delimiter=',', comment_character='#', heading_row=None, debug=False):
    """Convert CSV data to json."""
    formatted_json = list()

    f = StringIO(csv_string)
    csv_reader = csv.reader(f, delimiter=delimiter)
    rows = [row for row in csv_reader]
    _debug(debug, 'Found {} rows before removing commented rows'.format(len(rows)))
    uncommented_rows = _remove_commented_rows(rows, comment_character)
    _debug(debug, 'Found {} rows after removing commented rows:\n{}'.format(len(uncommented_rows), uncommented_rows))

    # get the keys for the json from the CSV
    if heading_row is not None:
        # if the heading row is zero, assume that the user wants to use the first row
        if heading_row == 0:
            print('I\'m going to assume that you want to use the first row as the heading_row. In the future, use the natural, counting number to specify the correct heading row (e.g. 1 specifies the first row, 2 specifies the second row, etc...)')
        # otherwise, assume that the user is using natural counting numbers to specify the heading row
        else:
            _debug(debug, 'The user gave {} as the heading_row. I\'m going to take the headings from the row at index {}.'.format(heading_row, int(heading_row) - 1))
            heading_row = int(heading_row) - 1
        _debug(debug, 'Using the heading from row {} to get the keys:\n{}'.format(heading_row, uncommented_rows[heading_row]))
        keys = uncommented_rows[heading_row]
        del uncommented_rows[heading_row]
    # get the keys for the json from ascii characters
    else:
        keys = list()
        available_keys = string.ascii_lowercase
        # find the max length of all entries in the CSV
        max_length = max([len(row) for row in uncommented_rows])
        _debug(debug, 'The CSV will be created with {} keys'.format(max_length))
        if max_length > 26:
            raise RuntimeError("There are more than 26 columns in the CSV ({} columns found) and the conversion system is designed to handle no more than 26.".format(max_length))
        else:
            for i in range(0, max_length):
                keys.append(available_keys[i])
            _debug(debug, 'The following keys will be used for this csv: {}'.format(keys))

    _debug(debug, '========== STARTING CSV PROCESSING ==========')
    for row in uncommented_rows:
        _debug(debug, '    Processing row:\n    {}'.format(row))
        row_data = dict()
        for index, value in enumerate(row):
            row_data[keys[index]] = value
        _debug(debug, '    Created row data:\n    {}'.format(row_data))
        formatted_json.append(row_data)
    _debug(debug, '========== DONE PROCESSING CSV ==========')

    return formatted_json
