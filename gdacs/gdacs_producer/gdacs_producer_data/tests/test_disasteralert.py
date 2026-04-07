"""
Test case for DisasterAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gdacs_producer_data.disasteralert import DisasterAlert
from gdacs_producer_data.eventtypeenum import EventTypeenum
from gdacs_producer_data.alertlevelenum import AlertLevelenum
import datetime


class Test_DisasterAlert(unittest.TestCase):
    """
    Test case for DisasterAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DisasterAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DisasterAlert for testing
        """
        instance = DisasterAlert(
            event_type=EventTypeenum.EQ,
            event_id='bhsbltkzvkchjtmajmkk',
            episode_id='geulgkhgmtdtxzkffbar',
            alert_level=AlertLevelenum.Green,
            alert_score=float(27.83954627090922),
            episode_alert_level='ilfesmbqeezuelgczvdf',
            episode_alert_score=float(99.13918693817008),
            event_name='yrqlwyawetczxtdinonh',
            severity_value=float(75.97768906998337),
            severity_unit='zeqscrstmohzijsbdtkc',
            severity_text='jktxoqkfhsfinktzylax',
            country='tyehfdvljuohcbfdnhqv',
            iso3='jzttmkjotpzxlalschro',
            latitude=float(1.5258740707473017),
            longitude=float(44.52284495066006),
            from_date=datetime.datetime.now(datetime.timezone.utc),
            to_date=datetime.datetime.now(datetime.timezone.utc),
            population_value=float(56.46441849228597),
            population_unit='syxzuieearwyfhglqowu',
            vulnerability=float(0.6035017236298179),
            bbox_min_lon=float(61.729340334635964),
            bbox_max_lon=float(8.834007927393072),
            bbox_min_lat=float(27.921532884725686),
            bbox_max_lat=float(92.21742038533569),
            is_current=True,
            version=int(64),
            description='gtelxbdjyzfphogawfgk',
            link='vztjsjuafgwzfkcplhlr',
            pub_date=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = EventTypeenum.EQ
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'bhsbltkzvkchjtmajmkk'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_episode_id_property(self):
        """
        Test episode_id property
        """
        test_value = 'geulgkhgmtdtxzkffbar'
        self.instance.episode_id = test_value
        self.assertEqual(self.instance.episode_id, test_value)
    
    def test_alert_level_property(self):
        """
        Test alert_level property
        """
        test_value = AlertLevelenum.Green
        self.instance.alert_level = test_value
        self.assertEqual(self.instance.alert_level, test_value)
    
    def test_alert_score_property(self):
        """
        Test alert_score property
        """
        test_value = float(27.83954627090922)
        self.instance.alert_score = test_value
        self.assertEqual(self.instance.alert_score, test_value)
    
    def test_episode_alert_level_property(self):
        """
        Test episode_alert_level property
        """
        test_value = 'ilfesmbqeezuelgczvdf'
        self.instance.episode_alert_level = test_value
        self.assertEqual(self.instance.episode_alert_level, test_value)
    
    def test_episode_alert_score_property(self):
        """
        Test episode_alert_score property
        """
        test_value = float(99.13918693817008)
        self.instance.episode_alert_score = test_value
        self.assertEqual(self.instance.episode_alert_score, test_value)
    
    def test_event_name_property(self):
        """
        Test event_name property
        """
        test_value = 'yrqlwyawetczxtdinonh'
        self.instance.event_name = test_value
        self.assertEqual(self.instance.event_name, test_value)
    
    def test_severity_value_property(self):
        """
        Test severity_value property
        """
        test_value = float(75.97768906998337)
        self.instance.severity_value = test_value
        self.assertEqual(self.instance.severity_value, test_value)
    
    def test_severity_unit_property(self):
        """
        Test severity_unit property
        """
        test_value = 'zeqscrstmohzijsbdtkc'
        self.instance.severity_unit = test_value
        self.assertEqual(self.instance.severity_unit, test_value)
    
    def test_severity_text_property(self):
        """
        Test severity_text property
        """
        test_value = 'jktxoqkfhsfinktzylax'
        self.instance.severity_text = test_value
        self.assertEqual(self.instance.severity_text, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'tyehfdvljuohcbfdnhqv'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_iso3_property(self):
        """
        Test iso3 property
        """
        test_value = 'jzttmkjotpzxlalschro'
        self.instance.iso3 = test_value
        self.assertEqual(self.instance.iso3, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(1.5258740707473017)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(44.52284495066006)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_from_date_property(self):
        """
        Test from_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.from_date = test_value
        self.assertEqual(self.instance.from_date, test_value)
    
    def test_to_date_property(self):
        """
        Test to_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.to_date = test_value
        self.assertEqual(self.instance.to_date, test_value)
    
    def test_population_value_property(self):
        """
        Test population_value property
        """
        test_value = float(56.46441849228597)
        self.instance.population_value = test_value
        self.assertEqual(self.instance.population_value, test_value)
    
    def test_population_unit_property(self):
        """
        Test population_unit property
        """
        test_value = 'syxzuieearwyfhglqowu'
        self.instance.population_unit = test_value
        self.assertEqual(self.instance.population_unit, test_value)
    
    def test_vulnerability_property(self):
        """
        Test vulnerability property
        """
        test_value = float(0.6035017236298179)
        self.instance.vulnerability = test_value
        self.assertEqual(self.instance.vulnerability, test_value)
    
    def test_bbox_min_lon_property(self):
        """
        Test bbox_min_lon property
        """
        test_value = float(61.729340334635964)
        self.instance.bbox_min_lon = test_value
        self.assertEqual(self.instance.bbox_min_lon, test_value)
    
    def test_bbox_max_lon_property(self):
        """
        Test bbox_max_lon property
        """
        test_value = float(8.834007927393072)
        self.instance.bbox_max_lon = test_value
        self.assertEqual(self.instance.bbox_max_lon, test_value)
    
    def test_bbox_min_lat_property(self):
        """
        Test bbox_min_lat property
        """
        test_value = float(27.921532884725686)
        self.instance.bbox_min_lat = test_value
        self.assertEqual(self.instance.bbox_min_lat, test_value)
    
    def test_bbox_max_lat_property(self):
        """
        Test bbox_max_lat property
        """
        test_value = float(92.21742038533569)
        self.instance.bbox_max_lat = test_value
        self.assertEqual(self.instance.bbox_max_lat, test_value)
    
    def test_is_current_property(self):
        """
        Test is_current property
        """
        test_value = True
        self.instance.is_current = test_value
        self.assertEqual(self.instance.is_current, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(64)
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'gtelxbdjyzfphogawfgk'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_link_property(self):
        """
        Test link property
        """
        test_value = 'vztjsjuafgwzfkcplhlr'
        self.instance.link = test_value
        self.assertEqual(self.instance.link, test_value)
    
    def test_pub_date_property(self):
        """
        Test pub_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pub_date = test_value
        self.assertEqual(self.instance.pub_date, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DisasterAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DisasterAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

