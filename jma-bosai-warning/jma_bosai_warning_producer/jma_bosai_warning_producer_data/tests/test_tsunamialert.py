"""
Test case for TsunamiAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_producer_data.tsunamialert import TsunamiAlert
from jma_bosai_warning_producer_data.tsunamiobservation import TsunamiObservation
from jma_bosai_warning_producer_data.infotypeenum import InfoTypeenum
from jma_bosai_warning_producer_data.affectedcoastalregion import AffectedCoastalRegion
import datetime


class Test_TsunamiAlert(unittest.TestCase):
    """
    Test case for TsunamiAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TsunamiAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TsunamiAlert for testing
        """
        instance = TsunamiAlert(
            event_id='wpnkhztnzcgqzcrjtyfu',
            serial=int(67),
            info_type=InfoTypeenum.ISSUED,
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            title_jp='xtmqoilnovayyixespny',
            title_en='mdiinkusgmedjdegfifu',
            bulletin_type='jkrpqayphakjqqkmivcy',
            detail_url='vvzpmsukbwxhitzmlslf',
            affected_coastal_regions=[None, None, None],
            observations=[None, None, None, None, None]
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'wpnkhztnzcgqzcrjtyfu'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_serial_property(self):
        """
        Test serial property
        """
        test_value = int(67)
        self.instance.serial = test_value
        self.assertEqual(self.instance.serial, test_value)
    
    def test_info_type_property(self):
        """
        Test info_type property
        """
        test_value = InfoTypeenum.ISSUED
        self.instance.info_type = test_value
        self.assertEqual(self.instance.info_type, test_value)
    
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
    
    def test_title_jp_property(self):
        """
        Test title_jp property
        """
        test_value = 'xtmqoilnovayyixespny'
        self.instance.title_jp = test_value
        self.assertEqual(self.instance.title_jp, test_value)
    
    def test_title_en_property(self):
        """
        Test title_en property
        """
        test_value = 'mdiinkusgmedjdegfifu'
        self.instance.title_en = test_value
        self.assertEqual(self.instance.title_en, test_value)
    
    def test_bulletin_type_property(self):
        """
        Test bulletin_type property
        """
        test_value = 'jkrpqayphakjqqkmivcy'
        self.instance.bulletin_type = test_value
        self.assertEqual(self.instance.bulletin_type, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'vvzpmsukbwxhitzmlslf'
        self.instance.detail_url = test_value
        self.assertEqual(self.instance.detail_url, test_value)
    
    def test_affected_coastal_regions_property(self):
        """
        Test affected_coastal_regions property
        """
        test_value = [None, None, None]
        self.instance.affected_coastal_regions = test_value
        self.assertEqual(self.instance.affected_coastal_regions, test_value)
    
    def test_observations_property(self):
        """
        Test observations property
        """
        test_value = [None, None, None, None, None]
        self.instance.observations = test_value
        self.assertEqual(self.instance.observations, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TsunamiAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TsunamiAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

