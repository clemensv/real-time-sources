"""
Test case for WeatherAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_alerts_producer_data.weatheralert import WeatherAlert
from nws_alerts_producer_data.certaintyenum import CertaintyEnum
from nws_alerts_producer_data.severityenum import SeverityEnum
from nws_alerts_producer_data.urgencyenum import UrgencyEnum
from nws_alerts_producer_data.messagetypeenum import MessageTypeenum
from nws_alerts_producer_data.statusenum import StatusEnum
import datetime


class Test_WeatherAlert(unittest.TestCase):
    """
    Test case for WeatherAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherAlert for testing
        """
        instance = WeatherAlert(
            alert_id='qkocnvopesgeypfivbnh',
            area_desc='vimpkczbibnylcuechip',
            same_codes='umofbnuysklsmyzttyqq',
            ugc_codes='wfladtzwhkqxkvtwpcfl',
            sent=datetime.datetime.now(datetime.timezone.utc),
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            ends=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            message_type=MessageTypeenum.Alert,
            category='labipkbqicpzlqhiznei',
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            urgency=UrgencyEnum.Immediate,
            event='jxqngiwekneemgshnrkn',
            sender='shudqnfgxmhrvyvgfewp',
            sender_name='lnwqwbkxowwhjnflzhpr',
            headline='ylnzvjtxvtcfzuedfxrt',
            description='dhrdvfjmswsjxmgqnroi',
            instruction='wqgmpkzekulfjostgkqy',
            response='imvsfhdpoodzrjbbqtpw',
            scope='qptioijdgtufxgoaqvev',
            code='izimctvtqhpekrsmujmc',
            nws_headline='bwsjicdtnapbbrqozpqy',
            vtec='hokhcopozgutenitrzyg',
            web='kiumdfugtiwiattqzrbz'
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'qkocnvopesgeypfivbnh'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'vimpkczbibnylcuechip'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_same_codes_property(self):
        """
        Test same_codes property
        """
        test_value = 'umofbnuysklsmyzttyqq'
        self.instance.same_codes = test_value
        self.assertEqual(self.instance.same_codes, test_value)
    
    def test_ugc_codes_property(self):
        """
        Test ugc_codes property
        """
        test_value = 'wfladtzwhkqxkvtwpcfl'
        self.instance.ugc_codes = test_value
        self.assertEqual(self.instance.ugc_codes, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_effective_property(self):
        """
        Test effective property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.effective = test_value
        self.assertEqual(self.instance.effective, test_value)
    
    def test_onset_property(self):
        """
        Test onset property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.onset = test_value
        self.assertEqual(self.instance.onset, test_value)
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
    def test_ends_property(self):
        """
        Test ends property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ends = test_value
        self.assertEqual(self.instance.ends, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = StatusEnum.Actual
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_message_type_property(self):
        """
        Test message_type property
        """
        test_value = MessageTypeenum.Alert
        self.instance.message_type = test_value
        self.assertEqual(self.instance.message_type, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'labipkbqicpzlqhiznei'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.Extreme
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = CertaintyEnum.Observed
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = UrgencyEnum.Immediate
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'jxqngiwekneemgshnrkn'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'shudqnfgxmhrvyvgfewp'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'lnwqwbkxowwhjnflzhpr'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'ylnzvjtxvtcfzuedfxrt'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'dhrdvfjmswsjxmgqnroi'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_instruction_property(self):
        """
        Test instruction property
        """
        test_value = 'wqgmpkzekulfjostgkqy'
        self.instance.instruction = test_value
        self.assertEqual(self.instance.instruction, test_value)
    
    def test_response_property(self):
        """
        Test response property
        """
        test_value = 'imvsfhdpoodzrjbbqtpw'
        self.instance.response = test_value
        self.assertEqual(self.instance.response, test_value)
    
    def test_scope_property(self):
        """
        Test scope property
        """
        test_value = 'qptioijdgtufxgoaqvev'
        self.instance.scope = test_value
        self.assertEqual(self.instance.scope, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'izimctvtqhpekrsmujmc'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_nws_headline_property(self):
        """
        Test nws_headline property
        """
        test_value = 'bwsjicdtnapbbrqozpqy'
        self.instance.nws_headline = test_value
        self.assertEqual(self.instance.nws_headline, test_value)
    
    def test_vtec_property(self):
        """
        Test vtec property
        """
        test_value = 'hokhcopozgutenitrzyg'
        self.instance.vtec = test_value
        self.assertEqual(self.instance.vtec, test_value)
    
    def test_web_property(self):
        """
        Test web property
        """
        test_value = 'kiumdfugtiwiattqzrbz'
        self.instance.web = test_value
        self.assertEqual(self.instance.web, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

