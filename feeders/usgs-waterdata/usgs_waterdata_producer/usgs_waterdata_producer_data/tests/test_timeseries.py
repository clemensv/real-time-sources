"""
Test case for TimeSeries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_producer_data.usgs.waterdata.timeseries import TimeSeries
from usgs_waterdata_producer_data.usgs.waterdata.point import Point
from usgs_waterdata_producer_data.usgs.waterdata.threshold import Threshold
import datetime


class Test_TimeSeries(unittest.TestCase):
    """
    Test case for TimeSeries
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TimeSeries.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TimeSeries for testing
        """
        instance = TimeSeries(
            unit_of_measure='gsurgfwiwdwjlsuqvtba',
            parameter_name='rpqmkhppxcdvotcwmfzg',
            parameter_code='ocafhbhwtxvfwjqzpprg',
            statistic_id='rotektrglcwjstwvoiky',
            last_modified='dawrirvvtrejatgggaat',
            begin=datetime.datetime.now(datetime.timezone.utc),
            end=datetime.datetime.now(datetime.timezone.utc),
            computation_period_identifier='wygfrpamcxdikoapknvu',
            computation_identifier='ejfanrjzbtnebtoqgckg',
            thresholds=[None, None, None, None],
            sublocation_identifier='qpaezebshuqxrpjmcsve',
            primary='wdbssqjjxuawothswkwv',
            monitoring_location_id='gmmasxoyjfnbqvwewbdh',
            web_description='okufcdrpurinrwxjedgy',
            parameter_description='txxjdqrrgzpofurcvepf',
            parent_time_series_id='goxotzfhqfzymijernxj',
            data_gap_interval=datetime.timedelta(days=1),
            statistics_begin='vngaelldmkcunugoojik',
            time_series_id='oalnhrcjhvttphnawbkc',
            geometry=None
        )
        return instance

    
    def test_unit_of_measure_property(self):
        """
        Test unit_of_measure property
        """
        test_value = 'gsurgfwiwdwjlsuqvtba'
        self.instance.unit_of_measure = test_value
        self.assertEqual(self.instance.unit_of_measure, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'rpqmkhppxcdvotcwmfzg'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'ocafhbhwtxvfwjqzpprg'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_statistic_id_property(self):
        """
        Test statistic_id property
        """
        test_value = 'rotektrglcwjstwvoiky'
        self.instance.statistic_id = test_value
        self.assertEqual(self.instance.statistic_id, test_value)
    
    def test_last_modified_property(self):
        """
        Test last_modified property
        """
        test_value = 'dawrirvvtrejatgggaat'
        self.instance.last_modified = test_value
        self.assertEqual(self.instance.last_modified, test_value)
    
    def test_begin_property(self):
        """
        Test begin property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.begin = test_value
        self.assertEqual(self.instance.begin, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_computation_period_identifier_property(self):
        """
        Test computation_period_identifier property
        """
        test_value = 'wygfrpamcxdikoapknvu'
        self.instance.computation_period_identifier = test_value
        self.assertEqual(self.instance.computation_period_identifier, test_value)
    
    def test_computation_identifier_property(self):
        """
        Test computation_identifier property
        """
        test_value = 'ejfanrjzbtnebtoqgckg'
        self.instance.computation_identifier = test_value
        self.assertEqual(self.instance.computation_identifier, test_value)
    
    def test_thresholds_property(self):
        """
        Test thresholds property
        """
        test_value = [None, None, None, None]
        self.instance.thresholds = test_value
        self.assertEqual(self.instance.thresholds, test_value)
    
    def test_sublocation_identifier_property(self):
        """
        Test sublocation_identifier property
        """
        test_value = 'qpaezebshuqxrpjmcsve'
        self.instance.sublocation_identifier = test_value
        self.assertEqual(self.instance.sublocation_identifier, test_value)
    
    def test_primary_property(self):
        """
        Test primary property
        """
        test_value = 'wdbssqjjxuawothswkwv'
        self.instance.primary = test_value
        self.assertEqual(self.instance.primary, test_value)
    
    def test_monitoring_location_id_property(self):
        """
        Test monitoring_location_id property
        """
        test_value = 'gmmasxoyjfnbqvwewbdh'
        self.instance.monitoring_location_id = test_value
        self.assertEqual(self.instance.monitoring_location_id, test_value)
    
    def test_web_description_property(self):
        """
        Test web_description property
        """
        test_value = 'okufcdrpurinrwxjedgy'
        self.instance.web_description = test_value
        self.assertEqual(self.instance.web_description, test_value)
    
    def test_parameter_description_property(self):
        """
        Test parameter_description property
        """
        test_value = 'txxjdqrrgzpofurcvepf'
        self.instance.parameter_description = test_value
        self.assertEqual(self.instance.parameter_description, test_value)
    
    def test_parent_time_series_id_property(self):
        """
        Test parent_time_series_id property
        """
        test_value = 'goxotzfhqfzymijernxj'
        self.instance.parent_time_series_id = test_value
        self.assertEqual(self.instance.parent_time_series_id, test_value)
    
    def test_data_gap_interval_property(self):
        """
        Test data_gap_interval property
        """
        test_value = datetime.timedelta(days=1)
        self.instance.data_gap_interval = test_value
        self.assertEqual(self.instance.data_gap_interval, test_value)
    
    def test_statistics_begin_property(self):
        """
        Test statistics_begin property
        """
        test_value = 'vngaelldmkcunugoojik'
        self.instance.statistics_begin = test_value
        self.assertEqual(self.instance.statistics_begin, test_value)
    
    def test_time_series_id_property(self):
        """
        Test time_series_id property
        """
        test_value = 'oalnhrcjhvttphnawbkc'
        self.instance.time_series_id = test_value
        self.assertEqual(self.instance.time_series_id, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = None
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TimeSeries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TimeSeries.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

