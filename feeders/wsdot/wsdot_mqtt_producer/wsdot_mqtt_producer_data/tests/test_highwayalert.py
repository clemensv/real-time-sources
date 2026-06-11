"""
Test case for HighwayAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.highwayalert import HighwayAlert
from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.priorityenum import PriorityEnum
from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.eventstatusenum import EventStatusenum


class Test_HighwayAlert(unittest.TestCase):
    """
    Test case for HighwayAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_HighwayAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of HighwayAlert for testing
        """
        instance = HighwayAlert(
            alert_id='wxuyqjylgbdbopltuyct',
            county='avrfqnyhqqadethyrlef',
            region='rtawcawronljoujlfmig',
            priority=PriorityEnum.Highest,
            event_category='thwkrhsjslqxrkjlngom',
            event_status=EventStatusenum.Open,
            headline_description='pujkuzpsdeovsmlszqhq',
            extended_description='xecxkrhjfsluzdinoppw',
            start_time='eqbuaaepgbiejimibbmt',
            end_time='atsoskgmrmpqmlogpngs',
            last_updated_time='yoznftypbppbqyojmoss',
            start_description='lglstteibxrgykojksbc',
            start_direction='vkqemytyxysqxguczuzc',
            start_road_name='ndwiitcmtozrunstyvpj',
            start_milepost=float(87.25953991183297),
            start_latitude=float(42.01886366886094),
            start_longitude=float(31.41092549591408),
            end_description='heuxqetuupzbuyixkcwp',
            end_direction='aurgwfdufbpthruovzpt',
            end_road_name='euusywbvzekbzpgyadrr',
            end_milepost=float(65.34404757466649),
            end_latitude=float(50.56659353524785),
            end_longitude=float(55.80440474361418)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'wxuyqjylgbdbopltuyct'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'avrfqnyhqqadethyrlef'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'rtawcawronljoujlfmig'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_priority_property(self):
        """
        Test priority property
        """
        test_value = PriorityEnum.Highest
        self.instance.priority = test_value
        self.assertEqual(self.instance.priority, test_value)
    
    def test_event_category_property(self):
        """
        Test event_category property
        """
        test_value = 'thwkrhsjslqxrkjlngom'
        self.instance.event_category = test_value
        self.assertEqual(self.instance.event_category, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = EventStatusenum.Open
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_headline_description_property(self):
        """
        Test headline_description property
        """
        test_value = 'pujkuzpsdeovsmlszqhq'
        self.instance.headline_description = test_value
        self.assertEqual(self.instance.headline_description, test_value)
    
    def test_extended_description_property(self):
        """
        Test extended_description property
        """
        test_value = 'xecxkrhjfsluzdinoppw'
        self.instance.extended_description = test_value
        self.assertEqual(self.instance.extended_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'eqbuaaepgbiejimibbmt'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'atsoskgmrmpqmlogpngs'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_last_updated_time_property(self):
        """
        Test last_updated_time property
        """
        test_value = 'yoznftypbppbqyojmoss'
        self.instance.last_updated_time = test_value
        self.assertEqual(self.instance.last_updated_time, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'lglstteibxrgykojksbc'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'vkqemytyxysqxguczuzc'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'ndwiitcmtozrunstyvpj'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(87.25953991183297)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(42.01886366886094)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(31.41092549591408)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'heuxqetuupzbuyixkcwp'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'aurgwfdufbpthruovzpt'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'euusywbvzekbzpgyadrr'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(65.34404757466649)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(50.56659353524785)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(55.80440474361418)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = HighwayAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = HighwayAlert.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

