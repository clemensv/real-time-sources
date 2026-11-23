"""
Test case for Parameter
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_amqp_producer_data.usgs.waterdata.parameter import Parameter
from usgs_waterdata_amqp_producer_data.usgs.waterdata.parametermetadata import ParameterMetadata


class Test_Parameter(unittest.TestCase):
    """
    Test case for Parameter
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Parameter.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Parameter for testing
        """
        instance = Parameter(
            time_series_id='pluwbtpbmeloiihjqkkf',
            parameter=None
        )
        return instance

    
    def test_time_series_id_property(self):
        """
        Test time_series_id property
        """
        test_value = 'pluwbtpbmeloiihjqkkf'
        self.instance.time_series_id = test_value
        self.assertEqual(self.instance.time_series_id, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = None
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Parameter.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Parameter.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

