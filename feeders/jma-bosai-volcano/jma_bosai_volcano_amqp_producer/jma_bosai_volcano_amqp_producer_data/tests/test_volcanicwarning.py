"""
Test case for VolcanicWarning
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_amqp_producer_data.volcanicwarning import VolcanicWarning
from jma_bosai_volcano_amqp_producer_data.eventenum import EventEnum
from jma_bosai_volcano_amqp_producer_data.alertlevelcodeenum import AlertLevelCodeenum
from jma_bosai_volcano_amqp_producer_data.conditionenum import ConditionEnum
import datetime


class Test_VolcanicWarning(unittest.TestCase):
    """
    Test case for VolcanicWarning
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VolcanicWarning.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanicWarning for testing
        """
        instance = VolcanicWarning(
            volcano_code='mjjvanaqhjcuywrqrdhc',
            event_id='vzpogxxjrmseutjvdqss',
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            alert_level_code=AlertLevelCodeenum.CODE_02,
            alert_level_name='nvmogczxopwbapdefxhy',
            previous_level_code='onwfmamkjapqkihywwmp',
            condition=ConditionEnum.ISSUED,
            info_type_jp='jlojmwcdxksnwjnfiiqp',
            area_codes=['vjzjcqmuybpsbbviofhk'],
            prefecture='pvrsneygulidmqeptesk',
            event=EventEnum.warning
        )
        return instance

    
    def test_volcano_code_property(self):
        """
        Test volcano_code property
        """
        test_value = 'mjjvanaqhjcuywrqrdhc'
        self.instance.volcano_code = test_value
        self.assertEqual(self.instance.volcano_code, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'vzpogxxjrmseutjvdqss'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_report_datetime_property(self):
        """
        Test report_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime = test_value
        self.assertEqual(self.instance.report_datetime, test_value)
    
    def test_report_datetime_local_property(self):
        """
        Test report_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime_local = test_value
        self.assertEqual(self.instance.report_datetime_local, test_value)
    
    def test_alert_level_code_property(self):
        """
        Test alert_level_code property
        """
        test_value = AlertLevelCodeenum.CODE_02
        self.instance.alert_level_code = test_value
        self.assertEqual(self.instance.alert_level_code, test_value)
    
    def test_alert_level_name_property(self):
        """
        Test alert_level_name property
        """
        test_value = 'nvmogczxopwbapdefxhy'
        self.instance.alert_level_name = test_value
        self.assertEqual(self.instance.alert_level_name, test_value)
    
    def test_previous_level_code_property(self):
        """
        Test previous_level_code property
        """
        test_value = 'onwfmamkjapqkihywwmp'
        self.instance.previous_level_code = test_value
        self.assertEqual(self.instance.previous_level_code, test_value)
    
    def test_condition_property(self):
        """
        Test condition property
        """
        test_value = ConditionEnum.ISSUED
        self.instance.condition = test_value
        self.assertEqual(self.instance.condition, test_value)
    
    def test_info_type_jp_property(self):
        """
        Test info_type_jp property
        """
        test_value = 'jlojmwcdxksnwjnfiiqp'
        self.instance.info_type_jp = test_value
        self.assertEqual(self.instance.info_type_jp, test_value)
    
    def test_area_codes_property(self):
        """
        Test area_codes property
        """
        test_value = ['vjzjcqmuybpsbbviofhk']
        self.instance.area_codes = test_value
        self.assertEqual(self.instance.area_codes, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'pvrsneygulidmqeptesk'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
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
        new_instance = VolcanicWarning.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VolcanicWarning.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

