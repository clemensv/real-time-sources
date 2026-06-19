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
            alert_id='abrrbvmihcamclovcliv',
            county='umwdbquuulzkesqszyrc',
            region='bvzxtbgpfijgchvhxkle',
            priority=PriorityEnum.Highest,
            event_category='guljjcgrlttxjfxzopfh',
            event_status=EventStatusenum.Open,
            headline_description='eekkvgdrdgrfkhdeulwx',
            extended_description='ppzvoidbccvnurosovci',
            start_time='gauconscwgadnfdbpvur',
            end_time='umilntfgpbqjdmkooeqb',
            last_updated_time='lfgakqmzrujtynubvomk',
            start_description='ijsuctdvnrzqmnwnlfnr',
            start_direction='okiholshbnkzkolvjuql',
            start_road_name='smmgrpoglxqpivbjrdow',
            start_milepost=float(83.80545318474837),
            start_latitude=float(12.3671607050022),
            start_longitude=float(53.33721261426413),
            end_description='ylxpqyqhmuqhpmseacsj',
            end_direction='pppdxuqqjobflaiofmbz',
            end_road_name='wuyjfbiwpsgkzlrffcve',
            end_milepost=float(26.61525930718446),
            end_latitude=float(11.533427008206221),
            end_longitude=float(57.13669950651682)
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'abrrbvmihcamclovcliv'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_county_property(self):
        """
        Test county property
        """
        test_value = 'umwdbquuulzkesqszyrc'
        self.instance.county = test_value
        self.assertEqual(self.instance.county, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'bvzxtbgpfijgchvhxkle'
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
        test_value = 'guljjcgrlttxjfxzopfh'
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
        test_value = 'eekkvgdrdgrfkhdeulwx'
        self.instance.headline_description = test_value
        self.assertEqual(self.instance.headline_description, test_value)
    
    def test_extended_description_property(self):
        """
        Test extended_description property
        """
        test_value = 'ppzvoidbccvnurosovci'
        self.instance.extended_description = test_value
        self.assertEqual(self.instance.extended_description, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'gauconscwgadnfdbpvur'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_end_time_property(self):
        """
        Test end_time property
        """
        test_value = 'umilntfgpbqjdmkooeqb'
        self.instance.end_time = test_value
        self.assertEqual(self.instance.end_time, test_value)
    
    def test_last_updated_time_property(self):
        """
        Test last_updated_time property
        """
        test_value = 'lfgakqmzrujtynubvomk'
        self.instance.last_updated_time = test_value
        self.assertEqual(self.instance.last_updated_time, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'ijsuctdvnrzqmnwnlfnr'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'okiholshbnkzkolvjuql'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'smmgrpoglxqpivbjrdow'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(83.80545318474837)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(12.3671607050022)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(53.33721261426413)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'ylxpqyqhmuqhpmseacsj'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'pppdxuqqjobflaiofmbz'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'wuyjfbiwpsgkzlrffcve'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(26.61525930718446)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(11.533427008206221)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(57.13669950651682)
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

