"""
Test case for StationMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.stationmetadata import StationMetadata


class Test_StationMetadata(unittest.TestCase):
    """
    Test case for StationMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationMetadata for testing
        """
        instance = StationMetadata(
            station_id='bbxczjabtcoxnutbqryk',
            station_name='wtxsxmfkwxaazymolgsv',
            latitude=float(12.12342266324482),
            longitude=float(66.33852314812091),
            elevation=float(78.02314607078537),
            state='ogzaqylxsqkrisomdfxg',
            from_date='qbasnsiaowjpaavottns',
            to_date='aobeavtsldgyupyvmoms'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bbxczjabtcoxnutbqryk'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'wtxsxmfkwxaazymolgsv'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(12.12342266324482)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(66.33852314812091)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(78.02314607078537)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'ogzaqylxsqkrisomdfxg'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_from_date_property(self):
        """
        Test from_date property
        """
        test_value = 'qbasnsiaowjpaavottns'
        self.instance.from_date = test_value
        self.assertEqual(self.instance.from_date, test_value)
    
    def test_to_date_property(self):
        """
        Test to_date property
        """
        test_value = 'aobeavtsldgyupyvmoms'
        self.instance.to_date = test_value
        self.assertEqual(self.instance.to_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

