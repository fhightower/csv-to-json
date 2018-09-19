#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `csv_to_json` module."""

import os

import pytest

from csv_to_json import csv_to_json


def _get_csv_data(file_path='./data/test.csv'):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), file_path)), 'r') as f:
        file_text = f.read()
    return file_text


def test_csv_to_json():
    data = _get_csv_data()
    converted_data = csv_to_json.convert(data, delimiter='\t', heading_row=1)
    assert len(converted_data) == 20

    assert converted_data[0]['Start'] == '111.37.20.0'
    assert converted_data[0]['End'] == '111.37.20.255'
    assert converted_data[0]['Netmask'] == '24'
    assert converted_data[0]['Attacks'] == '4123'
    assert converted_data[0]['Name'] == 'CMNET-GD Guangdong Mobile Communication Co.Ltd.,'
    assert converted_data[0]['Country'] == 'CN'
    assert converted_data[0]['email'] == 'ipas@cnnic.cn'

    assert converted_data[-1]['Start'] == '111.37.25.0'
    assert converted_data[-1]['End'] == '111.37.25.255'
    assert converted_data[-1]['Netmask'] == '24'
    assert converted_data[-1]['Attacks'] == '2108'
    assert converted_data[-1]['Name'] == 'CMNET-GD Guangdong Mobile Communication Co.Ltd.,'
    assert converted_data[-1]['Country'] == 'CN'
    assert converted_data[-1]['email'] == 'ipas@cnnic.cn'


def test_csv_quotation_mark_escaping():
    data = _get_csv_data('./data/test_quotation_mark_escaping.csv')
    converted_data = csv_to_json.convert(data, heading_row=1)
    assert len(converted_data) == 2

    assert converted_data[0]['A'] == '1'
    assert converted_data[0]['B'] == 'test, ing'


def test_csv_without_column_names():
    data = _get_csv_data('./data/test_no_column_headings.csv')
    converted_data = csv_to_json.convert(data)
    assert len(converted_data) == 2

    assert converted_data[0]['a'] == '1'
    assert converted_data[0]['b'] == 'test, ing'


def test_hpfeeds_tsv():
    data = _get_csv_data('./data/hp_hosts.csv')
    converted_data = csv_to_json.convert(data, delimiter='\t')
    assert len(converted_data) == 1158
    # make sure the lines with real data are handled properly
    assert converted_data[2]['b'] == '115qxw.hbg.hebdenbridgedental.co.uk'
    # make sure the lines with some data missing are handled properly (with only one entry (`a`))
    assert converted_data[0] == {'a': '127.0.0.1 localhost #IPv4 localhost'}
    assert not converted_data[0].get('b')


def test_unicode_data():
    data = _get_csv_data('./data/test_encoded_data.csv')
    converted_data = csv_to_json.convert(data, delimiter='\t')
    assert len(converted_data) == 57
    assert converted_data[0]['a'] == '127.0.0.1'
    assert converted_data[0]['b'] == 'bireysel---sube--giris--tr.com'
    assert converted_data[9]['a'] == '127.0.0.1'
    assert converted_data[9]['b'] == 'bireysel-zîraat.com'
