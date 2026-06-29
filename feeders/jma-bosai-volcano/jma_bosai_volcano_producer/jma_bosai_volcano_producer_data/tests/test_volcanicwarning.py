"""
Test case for VolcanicWarning
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_producer_data.volcanicwarning import VolcanicWarning
from jma_bosai_volcano_producer_data.volcanicwarningeventenum import VolcanicWarningEventEnum
from jma_bosai_volcano_producer_data.conditionenum import ConditionEnum
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
            volcano_code='aphalkennbnhwemnxoaf',
            event_id='lixlznfbkjzxqlxghnin',
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            alert_level_code='dqzcnpdwixdgvjawzzzi',
            alert_level_name='kxcftooklscohdvhsghg',
            previous_level_code='ofnzdurdctxckhnamfod',
            condition=ConditionEnum.ISSUED,
            info_type_jp='vxitnizbutwxahlekfzk',
            area_codes=['xxnlpmbsnsustfjmahsg', 'hdhyzifesbpjfxxugrgk', 'fgzbwroqkuaajauulgul', 'oksdvchcfqnzjxxsbzsf', 'txhcpxhscuumphvkmmjf'],
            prefecture='frwfamdhcaxzavcretzu',
            event=VolcanicWarningEventEnum.warning
        )
        return instance

    
    def test_volcano_code_property(self):
        """
        Test volcano_code property
        """
        test_value = 'aphalkennbnhwemnxoaf'
        self.instance.volcano_code = test_value
        self.assertEqual(self.instance.volcano_code, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'lixlznfbkjzxqlxghnin'
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
        test_value = 'dqzcnpdwixdgvjawzzzi'
        self.instance.alert_level_code = test_value
        self.assertEqual(self.instance.alert_level_code, test_value)
    
    def test_alert_level_name_property(self):
        """
        Test alert_level_name property
        """
        test_value = 'kxcftooklscohdvhsghg'
        self.instance.alert_level_name = test_value
        self.assertEqual(self.instance.alert_level_name, test_value)
    
    def test_previous_level_code_property(self):
        """
        Test previous_level_code property
        """
        test_value = 'ofnzdurdctxckhnamfod'
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
        test_value = 'vxitnizbutwxahlekfzk'
        self.instance.info_type_jp = test_value
        self.assertEqual(self.instance.info_type_jp, test_value)
    
    def test_area_codes_property(self):
        """
        Test area_codes property
        """
        test_value = ['xxnlpmbsnsustfjmahsg', 'hdhyzifesbpjfxxugrgk', 'fgzbwroqkuaajauulgul', 'oksdvchcfqnzjxxsbzsf', 'txhcpxhscuumphvkmmjf']
        self.instance.area_codes = test_value
        self.assertEqual(self.instance.area_codes, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'frwfamdhcaxzavcretzu'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = VolcanicWarningEventEnum.warning
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

