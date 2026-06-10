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
            measurement_site_id='glgndtcajnfcmhirrlxq',
            name='vtnyebonhrxlrqzdxjto',
            measurement_site_type='pxvydelngxhtnrnnrdxg',
            period=int(78),
            start_latitude=float(3.3277016829985295),
            start_longitude=float(49.4375989176555),
            end_latitude=float(9.600601853354673),
            end_longitude=float(73.88297337781),
            road_name='cylcbttlblxqctrasyga',
            length_metres=float(68.84100610881082)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'glgndtcajnfcmhirrlxq'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'vtnyebonhrxlrqzdxjto'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_measurement_site_type_property(self):
        """
        Test measurement_site_type property
        """
        test_value = 'pxvydelngxhtnrnnrdxg'
        self.instance.measurement_site_type = test_value
        self.assertEqual(self.instance.measurement_site_type, test_value)
    
    def test_period_property(self):
        """
        Test period property
        """
        test_value = int(78)
        self.instance.period = test_value
        self.assertEqual(self.instance.period, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(3.3277016829985295)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(49.4375989176555)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(9.600601853354673)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(73.88297337781)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'cylcbttlblxqctrasyga'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_length_metres_property(self):
        """
        Test length_metres property
        """
        test_value = float(68.84100610881082)
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

