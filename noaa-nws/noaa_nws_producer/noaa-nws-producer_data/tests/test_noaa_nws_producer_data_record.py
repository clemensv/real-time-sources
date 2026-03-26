"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            alert_id='ymowegpgkpscwctsqcrq',
            area_desc='rolmmryjqwjynqljsllo',
            sent='vtslawcapcgbbesxrtvw',
            effective='glrtlxhcjwugatssslfd',
            expires='gbapthwbszvncarrllpn',
            status='rnaocpitakswoqngzavn',
            message_type='xvyuqoqcyizswwsiehja',
            category='hzsobdzqlzwqerqwxvtv',
            severity='lskbglakyghhhabfqibx',
            certainty='mxgzxfzbqlhpbgoafxgo',
            urgency='gmwvpisjjvvshlgzxtoc',
            event='huznwydpvxwxdmwcckop',
            sender_name='fhdxhyezkecwpsdbuyjt',
            headline='mcshziswwkpqnvqkbhfr',
            description='atfmrhonorakjtwmddgk'
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'ymowegpgkpscwctsqcrq'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'rolmmryjqwjynqljsllo'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = 'vtslawcapcgbbesxrtvw'
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_effective_property(self):
        """
        Test effective property
        """
        test_value = 'glrtlxhcjwugatssslfd'
        self.instance.effective = test_value
        self.assertEqual(self.instance.effective, test_value)
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = 'gbapthwbszvncarrllpn'
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'rnaocpitakswoqngzavn'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_message_type_property(self):
        """
        Test message_type property
        """
        test_value = 'xvyuqoqcyizswwsiehja'
        self.instance.message_type = test_value
        self.assertEqual(self.instance.message_type, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'hzsobdzqlzwqerqwxvtv'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'lskbglakyghhhabfqibx'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = 'mxgzxfzbqlhpbgoafxgo'
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = 'gmwvpisjjvvshlgzxtoc'
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'huznwydpvxwxdmwcckop'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'fhdxhyezkecwpsdbuyjt'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'mcshziswwkpqnvqkbhfr'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'atfmrhonorakjtwmddgk'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
