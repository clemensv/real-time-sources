"""
Test case for ContinuousObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_producer_data.usgs.waterdata.continuousobservation import ContinuousObservation
from usgs_waterdata_producer_data.usgs.waterdata.point import Point
import datetime


class Test_ContinuousObservation(unittest.TestCase):
    """
    Test case for ContinuousObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ContinuousObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ContinuousObservation for testing
        """
        instance = ContinuousObservation(
            time_series_id='zhgpdizlgrbdmvdhskdk',
            monitoring_location_id='zhbxnsheqfdtnxvkraxd',
            parameter_code='bojtmvffwyjeqkiqpdzb',
            statistic_id='filcgctapusybipzcdzo',
            time=datetime.datetime.now(datetime.timezone.utc),
            value='uuifxqwyfaxruuxzqdik',
            unit_of_measure='dvjblygvallvlzfoncva',
            approval_status='rfylpzapvhvqxkhgbgpj',
            qualifier='ricvtihmapwijblfjarn',
            last_modified=datetime.datetime.now(datetime.timezone.utc),
            method_category='axwqutmiweujjnmbyxyd',
            geometry=None,
            feature_id='pqlsucsnzadlykbiiqvq'
        )
        return instance

    
    def test_time_series_id_property(self):
        """
        Test time_series_id property
        """
        test_value = 'zhgpdizlgrbdmvdhskdk'
        self.instance.time_series_id = test_value
        self.assertEqual(self.instance.time_series_id, test_value)
    
    def test_monitoring_location_id_property(self):
        """
        Test monitoring_location_id property
        """
        test_value = 'zhbxnsheqfdtnxvkraxd'
        self.instance.monitoring_location_id = test_value
        self.assertEqual(self.instance.monitoring_location_id, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'bojtmvffwyjeqkiqpdzb'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_statistic_id_property(self):
        """
        Test statistic_id property
        """
        test_value = 'filcgctapusybipzcdzo'
        self.instance.statistic_id = test_value
        self.assertEqual(self.instance.statistic_id, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = 'uuifxqwyfaxruuxzqdik'
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_of_measure_property(self):
        """
        Test unit_of_measure property
        """
        test_value = 'dvjblygvallvlzfoncva'
        self.instance.unit_of_measure = test_value
        self.assertEqual(self.instance.unit_of_measure, test_value)
    
    def test_approval_status_property(self):
        """
        Test approval_status property
        """
        test_value = 'rfylpzapvhvqxkhgbgpj'
        self.instance.approval_status = test_value
        self.assertEqual(self.instance.approval_status, test_value)
    
    def test_qualifier_property(self):
        """
        Test qualifier property
        """
        test_value = 'ricvtihmapwijblfjarn'
        self.instance.qualifier = test_value
        self.assertEqual(self.instance.qualifier, test_value)
    
    def test_last_modified_property(self):
        """
        Test last_modified property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.last_modified = test_value
        self.assertEqual(self.instance.last_modified, test_value)
    
    def test_method_category_property(self):
        """
        Test method_category property
        """
        test_value = 'axwqutmiweujjnmbyxyd'
        self.instance.method_category = test_value
        self.assertEqual(self.instance.method_category, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = None
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_feature_id_property(self):
        """
        Test feature_id property
        """
        test_value = 'pqlsucsnzadlykbiiqvq'
        self.instance.feature_id = test_value
        self.assertEqual(self.instance.feature_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ContinuousObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ContinuousObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

