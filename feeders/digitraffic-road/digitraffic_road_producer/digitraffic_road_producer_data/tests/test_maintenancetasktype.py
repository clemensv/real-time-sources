"""
Test case for MaintenanceTaskType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.maintenancetasktype import MaintenanceTaskType


class Test_MaintenanceTaskType(unittest.TestCase):
    """
    Test case for MaintenanceTaskType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MaintenanceTaskType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MaintenanceTaskType for testing
        """
        instance = MaintenanceTaskType(
            task_id='cdgtqpstjmfnmoemjxwe',
            name_fi='mmswdnxivzueryxfktoh',
            name_en='izvreaqxlrufakxopkks',
            name_sv='thwmdxtwxquwzsgtcnfo',
            data_updated_time='wbpybxbifwxqdsmxxuuv'
        )
        return instance

    
    def test_task_id_property(self):
        """
        Test task_id property
        """
        test_value = 'cdgtqpstjmfnmoemjxwe'
        self.instance.task_id = test_value
        self.assertEqual(self.instance.task_id, test_value)
    
    def test_name_fi_property(self):
        """
        Test name_fi property
        """
        test_value = 'mmswdnxivzueryxfktoh'
        self.instance.name_fi = test_value
        self.assertEqual(self.instance.name_fi, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'izvreaqxlrufakxopkks'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_name_sv_property(self):
        """
        Test name_sv property
        """
        test_value = 'thwmdxtwxquwzsgtcnfo'
        self.instance.name_sv = test_value
        self.assertEqual(self.instance.name_sv, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'wbpybxbifwxqdsmxxuuv'
        self.instance.data_updated_time = test_value
        self.assertEqual(self.instance.data_updated_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MaintenanceTaskType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MaintenanceTaskType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

