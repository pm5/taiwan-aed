#!/usr/bin/env python

from .html import tree_html
import re
import json
import os

data_dir = './data'
data_filename = './data/{place_id}.json'


def parse_row(row):
    name = row.find('./th').text_content().strip().replace('：', '')
    value = row.find('./td').text_content().strip()

    if name.find("經緯度") > -1:
        lonlat_r = re.compile(r'([\d\.]+),([\d\.]+)')
        r = lonlat_r.search(value)
        if r:
            value = {
                'x': float(r.group(1)),
                'y': float(r.group(2)),
            }
    elif name.find("網址") > -1:
        value = row.find('./td/a').get('href')
        value = '' if value == 'http://' else value
    return (name, value)


def parse_place(place_tree):
    rows = place_tree.xpath('./tr')[1:]
    place = dict([parse_row(row) for row in rows])
    return place


def parse_aed(aed_tree):
    rows = aed_tree.xpath('./tr')[1:]
    aed = dict([parse_row(row) for row in rows])
    return aed


def parse_data(place_id):
    tree = tree_html(place_id)
    tables = tree.xpath('//table[@id="Ntable"]')
    if len(tables) == 4:
        place, aed = tables[0], tables[2]
    elif len(tables) == 2:
        place, aed = tables
    else:
        raise Exception('Unexpected number of tables')
    return {
        "place": parse_place(place),
        "aed": parse_aed(aed),
    }


def print_data(place_id):
    print(parse_data(place_id))


def get_json(place_id):
    return json.dumps(parse_data(place_id), ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def save_json(place_id, force=False):
    if not force and os.access(data_filename.format(place_id=place_id), os.R_OK):
        return -1
    with open(data_filename.format(place_id=place_id), 'w') as f:
        return f.write(get_json(place_id))

def get_data(place_id):
    with open(data_filename.format(place_id=place_id), 'r') as f:
        return json.loads(f.read())


def get_all_saved_ids():
    """
    Get a list of all item IDs that are saved.
    """
    return [
        place_id.replace('.json', '') for place_id in os.listdir(data_dir) if place_id.find('.json') > -1
    ]