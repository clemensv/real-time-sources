"""
Test case for WarningBulletin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bom_australia_producer_data.warningbulletin import WarningBulletin
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
            warning_id='gainratfwvralfgqzvld',
            warning_url='csxxaujzmtdicobdgtem',
            feed_url='hqzazpvkxjgovrlqyngl',
            feed_title='towixfkewbioofleskgm',
            title='sotxuayuaclsbrvvbpkm',
            published_at=datetime.datetime.now(datetime.timezone.utc),
            issued_local_time_text='qyovmhuhqtqikummtxei',
            warning_type='fvxkypoqzlcclwziejos',
            affected_area_text='kpfmndaqvwvipaxcrijx',
            severity='ijtypuwysitubsgaatsn',
            state='orkyexcvabnmfnalrovp'
        )
        return instance

    
    def test_warning_id_property(self):
        """
        Test warning_id property
        """
        test_value = 'gainratfwvralfgqzvld'
        self.instance.warning_id = test_value
        self.assertEqual(self.instance.warning_id, test_value)
    
    def test_warning_url_property(self):
        """
        Test warning_url property
        """
        test_value = 'csxxaujzmtdicobdgtem'
        self.instance.warning_url = test_value
        self.assertEqual(self.instance.warning_url, test_value)
    
    def test_feed_url_property(self):
        """
        Test feed_url property
        """
        test_value = 'hqzazpvkxjgovrlqyngl'
        self.instance.feed_url = test_value
        self.assertEqual(self.instance.feed_url, test_value)
    
    def test_feed_title_property(self):
        """
        Test feed_title property
        """
        test_value = 'towixfkewbioofleskgm'
        self.instance.feed_title = test_value
        self.assertEqual(self.instance.feed_title, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'sotxuayuaclsbrvvbpkm'
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
        test_value = 'qyovmhuhqtqikummtxei'
        self.instance.issued_local_time_text = test_value
        self.assertEqual(self.instance.issued_local_time_text, test_value)
    
    def test_warning_type_property(self):
        """
        Test warning_type property
        """
        test_value = 'fvxkypoqzlcclwziejos'
        self.instance.warning_type = test_value
        self.assertEqual(self.instance.warning_type, test_value)
    
    def test_affected_area_text_property(self):
        """
        Test affected_area_text property
        """
        test_value = 'kpfmndaqvwvipaxcrijx'
        self.instance.affected_area_text = test_value
        self.assertEqual(self.instance.affected_area_text, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ijtypuwysitubsgaatsn'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'orkyexcvabnmfnalrovp'
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

