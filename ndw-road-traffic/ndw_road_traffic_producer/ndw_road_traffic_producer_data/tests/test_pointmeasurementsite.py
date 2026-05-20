"""
Test case for PointMeasurementSite
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.pointmeasurementsite import PointMeasurementSite


class Test_PointMeasurementSite(unittest.TestCase):
    """
    Test case for PointMeasurementSite
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PointMeasurementSite.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PointMeasurementSite for testing
        """
        instance = PointMeasurementSite(
            measurement_site_id='iawsurfcubfayfhchgdl',
            name='hkzmcnpgrbqtfbaphrsr',
            measurement_site_type='qwtjvhiappatdibvmepo',
            period=int(6),
            latitude=float(43.84508939873809),
            longitude=float(24.227135200210714),
            road_name='ulxncccqvpnkszofmzas',
            lane_count=int(82),
            carriageway_type='btkjaeqsbkkxdducomhb'
        )
        return instance

    
    def test_measurement_site_id_property(self):
        """
        Test measurement_site_id property
        """
        test_value = 'iawsurfcubfayfhchgdl'
        self.instance.measurement_site_id = test_value
        self.assertEqual(self.instance.measurement_site_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hkzmcnpgrbqtfbaphrsr'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_measurement_site_type_property(self):
        """
        Test measurement_site_type property
        """
        test_value = 'qwtjvhiappatdibvmepo'
        self.instance.measurement_site_type = test_value
        self.assertEqual(self.instance.measurement_site_type, test_value)
    
    def test_period_property(self):
        """
        Test period property
        """
        test_value = int(6)
        self.instance.period = test_value
        self.assertEqual(self.instance.period, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(43.84508939873809)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(24.227135200210714)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_road_name_property(self):
        """
        Test road_name property
        """
        test_value = 'ulxncccqvpnkszofmzas'
        self.instance.road_name = test_value
        self.assertEqual(self.instance.road_name, test_value)
    
    def test_lane_count_property(self):
        """
        Test lane_count property
        """
        test_value = int(82)
        self.instance.lane_count = test_value
        self.assertEqual(self.instance.lane_count, test_value)
    
    def test_carriageway_type_property(self):
        """
        Test carriageway_type property
        """
        test_value = 'btkjaeqsbkkxdducomhb'
        self.instance.carriageway_type = test_value
        self.assertEqual(self.instance.carriageway_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PointMeasurementSite.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PointMeasurementSite.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

