"""
Test case for BuoyStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_ndbc_producer_data.microsoft.opendata.us.noaa.ndbc.buoystation import BuoyStation


class Test_BuoyStation(unittest.TestCase):
    """
    Test case for BuoyStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BuoyStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BuoyStation for testing
        """
        instance = BuoyStation(
            station_id='jgetfxbqvrhemxshxjdn',
            owner='dhrclmjfsszpaysiamam',
            station_type='skdzshrueyscbvtugyxo',
            hull='dwyoxwystdfckvkdwjuq',
            name='tlfvlihowihkhzqkbdkq',
            latitude=float(96.0774771170518),
            longitude=float(82.87603844206437),
            timezone='yhdcbbysfnifjadcwrxm'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jgetfxbqvrhemxshxjdn'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'dhrclmjfsszpaysiamam'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'skdzshrueyscbvtugyxo'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_hull_property(self):
        """
        Test hull property
        """
        test_value = 'dwyoxwystdfckvkdwjuq'
        self.instance.hull = test_value
        self.assertEqual(self.instance.hull, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'tlfvlihowihkhzqkbdkq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(96.0774771170518)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(82.87603844206437)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'yhdcbbysfnifjadcwrxm'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BuoyStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
