"""
Test case for HighwayAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.alerts.highwayalert import HighwayAlert
from wsdot_producer_data.us.wa.wsdot.alerts.eventstatusenum import EventStatusenum
from wsdot_producer_data.us.wa.wsdot.alerts.priorityenum import PriorityEnum


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
            alert_id='ujujjimpusgfbpdxvrbl',
            county='abwgicgjdmvhbsfshjwn',
            region='drbygunjzewopcmxdeps',
            priority=PriorityEnum.Highest,
            event_category='rkstxvzperyuxegzkjwz',
            event_status=EventStatusenum.Open,
            headline_description='ywjnkcuwxchhscdlwsvp',
            extended_description='fogjlmwzhkbuaeguictr',
            start_time='yexlbruyumsuqhlgckwy',
            end_time='xafksvsxkghjasdslvbs',
            last_updated_time='wnazdbiqekleprxfvaqj',
            start_description='ktxefzjswyzzbayfkbiw',
            start_direction='juuscchepvkuqvxqbumh',
            start_road_name='cdiudoqszdstmqmmwnbl',
            start_milepost=float(42.76917014704722),
            start_latitude=float(42.43658397520247),
            start_longitude=float(59.690588926140656),
            end_description='vnjeyotusyohscanbwsz',
            end_direction='ksrjtpmxuoinzcdshltv',
            end_road_name='nomqwghmsvzxbuvauznb',
            end_milepost=float(56.954314862736396),
            end_latitude=float(79.54066372832067),
            end_longitude=float(34.87069508165379)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'ujujjimpusgfbpdxvrbl'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'abwgicgjdmvhbsfshjwn'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'drbygunjzewopcmxdeps'
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
        test_value = 'rkstxvzperyuxegzkjwz'
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
        test_value = 'ywjnkcuwxchhscdlwsvp'
        self.instance.headline_description = test_value
        self.assertEqual(self.instance.headline_description, test_value)
    
    def test_extended_description_property(self):
        """
        Test extended_description property
        """
        test_value = 'fogjlmwzhkbuaeguictr'
        self.instance.extended_description = test_value
        self.assertEqual(self.instance.extended_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'yexlbruyumsuqhlgckwy'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'xafksvsxkghjasdslvbs'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_last_updated_time_property(self):
        """
        Test last_updated_time property
        """
        test_value = 'wnazdbiqekleprxfvaqj'
        self.instance.last_updated_time = test_value
        self.assertEqual(self.instance.last_updated_time, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'ktxefzjswyzzbayfkbiw'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'juuscchepvkuqvxqbumh'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'cdiudoqszdstmqmmwnbl'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(42.76917014704722)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(42.43658397520247)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(59.690588926140656)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'vnjeyotusyohscanbwsz'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'ksrjtpmxuoinzcdshltv'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'nomqwghmsvzxbuvauznb'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(56.954314862736396)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(79.54066372832067)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(34.87069508165379)
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

