"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gios_poland_producer_data.station import Station


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
            station_id=int(34),
            station_code='skcvhxmkkisbtsbvfqko',
            name='dbgrfmpvbggamzsfuihm',
            latitude=float(95.31600181825),
            longitude=float(46.269423795868356),
            city_id=int(23),
            city_name='ofheemvykxlyettcvdgt',
            commune='duhdyyobpebpyjgejuew',
            district='sxqxyeizufyhhfpbubho',
            voivodeship='ysfxmqwmkunwazwwmwpq',
            street='noihcxyowmfwazutjayf'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(34)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'skcvhxmkkisbtsbvfqko'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'dbgrfmpvbggamzsfuihm'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(95.31600181825)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(46.269423795868356)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_city_id_property(self):
        """
        Test city_id property
        """
        test_value = int(23)
        self.instance.city_id = test_value
        self.assertEqual(self.instance.city_id, test_value)
    
    def test_city_name_property(self):
        """
        Test city_name property
        """
        test_value = 'ofheemvykxlyettcvdgt'
        self.instance.city_name = test_value
        self.assertEqual(self.instance.city_name, test_value)
    
    def test_commune_property(self):
        """
        Test commune property
        """
        test_value = 'duhdyyobpebpyjgejuew'
        self.instance.commune = test_value
        self.assertEqual(self.instance.commune, test_value)
    
    def test_district_property(self):
        """
        Test district property
        """
        test_value = 'sxqxyeizufyhhfpbubho'
        self.instance.district = test_value
        self.assertEqual(self.instance.district, test_value)
    
    def test_voivodeship_property(self):
        """
        Test voivodeship property
        """
        test_value = 'ysfxmqwmkunwazwwmwpq'
        self.instance.voivodeship = test_value
        self.assertEqual(self.instance.voivodeship, test_value)
    
    def test_street_property(self):
        """
        Test street property
        """
        test_value = 'noihcxyowmfwazutjayf'
        self.instance.street = test_value
        self.assertEqual(self.instance.street, test_value)
    
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

