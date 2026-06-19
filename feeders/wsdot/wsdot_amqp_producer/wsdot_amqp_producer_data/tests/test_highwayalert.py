"""
Test case for HighwayAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.alerts.highwayalert import HighwayAlert
from wsdot_amqp_producer_data.us.wa.wsdot.alerts.eventstatusenum import EventStatusenum
from wsdot_amqp_producer_data.us.wa.wsdot.alerts.priorityenum import PriorityEnum


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
            alert_id='yfxbaciykwbviazfliwr',
            county='pfnftrmyvnyhqzxtkiwf',
            region='axldelqdwgjscywyuahg',
            priority=PriorityEnum.Highest,
            event_category='ekvspsgjcsknqcbmwcvy',
            event_status=EventStatusenum.Open,
            headline_description='cfkxbmojgneoryjsdziz',
            extended_description='glzzjkpminzgdicxcmpn',
            start_time='kvbfpcatyeuxisnpqbod',
            end_time='urmhwlcssefmnhlfciuq',
            last_updated_time='seuqzcgfohdbflutzmmi',
            start_description='uthlqmldeubuyfqzsxpj',
            start_direction='fztxdlufoaefwnokqdff',
            start_road_name='hogcwtziiujhphkhaedk',
            start_milepost=float(95.69197795224002),
            start_latitude=float(98.25966332652604),
            start_longitude=float(37.49181383091354),
            end_description='vciqowbogjhwwhjzqmgi',
            end_direction='qcqeqoamtakleodrecch',
            end_road_name='zdngnbwsdvagzvlshark',
            end_milepost=float(86.54692575312548),
            end_latitude=float(65.22834395817078),
            end_longitude=float(89.9492416992018)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'yfxbaciykwbviazfliwr'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'pfnftrmyvnyhqzxtkiwf'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'axldelqdwgjscywyuahg'
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
        test_value = 'ekvspsgjcsknqcbmwcvy'
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
        test_value = 'cfkxbmojgneoryjsdziz'
        self.instance.headline_description = test_value
        self.assertEqual(self.instance.headline_description, test_value)
    
    def test_extended_description_property(self):
        """
        Test extended_description property
        """
        test_value = 'glzzjkpminzgdicxcmpn'
        self.instance.extended_description = test_value
        self.assertEqual(self.instance.extended_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'kvbfpcatyeuxisnpqbod'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'urmhwlcssefmnhlfciuq'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_last_updated_time_property(self):
        """
        Test last_updated_time property
        """
        test_value = 'seuqzcgfohdbflutzmmi'
        self.instance.last_updated_time = test_value
        self.assertEqual(self.instance.last_updated_time, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'uthlqmldeubuyfqzsxpj'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'fztxdlufoaefwnokqdff'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'hogcwtziiujhphkhaedk'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(95.69197795224002)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(98.25966332652604)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(37.49181383091354)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'vciqowbogjhwwhjzqmgi'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'qcqeqoamtakleodrecch'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'zdngnbwsdvagzvlshark'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(86.54692575312548)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(65.22834395817078)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(89.9492416992018)
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

