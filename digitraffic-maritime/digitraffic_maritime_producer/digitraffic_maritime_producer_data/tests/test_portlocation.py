"""
Test case for PortLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.portlocation import PortLocation
from digitraffic_maritime_producer_data.portarea import PortArea
from digitraffic_maritime_producer_data.berth import Berth
import datetime


class Test_PortLocation(unittest.TestCase):
    """
    Test case for PortLocation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PortLocation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PortLocation for testing
        """
        instance = PortLocation(
            locode='uxikuqprpxqiunyaejus',
            data_updated_time=datetime.datetime.now(datetime.timezone.utc),
            location_name='qnkazjzvcvzzbxvggsmx',
            country='wbniyutiluqlbzkjappi',
            longitude=float(39.54394184743767),
            latitude=float(62.49799126211494),
            port_areas=[None, None],
            berths=[None, None, None, None, None]
        )
        return instance

    
    def test_locode_property(self):
        """
        Test locode property
        """
        test_value = 'uxikuqprpxqiunyaejus'
        self.instance.locode = test_value
        self.assertEqual(self.instance.locode, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.data_updated_time = test_value
        self.assertEqual(self.instance.data_updated_time, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'qnkazjzvcvzzbxvggsmx'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'wbniyutiluqlbzkjappi'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(39.54394184743767)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(62.49799126211494)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_port_areas_property(self):
        """
        Test port_areas property
        """
        test_value = [None, None]
        self.instance.port_areas = test_value
        self.assertEqual(self.instance.port_areas, test_value)
    
    def test_berths_property(self):
        """
        Test berths property
        """
        test_value = [None, None, None, None, None]
        self.instance.berths = test_value
        self.assertEqual(self.instance.berths, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PortLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PortLocation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

