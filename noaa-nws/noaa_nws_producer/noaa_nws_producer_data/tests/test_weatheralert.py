"""
Test case for WeatherAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.weatheralert import WeatherAlert
from noaa_nws_producer_data.categoryenum import CategoryEnum
from noaa_nws_producer_data.messagetypeenum import MessageTypeenum
from noaa_nws_producer_data.certaintyenum import CertaintyEnum
from noaa_nws_producer_data.statusenum import StatusEnum
from noaa_nws_producer_data.severityenum import SeverityEnum
from noaa_nws_producer_data.urgencyenum import UrgencyEnum
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
            alert_id='pynwcvvtnmoybhdhikwd',
            area_desc='gnfqejanqhdtibbdrjyb',
            sent=datetime.datetime.now(datetime.timezone.utc),
            effective=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            status=StatusEnum.Actual,
            message_type=MessageTypeenum.Alert,
            category=CategoryEnum.Met,
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            urgency=UrgencyEnum.Immediate,
            event='rgunkesfpugvclpcangv',
            sender_name='zhwpfbhzmtlawimdfrue',
            headline='yskavcczpgugvlkemtjm',
            description='xcdgyumcpvvyhimqmrba'
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'pynwcvvtnmoybhdhikwd'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'gnfqejanqhdtibbdrjyb'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
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
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
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
        test_value = 'rgunkesfpugvclpcangv'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'zhwpfbhzmtlawimdfrue'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'yskavcczpgugvlkemtjm'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'xcdgyumcpvvyhimqmrba'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
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

