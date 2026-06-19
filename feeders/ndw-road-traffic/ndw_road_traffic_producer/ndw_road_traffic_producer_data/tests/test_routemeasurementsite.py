"""
Test case for RouteMeasurementSite
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.routemeasurementsite import RouteMeasurementSite


class Test_RouteMeasurementSite(unittest.TestCase):
    """
    Test case for RouteMeasurementSite
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RouteMeasurementSite.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RouteMeasurementSite for testing
        """
        instance = RouteMeasurementSite(
            measurement_site_id='ocpwolciceuavpmdnbqy',
            name='wutqixtmotkzrrllaujl',
            measurement_site_type='ntllbglcotpwewljhsbe',
            period=int(89),
            start_latitude=float(13.868802461638252),
            start_longitude=float(62.695521716750505),
            end_latitude=float(1.90257258200357),
            end_longitude=float(98.5755697844716),
            road_name='kdrflrugunsuhifpczem',
            length_metres=float(1.0544516557310368)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'ocpwolciceuavpmdnbqy'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wutqixtmotkzrrllaujl'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_measurement_site_type_property(self):
        """
        Test measurement_site_type property
        """
        test_value = 'ntllbglcotpwewljhsbe'
        self.instance.measurement_site_type = test_value
        self.assertEqual(self.instance.measurement_site_type, test_value)
    
    def test_period_property(self):
        """
        Test period property
        """
        test_value = int(89)
        self.instance.period = test_value
        self.assertEqual(self.instance.period, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(13.868802461638252)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(62.695521716750505)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(1.90257258200357)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(98.5755697844716)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'kdrflrugunsuhifpczem'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_length_metres_property(self):
        """
        Test length_metres property
        """
        test_value = float(1.0544516557310368)
        self.instance.length_metres = test_value
        self.assertEqual(self.instance.length_metres, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RouteMeasurementSite.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RouteMeasurementSite.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

