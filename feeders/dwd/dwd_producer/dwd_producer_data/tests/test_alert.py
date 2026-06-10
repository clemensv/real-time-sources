"""
Test case for Alert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_producer_data.alert import Alert


class Test_Alert(unittest.TestCase):
    """
    Test case for Alert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Alert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Alert for testing
        """
        instance = Alert(
            identifier='dkolsweyiflxslbtxgst',
            sender='mbjischshoafwhrfrwnu',
            sent='ldzdgawzhpilltaomqob',
            status='tueajftuptbhbzosaeni',
            msg_type='nkhclpmvmzwobhuxotfy',
            severity='lptrsgpdbgqeasqvmbrt',
            urgency='aomclyosieqygyuipksc',
            certainty='ozsitzzwdkajdphubort',
            event='gtywgiqmtbnhlotosner',
            headline='zwawzxnxqkatuyortqlj',
            description='hupjbgsncjhndvvzpqwa',
            effective='oykclgriyqkpebduckzh',
            onset='derrwoonkyujkvxasonl',
            expires='icwfntbidultfipvghqx',
            area_desc='vqozlqxawvlmlrhoyrug',
            geocodes='kghzycuqjaotwcdyxkdx',
            state='wgbcnfsktsqklnxwsktk'
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'dkolsweyiflxslbtxgst'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'mbjischshoafwhrfrwnu'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = 'ldzdgawzhpilltaomqob'
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'tueajftuptbhbzosaeni'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_msg_type_property(self):
        """
        Test msg_type property
        """
        test_value = 'nkhclpmvmzwobhuxotfy'
        self.instance.msg_type = test_value
        self.assertEqual(self.instance.msg_type, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'lptrsgpdbgqeasqvmbrt'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = 'aomclyosieqygyuipksc'
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = 'ozsitzzwdkajdphubort'
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'gtywgiqmtbnhlotosner'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'zwawzxnxqkatuyortqlj'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'hupjbgsncjhndvvzpqwa'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_effective_property(self):
        """
        Test effective property
        """
        test_value = 'oykclgriyqkpebduckzh'
        self.instance.effective = test_value
        self.assertEqual(self.instance.effective, test_value)
    
    def test_onset_property(self):
        """
        Test onset property
        """
        test_value = 'derrwoonkyujkvxasonl'
        self.instance.onset = test_value
        self.assertEqual(self.instance.onset, test_value)
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = 'icwfntbidultfipvghqx'
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'vqozlqxawvlmlrhoyrug'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_geocodes_property(self):
        """
        Test geocodes property
        """
        test_value = 'kghzycuqjaotwcdyxkdx'
        self.instance.geocodes = test_value
        self.assertEqual(self.instance.geocodes, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'wgbcnfsktsqklnxwsktk'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Alert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Alert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

