"""
Test case for Office
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.office import Office
from jma_bosai_warning_producer_data.officetypeenum import OfficeTypeenum
from jma_bosai_warning_producer_data.eventenum import EventEnum
from jma_bosai_warning_producer_data.severityenum import SeverityEnum


class Test_Office(unittest.TestCase):
    """
    Test case for Office
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Office.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Office for testing
        """
        instance = Office(
            office_code='aamcsxjlpqskqgkxqnwp',
            area_code='qiaybsyupkdgkxbobpxf',
            name_jp='smqsxwrzwqvkedkhnjlc',
            name_en='rlqqaukfnuoyuxisxkxa',
            parent_office_code='uwsxvfwbusyvbutpyhnv',
            office_type=OfficeTypeenum.PREFECTURE,
            prefecture='rvspdreirglveuullmqb',
            severity=SeverityEnum.info,
            event=EventEnum.warning
        )
        return instance

    
    def test_office_code_property(self):
        """
        Test office_code property
        """
        test_value = 'aamcsxjlpqskqgkxqnwp'
        self.instance.office_code = test_value
        self.assertEqual(self.instance.office_code, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'qiaybsyupkdgkxbobpxf'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_name_jp_property(self):
        """
        Test name_jp property
        """
        test_value = 'smqsxwrzwqvkedkhnjlc'
        self.instance.name_jp = test_value
        self.assertEqual(self.instance.name_jp, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'rlqqaukfnuoyuxisxkxa'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_parent_office_code_property(self):
        """
        Test parent_office_code property
        """
        test_value = 'uwsxvfwbusyvbutpyhnv'
        self.instance.parent_office_code = test_value
        self.assertEqual(self.instance.parent_office_code, test_value)
    
    def test_office_type_property(self):
        """
        Test office_type property
        """
        test_value = OfficeTypeenum.PREFECTURE
        self.instance.office_type = test_value
        self.assertEqual(self.instance.office_type, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'rvspdreirglveuullmqb'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.info
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = EventEnum.warning
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Office.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Office.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

