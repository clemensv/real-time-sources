"""
Test case for DisasterAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gdacs_amqp_producer_data.disasteralert import DisasterAlert
from gdacs_amqp_producer_data.alertcolorenum import AlertColorenum
from gdacs_amqp_producer_data.alertlevelenum import AlertLevelenum
from gdacs_amqp_producer_data.eventtypeenum import EventTypeenum
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
            event_id='eaplmxnxyhlgedbbsgmd',
            episode_id='sktxjhfzdqbypneypnpw',
            alert_level=AlertLevelenum.Green,
            alert_score=float(62.81985910687151),
            episode_alert_level='qcwevpsrkywckyzqotdi',
            episode_alert_score=float(30.918252039817627),
            event_name='trhvwuhqrsysslxjbaru',
            severity_value=float(36.89808259596108),
            severity_unit='ybazgjnplxwbuugteaor',
            severity_text='pbfsbgnjekrpyusrrhhm',
            country='unegmfmwnlfjqbyfiqtc',
            iso3='wkwulhcapvlvzoatxiie',
            latitude=float(74.86681563589718),
            longitude=float(76.78090620778627),
            from_date=datetime.datetime.now(datetime.timezone.utc),
            to_date=datetime.datetime.now(datetime.timezone.utc),
            population_value=float(5.135512396939202),
            population_unit='rhiilekrttczbcapdglt',
            vulnerability=float(11.44534919170509),
            bbox_min_lon=float(73.37074507028105),
            bbox_max_lon=float(58.55488462119482),
            bbox_min_lat=float(31.853944786600717),
            bbox_max_lat=float(72.23439149698913),
            is_current=False,
            version=int(1),
            description='zvluhgcbfopaajshmdqw',
            link='bfamhqedjjfvfewuwptc',
            pub_date=datetime.datetime.now(datetime.timezone.utc),
            alert_color=AlertColorenum.green
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
        test_value = 'eaplmxnxyhlgedbbsgmd'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_episode_id_property(self):
        """
        Test episode_id property
        """
        test_value = 'sktxjhfzdqbypneypnpw'
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
        test_value = float(62.81985910687151)
        self.instance.alert_score = test_value
        self.assertEqual(self.instance.alert_score, test_value)
    
    def test_episode_alert_level_property(self):
        """
        Test episode_alert_level property
        """
        test_value = 'qcwevpsrkywckyzqotdi'
        self.instance.episode_alert_level = test_value
        self.assertEqual(self.instance.episode_alert_level, test_value)
    
    def test_episode_alert_score_property(self):
        """
        Test episode_alert_score property
        """
        test_value = float(30.918252039817627)
        self.instance.episode_alert_score = test_value
        self.assertEqual(self.instance.episode_alert_score, test_value)
    
    def test_event_name_property(self):
        """
        Test event_name property
        """
        test_value = 'trhvwuhqrsysslxjbaru'
        self.instance.event_name = test_value
        self.assertEqual(self.instance.event_name, test_value)
    
    def test_severity_value_property(self):
        """
        Test severity_value property
        """
        test_value = float(36.89808259596108)
        self.instance.severity_value = test_value
        self.assertEqual(self.instance.severity_value, test_value)
    
    def test_severity_unit_property(self):
        """
        Test severity_unit property
        """
        test_value = 'ybazgjnplxwbuugteaor'
        self.instance.severity_unit = test_value
        self.assertEqual(self.instance.severity_unit, test_value)
    
    def test_severity_text_property(self):
        """
        Test severity_text property
        """
        test_value = 'pbfsbgnjekrpyusrrhhm'
        self.instance.severity_text = test_value
        self.assertEqual(self.instance.severity_text, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'unegmfmwnlfjqbyfiqtc'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_iso3_property(self):
        """
        Test iso3 property
        """
        test_value = 'wkwulhcapvlvzoatxiie'
        self.instance.iso3 = test_value
        self.assertEqual(self.instance.iso3, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(74.86681563589718)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(76.78090620778627)
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
        test_value = float(5.135512396939202)
        self.instance.population_value = test_value
        self.assertEqual(self.instance.population_value, test_value)
    
    def test_population_unit_property(self):
        """
        Test population_unit property
        """
        test_value = 'rhiilekrttczbcapdglt'
        self.instance.population_unit = test_value
        self.assertEqual(self.instance.population_unit, test_value)
    
    def test_vulnerability_property(self):
        """
        Test vulnerability property
        """
        test_value = float(11.44534919170509)
        self.instance.vulnerability = test_value
        self.assertEqual(self.instance.vulnerability, test_value)
    
    def test_bbox_min_lon_property(self):
        """
        Test bbox_min_lon property
        """
        test_value = float(73.37074507028105)
        self.instance.bbox_min_lon = test_value
        self.assertEqual(self.instance.bbox_min_lon, test_value)
    
    def test_bbox_max_lon_property(self):
        """
        Test bbox_max_lon property
        """
        test_value = float(58.55488462119482)
        self.instance.bbox_max_lon = test_value
        self.assertEqual(self.instance.bbox_max_lon, test_value)
    
    def test_bbox_min_lat_property(self):
        """
        Test bbox_min_lat property
        """
        test_value = float(31.853944786600717)
        self.instance.bbox_min_lat = test_value
        self.assertEqual(self.instance.bbox_min_lat, test_value)
    
    def test_bbox_max_lat_property(self):
        """
        Test bbox_max_lat property
        """
        test_value = float(72.23439149698913)
        self.instance.bbox_max_lat = test_value
        self.assertEqual(self.instance.bbox_max_lat, test_value)
    
    def test_is_current_property(self):
        """
        Test is_current property
        """
        test_value = False
        self.instance.is_current = test_value
        self.assertEqual(self.instance.is_current, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(1)
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'zvluhgcbfopaajshmdqw'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_link_property(self):
        """
        Test link property
        """
        test_value = 'bfamhqedjjfvfewuwptc'
        self.instance.link = test_value
        self.assertEqual(self.instance.link, test_value)
    
    def test_pub_date_property(self):
        """
        Test pub_date property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.pub_date = test_value
        self.assertEqual(self.instance.pub_date, test_value)
    
    def test_alert_color_property(self):
        """
        Test alert_color property
        """
        test_value = AlertColorenum.green
        self.instance.alert_color = test_value
        self.assertEqual(self.instance.alert_color, test_value)
    
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

