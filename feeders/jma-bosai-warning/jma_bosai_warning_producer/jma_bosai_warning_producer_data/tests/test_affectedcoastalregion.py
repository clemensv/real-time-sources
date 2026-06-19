"""
Test case for AffectedCoastalRegion
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.affectedcoastalregion import AffectedCoastalRegion
from jma_bosai_warning_producer_data.categoryenum import CategoryEnum
import datetime


class Test_AffectedCoastalRegion(unittest.TestCase):
    """
    Test case for AffectedCoastalRegion
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AffectedCoastalRegion.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AffectedCoastalRegion for testing
        """
        instance = AffectedCoastalRegion(
            code='riinkmxuoxbeydmeplry',
            name='wzcmwbikkxlthdckxcid',
            category=CategoryEnum.MAJOR_WARNING,
            expected_max_wave_height_m=float(7.2629570651315145),
            expected_arrival_datetime=datetime.datetime.now(datetime.timezone.utc),
            expected_arrival_datetime_local=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'riinkmxuoxbeydmeplry'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wzcmwbikkxlthdckxcid'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = CategoryEnum.MAJOR_WARNING
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_expected_max_wave_height_m_property(self):
        """
        Test expected_max_wave_height_m property
        """
        test_value = float(7.2629570651315145)
        self.instance.expected_max_wave_height_m = test_value
        self.assertEqual(self.instance.expected_max_wave_height_m, test_value)
    
    def test_expected_arrival_datetime_property(self):
        """
        Test expected_arrival_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expected_arrival_datetime = test_value
        self.assertEqual(self.instance.expected_arrival_datetime, test_value)
    
    def test_expected_arrival_datetime_local_property(self):
        """
        Test expected_arrival_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expected_arrival_datetime_local = test_value
        self.assertEqual(self.instance.expected_arrival_datetime_local, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AffectedCoastalRegion.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AffectedCoastalRegion.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

