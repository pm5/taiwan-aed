#!/usr/bin/env python

import requests
from lxml import html, etree
import re
import os

list_url = 'http://tw-aed.mohw.gov.tw/SearchPlace.jsp?Action=Search&intPage={page_num}'
details_url = 'http://tw-aed.mohw.gov.tw/ShowPlace.jsp?PlaceID={place_id}'
tmp_dir = './tmp'
tmp_filename = './tmp/{place_id}.html'


def save_html(place_id, force=False):
    """
    Save HTML of the ith entry.
    """
    if not force and os.access(tmp_filename.format(place_id=place_id), os.R_OK):
        return -1
    r = requests.get(details_url.format(place_id=place_id))
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    tree = html.fromstring(r.content.decode('utf-8'))
    with open(tmp_filename.format(place_id=place_id), 'w') as f:
        f.write(etree.tostring(tree.xpath(
            '//div[@class="content2"]')[0], encoding='unicode'))
    return len(r.content)


def get_ids_in_list(page_num):
    """
    Get a list of IDs in the list page.
    """
    r = requests.get(list_url.format(page_num=page_num))
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    tree = html.fromstring(r.content)
    results_list, page_counter = tree.xpath('//table')[1:3]
    results = {
        'counter': parse_page_counter(page_counter),
        'ids': [parse_place_id(result)
                for result in results_list.xpath('./tr')[1:]],
    }
    return results


def parse_page_counter(page_counter):
    """
    Get page counter information.
    """
    page_counter_text = page_counter.findtext('.//font')
    r = re.match('當前第(\d+)頁/共(\d+)頁', page_counter_text)
    return {'current': r.group(1), 'total': r.group(2)}


def parse_place_id(result):
    """
    Get ID from result.
    """
    return result.findtext('.//div')


def read_html(place_id):
    with open(tmp_filename.format(place_id=place_id), 'r') as f:
        return f.read()


def tree_html(place_id):
    return html.fromstring(read_html(place_id))


def all_ids():
    return [
        place_id.replace('.html', '') for place_id in os.listdir(tmp_dir) if place_id.find('.html') > -1
    ]
