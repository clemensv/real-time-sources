"""
Test case for RoadCorridor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tfl_road_traffic_producer_data.roadcorridor import RoadCorridor
import datetime


class Test_RoadCorridor(unittest.TestCase):
    """
    Test case for RoadCorridor
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadCorridor.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadCorridor for testing
        """
        instance = RoadCorridor(
            road_id='umwbtmgtkexbfeqxfkmt',
            display_name='iqonsxzjgvqavnzxafau',
            status_severity='xsfddlyozxqwgvtlqolp',
            status_severity_description='vppzmuusbwlxdpfshpkk',
            bounds='bdlvpcrpudmhqgwudgjh',
            envelope='sdwvadapjhdsszicqoau',
            url='ncrnqpcqdkrkaczvbjym',
            status_aggregation_start_date=datetime.datetime.now(datetime.timezone.utc),
            status_aggregation_end_date=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_road_id_property(self):
        """
        Test road_id property
        """
        test_value = 'umwbtmgtkexbfeqxfkmt'
        self.instance.road_id = test_value
        self.assertEqual(self.instance.road_id, test_value)
    
    def test_display_name_property(self):
        """
        Test display_name property
        """
        test_value = 'iqonsxzjgvqavnzxafau'
        self.instance.display_name = test_value
        self.assertEqual(self.instance.display_name, test_value)
    
    def test_status_severity_property(self):
        """
        Test status_severity property
        """
        test_value = 'xsfddlyozxqwgvtlqolp'
        self.instance.status_severity = test_value
        self.assertEqual(self.instance.status_severity, test_value)
    
    def test_status_severity_description_property(self):
        """
        Test status_severity_description property
        """
        test_value = 'vppzmuusbwlxdpfshpkk'
        self.instance.status_severity_description = test_value
        self.assertEqual(self.instance.status_severity_description, test_value)
    
    def test_bounds_property(self):
        """
        Test bounds property
        """
        test_value = 'bdlvpcrpudmhqgwudgjh'
        self.instance.bounds = test_value
        self.assertEqual(self.instance.bounds, test_value)
    
    def test_envelope_property(self):
        """
        Test envelope property
        """
        test_value = 'sdwvadapjhdsszicqoau'
        self.instance.envelope = test_value
        self.assertEqual(self.instance.envelope, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'ncrnqpcqdkrkaczvbjym'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_status_aggregation_start_date_property(self):
        """
        Test status_aggregation_start_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.status_aggregation_start_date = test_value
        self.assertEqual(self.instance.status_aggregation_start_date, test_value)
    
    def test_status_aggregation_end_date_property(self):
        """
        Test status_aggregation_end_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.status_aggregation_end_date = test_value
        self.assertEqual(self.instance.status_aggregation_end_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadCorridor.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RoadCorridor.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

