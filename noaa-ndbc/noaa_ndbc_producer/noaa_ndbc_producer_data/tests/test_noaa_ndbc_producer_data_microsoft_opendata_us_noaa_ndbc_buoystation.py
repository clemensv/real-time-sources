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
            station_id='uyahmcuxybxjyonwecog',
            owner='sqjjgkkfemvxpudkdvyd',
            station_type='zslgrpchwqpprhracmvd',
            hull='tzcdgzqzcwyecnerudaj',
            name='afzxykkbksthnvcfvyaw',
            latitude=float(98.36210392985726),
            longitude=float(53.54694635020307),
            timezone='qefhbhnmaywfslwbzfmp'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'uyahmcuxybxjyonwecog'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'sqjjgkkfemvxpudkdvyd'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'zslgrpchwqpprhracmvd'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_hull_property(self):
        """
        Test hull property
        """
        test_value = 'tzcdgzqzcwyecnerudaj'
        self.instance.hull = test_value
        self.assertEqual(self.instance.hull, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'afzxykkbksthnvcfvyaw'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(98.36210392985726)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(53.54694635020307)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'qefhbhnmaywfslwbzfmp'
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
