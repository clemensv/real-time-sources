"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fmi_finland_producer_data.fi.fmi.opendata.airquality.station import Station


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
            fmisid='ouhdadcaagjqmuyluren',
            station_name='cfayxqckfooncleqwllq',
            latitude=float(34.84103644433701),
            longitude=float(3.048951517530707),
            municipality='abwoogogndbdjgufwoyx'
        )
        return instance

    
    def test_fmisid_property(self):
        """
        Test fmisid property
        """
        test_value = 'ouhdadcaagjqmuyluren'
        self.instance.fmisid = test_value
        self.assertEqual(self.instance.fmisid, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'cfayxqckfooncleqwllq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(34.84103644433701)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(3.048951517530707)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'abwoogogndbdjgufwoyx'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
