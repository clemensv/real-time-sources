"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_producer_data.be.irail.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_id='wmrfjjijlydqcaawvmdk',
            name='hoyzacxuoncjehlstyuj',
            standard_name='rthiqliprffwuhjipqro',
            longitude=float(27.174811866776572),
            latitude=float(10.789824293453554),
            uri='qokvklbapxevzhakmvdv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'wmrfjjijlydqcaawvmdk'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hoyzacxuoncjehlstyuj'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_standard_name_property(self):
        """
        Test standard_name property
        """
        test_value = 'rthiqliprffwuhjipqro'
        self.instance.standard_name = test_value
        self.assertEqual(self.instance.standard_name, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(27.174811866776572)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(10.789824293453554)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'qokvklbapxevzhakmvdv'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
