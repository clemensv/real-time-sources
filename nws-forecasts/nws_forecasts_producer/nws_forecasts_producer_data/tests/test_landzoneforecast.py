"""
Test case for LandZoneForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_forecasts_producer_data.landzoneforecast import LandZoneForecast
from nws_forecasts_producer_data.landforecastperiod import LandForecastPeriod
import datetime


class Test_LandZoneForecast(unittest.TestCase):
    """
    Test case for LandZoneForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LandZoneForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LandZoneForecast for testing
        """
        instance = LandZoneForecast(
            zone_id='ulisnxxsxlcamcigdtur',
            updated=datetime.datetime.now(datetime.timezone.utc),
            periods=[None, None]
        )
        return instance

    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'ulisnxxsxlcamcigdtur'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_periods_property(self):
        """
        Test periods property
        """
        test_value = [None, None]
        self.instance.periods = test_value
        self.assertEqual(self.instance.periods, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LandZoneForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LandZoneForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

