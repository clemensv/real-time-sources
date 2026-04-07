"""
Test case for WeatherWarning
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from meteoalarm_producer_data.weatherwarning import WeatherWarning
from meteoalarm_producer_data.statusenum import StatusEnum
from meteoalarm_producer_data.urgencyenum import UrgencyEnum
from meteoalarm_producer_data.scopeenum import ScopeEnum
from meteoalarm_producer_data.certaintyenum import CertaintyEnum
from meteoalarm_producer_data.msgtypeenum import MsgTypeenum
from meteoalarm_producer_data.categoryenum import CategoryEnum
from meteoalarm_producer_data.severityenum import SeverityEnum
import datetime


class Test_WeatherWarning(unittest.TestCase):
    """
    Test case for WeatherWarning
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherWarning.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherWarning for testing
        """
        instance = WeatherWarning(
            identifier='empwpuidlueexflfciah',
            sender='nvaphofuyefzpebuooun',
            sent=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            msg_type=MsgTypeenum.Alert,
            scope=ScopeEnum.Public,
            country='bqnrefuxygbnddguhcca',
            event='uzuxztrclmsffwvolxzb',
            category=CategoryEnum.Met,
            severity=SeverityEnum.Extreme,
            urgency=UrgencyEnum.Immediate,
            certainty=CertaintyEnum.Observed,
            headline='vzlpqgtktpupyszmcspd',
            description='ihzjsrfnzyhyxwfhqdtg',
            instruction='masbepziwacqddljrymj',
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            web='ddnrodhsnpnjzwdisgev',
            contact='dsupanqlchjgjhestoze',
            awareness_level='jgvbvypccznklszgbgfr',
            awareness_type='gffaobdbkkptwyntextb',
            area_desc='ahfwasuttiqziukdffuo',
            geocodes='ckzctznxwekswwhoylbb',
            language='ylfowlvosxhapwewjsku'
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'empwpuidlueexflfciah'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'nvaphofuyefzpebuooun'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = StatusEnum.Actual
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = MsgTypeenum.Alert
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_scope_property(self):
        """
        Test scope property
        """
        test_value = ScopeEnum.Public
        self.instance.scope = test_value
        self.assertEqual(self.instance.scope, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'bqnrefuxygbnddguhcca'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'uzuxztrclmsffwvolxzb'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = CategoryEnum.Met
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.Extreme
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = UrgencyEnum.Immediate
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = CertaintyEnum.Observed
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'vzlpqgtktpupyszmcspd'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'ihzjsrfnzyhyxwfhqdtg'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_instruction_property(self):
        """
        Test instruction property
        """
        test_value = 'masbepziwacqddljrymj'
        self.instance.instruction = test_value
        self.assertEqual(self.instance.instruction, test_value)
    
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
    
    def test_web_property(self):
        """
        Test web property
        """
        test_value = 'ddnrodhsnpnjzwdisgev'
        self.instance.web = test_value
        self.assertEqual(self.instance.web, test_value)
    
    def test_contact_property(self):
        """
        Test contact property
        """
        test_value = 'dsupanqlchjgjhestoze'
        self.instance.contact = test_value
        self.assertEqual(self.instance.contact, test_value)
    
    def test_awareness_level_property(self):
        """
        Test awareness_level property
        """
        test_value = 'jgvbvypccznklszgbgfr'
        self.instance.awareness_level = test_value
        self.assertEqual(self.instance.awareness_level, test_value)
    
    def test_awareness_type_property(self):
        """
        Test awareness_type property
        """
        test_value = 'gffaobdbkkptwyntextb'
        self.instance.awareness_type = test_value
        self.assertEqual(self.instance.awareness_type, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'ahfwasuttiqziukdffuo'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_geocodes_property(self):
        """
        Test geocodes property
        """
        test_value = 'ckzctznxwekswwhoylbb'
        self.instance.geocodes = test_value
        self.assertEqual(self.instance.geocodes, test_value)
    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'ylfowlvosxhapwewjsku'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherWarning.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherWarning.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

