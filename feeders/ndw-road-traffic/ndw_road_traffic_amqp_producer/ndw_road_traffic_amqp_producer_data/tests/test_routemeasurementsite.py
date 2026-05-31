"""
Test case for RouteMeasurementSite
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_amqp_producer_data.routemeasurementsite import RouteMeasurementSite


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
            measurement_site_id='dloegxvhifojgfmplfjm',
            name='zmfktepynphfzbsvxriv',
            measurement_site_type='pbyhpahrbfqchcvnmxgf',
            period=int(32),
            start_latitude=float(70.34232702344781),
            start_longitude=float(43.58507097288897),
            end_latitude=float(2.0948519073251015),
            end_longitude=float(30.34184309654875),
            road_name='ubhvhskchaywwmwnaaww',
            length_metres=float(52.236736255923624)
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'dloegxvhifojgfmplfjm'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'zmfktepynphfzbsvxriv'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_measurement_site_type_property(self):
        """
        Test measurement_site_type property
        """
        test_value = 'pbyhpahrbfqchcvnmxgf'
        self.instance.measurement_site_type = test_value
        self.assertEqual(self.instance.measurement_site_type, test_value)
    
    def test_period_property(self):
        """
        Test period property
        """
        test_value = int(32)
        self.instance.period = test_value
        self.assertEqual(self.instance.period, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(70.34232702344781)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(43.58507097288897)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(2.0948519073251015)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(30.34184309654875)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'ubhvhskchaywwmwnaaww'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_length_metres_property(self):
        """
        Test length_metres property
        """
        test_value = float(52.236736255923624)
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

