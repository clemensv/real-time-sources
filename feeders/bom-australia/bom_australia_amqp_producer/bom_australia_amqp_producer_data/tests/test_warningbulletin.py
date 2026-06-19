"""
Test case for WarningBulletin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bom_australia_amqp_producer_data.warningbulletin import WarningBulletin
import datetime


class Test_WarningBulletin(unittest.TestCase):
    """
    Test case for WarningBulletin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WarningBulletin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WarningBulletin for testing
        """
        instance = WarningBulletin(
            warning_id='ifiyxoandzrwjyqrvsha',
            warning_url='frdbcxjajoavezmuerbd',
            feed_url='kvgwttoblrmxewpybxka',
            feed_title='cufrmproyisambijvwhz',
            title='phtcuyeasxcbfidgwvsm',
            published_at=datetime.datetime.now(datetime.timezone.utc),
            issued_local_time_text='lzhnluoxtseoagtxvcky',
            warning_type='iuksijixnbxhqtclxhvv',
            affected_area_text='fgwjxqlthikmiajusphm',
            severity='wtsfcvwwmwkfdyixqzij',
            state='blvfxctoblojdkcpyzpb'
        )
        return instance

    
    def test_warning_id_property(self):
        """
        Test warning_id property
        """
        test_value = 'ifiyxoandzrwjyqrvsha'
        self.instance.warning_id = test_value
        self.assertEqual(self.instance.warning_id, test_value)
    
    def test_warning_url_property(self):
        """
        Test warning_url property
        """
        test_value = 'frdbcxjajoavezmuerbd'
        self.instance.warning_url = test_value
        self.assertEqual(self.instance.warning_url, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'kvgwttoblrmxewpybxka'
        self.instance.feed_url = test_value
        self.assertEqual(self.instance.feed_url, test_value)
    
    def test_feed_title_property(self):
        """
        Test feed_title property
        """
        test_value = 'cufrmproyisambijvwhz'
        self.instance.feed_title = test_value
        self.assertEqual(self.instance.feed_title, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'phtcuyeasxcbfidgwvsm'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_published_at_property(self):
        """
        Test published_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.published_at = test_value
        self.assertEqual(self.instance.published_at, test_value)
    
    def test_issued_local_time_text_property(self):
        """
        Test issued_local_time_text property
        """
        test_value = 'lzhnluoxtseoagtxvcky'
        self.instance.issued_local_time_text = test_value
        self.assertEqual(self.instance.issued_local_time_text, test_value)
    
    def test_warning_type_property(self):
        """
        Test warning_type property
        """
        test_value = 'iuksijixnbxhqtclxhvv'
        self.instance.warning_type = test_value
        self.assertEqual(self.instance.warning_type, test_value)
    
    def test_affected_area_text_property(self):
        """
        Test affected_area_text property
        """
        test_value = 'fgwjxqlthikmiajusphm'
        self.instance.affected_area_text = test_value
        self.assertEqual(self.instance.affected_area_text, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'wtsfcvwwmwkfdyixqzij'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'blvfxctoblojdkcpyzpb'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WarningBulletin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WarningBulletin.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

