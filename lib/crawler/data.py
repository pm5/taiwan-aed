#!/usr/bin/env python

from .html import tree_html
from .logging import default_logger as logger
import re
import json
import csv
import os

data_dir = './data'
data_filename = './data/{place_id}.json'
data_csv_filename = './data/data.csv'


def parse_field(field):
    name = field.find('./th').text_content().strip().replace('：', '')
    value = field.find('./td').text_content().strip()

    if name.find('經緯度') > -1:
        lonlat_r = re.compile(r'(\d+\.\d+),\s*(\d+\.\d+)')
        r = lonlat_r.search(value)
        if r:
            value = {
                'x': float(r.group(1)),
                'y': float(r.group(2)),
            }
        else:
            logger.warn(
                'latlon field "{name}" convertion failed. unchanged.'.format(name=name))
            logger.debug(value)
    elif name.find('網址') > -1:
        value = field.find('./td/a').get('href')
        value = '' if value == 'http://' else value
    return (name, value)


def parse_place(place_tree):
    fields = place_tree.xpath('./tr')[1:]
    place = dict([parse_field(field) for field in fields])
    return place


def parse_aed(aed_tree):
    fields = aed_tree.xpath('./tr')[1:]
    aed = dict([parse_field(field) for field in fields])
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
        'place': parse_place(place),
        'aed': parse_aed(aed),
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


def get_csv(place_id):
    data = parse_data(place_id)
    result = {}
    for entry in ['place', 'aed']:
        for field in data[entry].keys():
            if field.find('經緯度') > -1:
                result[field + 'X'] = data[entry][field]['x']
                result[field + 'Y'] = data[entry][field]['y']
            else:
                result[field] = data[entry][field]
    return result


def save_csv(csv_data):
    with open(data_csv_filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[
            '場所名稱', '場所地址', '場所經緯度X', '場所經緯度Y',
            '場所類型', '場所網址', '場所描述',
            'AED放置地點', 'AED經緯度X', 'AED經緯度Y', 'AED地點描述',
            '開放使用時間', '開放使用時間緊急連絡電話', '資料建立時間',
        ])
        writer.writeheader()
        writer.writerows(csv_data)


def get_data(place_id):
    with open(data_filename.format(place_id=place_id), 'r') as f:
        return json.loads(f.read())


def get_all_saved_ids():
    '''
    Get a list of all item IDs that are saved.
    '''
    return [
        place_id.replace('.json', '') for place_id in os.listdir(data_dir) if place_id.find('.json') > -1
    ]
