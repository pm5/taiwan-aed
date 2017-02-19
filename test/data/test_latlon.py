#!/usr/bin/env python

import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.curdir, 'lib'))
from crawler.data import get_all_saved_ids, get_data
from crawler.logging import default_logger as logger


class LatLonTest(unittest.TestCase):

    @unittest.expectedFailure
    def test_aed_latlon_and_place_latlon(self):
        for pid in get_all_saved_ids():
            data = get_data(pid)
            if data['aed']['AED經緯度']['x'] != data['place']['場所經緯度']['x']:
                logger.warning(
                    '{pid} has mismatched lon between place and aed'.format(pid=pid))
            if data['aed']['AED經緯度']['y'] != data['place']['場所經緯度']['y']:
                logger.warning(
                    '{pid} has mismatched lat between place and aed'.format(pid=pid))

if __name__ == "__main__":
    unittest.main()
