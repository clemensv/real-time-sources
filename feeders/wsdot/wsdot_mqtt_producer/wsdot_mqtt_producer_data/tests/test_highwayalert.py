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
            alert_id='jfgysunlshjdbbhywgih',
            county='ygkwclekdinnusnypdly',
            region='ntaysiiulsifnatgaiuf',
            priority=PriorityEnum.Highest,
            event_category='znvmsotoeattoafxgkmv',
            event_status=EventStatusenum.Open,
            headline_description='kseeoxdtjjxmhaxzwdvy',
            extended_description='vabewtgtdepsvcrnlgwl',
            start_time='itzqbjehmdhxcdfwcnbd',
            end_time='xlvxxjmdcfbnrymwieux',
            last_updated_time='aehomwhhhqadhirhowfu',
            start_description='hdkaxyuwpyicervaxtms',
            start_direction='sccnslqfsjjhravhttpv',
            start_road_name='fcluwmhktzwqydxnccvb',
            start_milepost=float(80.04964961326758),
            start_latitude=float(57.697584546359224),
            start_longitude=float(21.005104432593825),
            end_description='cdiaxeqsghmfaodeiyli',
            end_direction='jkfqxcowypfltgvjomdx',
            end_road_name='mcnshhlwwnovovtvfzrh',
            end_milepost=float(52.43843903189577),
            end_latitude=float(26.28653593574468),
            end_longitude=float(38.77080666848284)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'jfgysunlshjdbbhywgih'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'ygkwclekdinnusnypdly'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ntaysiiulsifnatgaiuf'
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
        test_value = 'znvmsotoeattoafxgkmv'
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
        test_value = 'kseeoxdtjjxmhaxzwdvy'
        self.instance.headline_description = test_value
        self.assertEqual(self.instance.headline_description, test_value)
    
    def test_extended_description_property(self):
        """
        Test extended_description property
        """
        test_value = 'vabewtgtdepsvcrnlgwl'
        self.instance.extended_description = test_value
        self.assertEqual(self.instance.extended_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'itzqbjehmdhxcdfwcnbd'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'xlvxxjmdcfbnrymwieux'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_last_updated_time_property(self):
        """
        Test last_updated_time property
        """
        test_value = 'aehomwhhhqadhirhowfu'
        self.instance.last_updated_time = test_value
        self.assertEqual(self.instance.last_updated_time, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'hdkaxyuwpyicervaxtms'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'sccnslqfsjjhravhttpv'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'fcluwmhktzwqydxnccvb'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(80.04964961326758)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(57.697584546359224)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(21.005104432593825)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'cdiaxeqsghmfaodeiyli'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'jkfqxcowypfltgvjomdx'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'mcnshhlwwnovovtvfzrh'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(52.43843903189577)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(26.28653593574468)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(38.77080666848284)
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

