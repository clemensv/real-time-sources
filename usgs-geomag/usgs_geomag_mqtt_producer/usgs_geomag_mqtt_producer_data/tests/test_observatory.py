"""
Test case for Observatory
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_geomag_mqtt_producer_data.observatory import Observatory


class Test_Observatory(unittest.TestCase):
    """
    Test case for Observatory
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observatory.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observatory for testing
        """
        instance = Observatory(
            iaga_code='nowykaioihnnadobmqsb',
            name='wjmvjxdsiecnpcwqkycy',
            agency='tbvqlvkkciyvhysgifwt',
            agency_name='siqwdesbudwegtrynpjp',
            latitude=float(41.62576511391492),
            longitude=float(7.706016669556403),
            elevation=float(43.623594593492165),
            sensor_orientation='qsjcljbfuhtlyyadfwmg',
            sensor_sampling_rate=float(24.29899627582488),
            declination_base=float(28.80896204101643)
        )
        return instance

    
    def test_iaga_code_property(self):
        """
        Test iaga_code property
        """
        test_value = 'nowykaioihnnadobmqsb'
        self.instance.iaga_code = test_value
        self.assertEqual(self.instance.iaga_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wjmvjxdsiecnpcwqkycy'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_agency_property(self):
        """
        Test agency property
        """
        test_value = 'tbvqlvkkciyvhysgifwt'
        self.instance.agency = test_value
        self.assertEqual(self.instance.agency, test_value)
    
    def test_agency_name_property(self):
        """
        Test agency_name property
        """
        test_value = 'siqwdesbudwegtrynpjp'
        self.instance.agency_name = test_value
        self.assertEqual(self.instance.agency_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(41.62576511391492)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(7.706016669556403)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(43.623594593492165)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_sensor_orientation_property(self):
        """
        Test sensor_orientation property
        """
        test_value = 'qsjcljbfuhtlyyadfwmg'
        self.instance.sensor_orientation = test_value
        self.assertEqual(self.instance.sensor_orientation, test_value)
    
    def test_sensor_sampling_rate_property(self):
        """
        Test sensor_sampling_rate property
        """
        test_value = float(24.29899627582488)
        self.instance.sensor_sampling_rate = test_value
        self.assertEqual(self.instance.sensor_sampling_rate, test_value)
    
    def test_declination_base_property(self):
        """
        Test declination_base property
        """
        test_value = float(28.80896204101643)
        self.instance.declination_base = test_value
        self.assertEqual(self.instance.declination_base, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observatory.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observatory.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

