"""
Test case for TidewaterStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_mqtt_producer_data.tidewaterstation import TidewaterStation
from dmi_mqtt_producer_data.countryenum import CountryEnum
import datetime


class Test_TidewaterStation(unittest.TestCase):
    """
    Test case for TidewaterStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TidewaterStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TidewaterStation for testing
        """
        instance = TidewaterStation(
            station_id='qikyyraatyecwucjtetf',
            name='gpvexazcnivviseaqvvn',
            country=CountryEnum.DNK,
            owner='bvuicpyzesbclpkrkdmq',
            latitude=float(91.71993949865637),
            longitude=float(90.05237351096446),
            valid_from=datetime.datetime.now(datetime.timezone.utc),
            valid_to=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'qikyyraatyecwucjtetf'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'gpvexazcnivviseaqvvn'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = CountryEnum.DNK
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'bvuicpyzesbclpkrkdmq'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(91.71993949865637)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(90.05237351096446)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TidewaterStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TidewaterStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

