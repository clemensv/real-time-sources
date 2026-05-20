"""
Test case for WarningItem
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.warningitem import WarningItem
from jma_bosai_warning_producer_data.severityenum import SeverityEnum
from jma_bosai_warning_producer_data.statusenum import StatusEnum


class Test_WarningItem(unittest.TestCase):
    """
    Test case for WarningItem
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WarningItem.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WarningItem for testing
        """
        instance = WarningItem(
            code='zcdiobqtsmnvdbornllb',
            code_description_jp='wncdpqehukdexcvtfxam',
            code_description_en='uwiolewirortcbrsrrwt',
            status=StatusEnum.ISSUED,
            severity=SeverityEnum.NONE
        )
        return instance

    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'zcdiobqtsmnvdbornllb'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_code_description_jp_property(self):
        """
        Test code_description_jp property
        """
        test_value = 'wncdpqehukdexcvtfxam'
        self.instance.code_description_jp = test_value
        self.assertEqual(self.instance.code_description_jp, test_value)
    
    def test_code_description_en_property(self):
        """
        Test code_description_en property
        """
        test_value = 'uwiolewirortcbrsrrwt'
        self.instance.code_description_en = test_value
        self.assertEqual(self.instance.code_description_en, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = StatusEnum.ISSUED
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.NONE
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WarningItem.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WarningItem.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

