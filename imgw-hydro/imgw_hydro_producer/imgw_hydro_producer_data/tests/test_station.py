"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from imgw_hydro_producer_data.station import Station


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
            id_stacji='xqrktabkwkuralfvdrya',
            stacja='jhxzbsnggqiikjwckcmc',
            rzeka='svlwiikefauydespepbg',
            wojewodztwo='lowhgloyeogrlhpsywml',
            longitude=float(66.84017725065847),
            latitude=float(84.5939805870382)
        )
        return instance

    
    def test_id_stacji_property(self):
        """
        Test id_stacji property
        """
        test_value = 'xqrktabkwkuralfvdrya'
        self.instance.id_stacji = test_value
        self.assertEqual(self.instance.id_stacji, test_value)
    
    def test_stacja_property(self):
        """
        Test stacja property
        """
        test_value = 'jhxzbsnggqiikjwckcmc'
        self.instance.stacja = test_value
        self.assertEqual(self.instance.stacja, test_value)
    
    def test_rzeka_property(self):
        """
        Test rzeka property
        """
        test_value = 'svlwiikefauydespepbg'
        self.instance.rzeka = test_value
        self.assertEqual(self.instance.rzeka, test_value)
    
    def test_wojewodztwo_property(self):
        """
        Test wojewodztwo property
        """
        test_value = 'lowhgloyeogrlhpsywml'
        self.instance.wojewodztwo = test_value
        self.assertEqual(self.instance.wojewodztwo, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(66.84017725065847)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(84.5939805870382)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

