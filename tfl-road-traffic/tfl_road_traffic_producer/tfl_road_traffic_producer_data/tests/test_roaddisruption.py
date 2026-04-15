"""
Test case for RoadDisruption
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from tfl_road_traffic_producer_data.roaddisruption import RoadDisruption
import datetime


class Test_RoadDisruption(unittest.TestCase):
    """
    Test case for RoadDisruption
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadDisruption.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadDisruption for testing
        """
        instance = RoadDisruption(
            disruption_id='ubptilvdtgtqtgjixxez',
            category='xeiazrmaujoascpufymb',
            sub_category='knliymarjfpnmhjulpfq',
            severity='ubnsxqbsefzfbcgxonxf',
            ordinal=int(12),
            url='qqfhgpibdcgseskqeyve',
            point='bfetvjepjzaxxgoggwsp',
            comments='casbnqknuztastiwmlia',
            current_update='opdxadtpkwwajdvfrtss',
            current_update_datetime=datetime.datetime.now(datetime.timezone.utc),
            corridor_ids={"test": "test"},
            start_datetime=datetime.datetime.now(datetime.timezone.utc),
            end_datetime=datetime.datetime.now(datetime.timezone.utc),
            last_modified_time=datetime.datetime.now(datetime.timezone.utc),
            level_of_interest='vhkfhldhmqjryratsget',
            location='fudfxxmfexskcjwgrwcc',
            is_provisional=True,
            has_closures=False,
            streets={"test": "test"},
            geography='gqyqckeevvnndpqovrun',
            geometry='tffzzaypmxwoebyivhlr',
            status='tznmfnquopjknkjcqzdj',
            is_active=True
        )
        return instance

    
    def test_disruption_id_property(self):
        """
        Test disruption_id property
        """
        test_value = 'ubptilvdtgtqtgjixxez'
        self.instance.disruption_id = test_value
        self.assertEqual(self.instance.disruption_id, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'xeiazrmaujoascpufymb'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_sub_category_property(self):
        """
        Test sub_category property
        """
        test_value = 'knliymarjfpnmhjulpfq'
        self.instance.sub_category = test_value
        self.assertEqual(self.instance.sub_category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ubnsxqbsefzfbcgxonxf'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_ordinal_property(self):
        """
        Test ordinal property
        """
        test_value = int(12)
        self.instance.ordinal = test_value
        self.assertEqual(self.instance.ordinal, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'qqfhgpibdcgseskqeyve'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'bfetvjepjzaxxgoggwsp'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_comments_property(self):
        """
        Test comments property
        """
        test_value = 'casbnqknuztastiwmlia'
        self.instance.comments = test_value
        self.assertEqual(self.instance.comments, test_value)
    
    def test_current_update_property(self):
        """
        Test current_update property
        """
        test_value = 'opdxadtpkwwajdvfrtss'
        self.instance.current_update = test_value
        self.assertEqual(self.instance.current_update, test_value)
    
    def test_current_update_datetime_property(self):
        """
        Test current_update_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.current_update_datetime = test_value
        self.assertEqual(self.instance.current_update_datetime, test_value)
    
    def test_corridor_ids_property(self):
        """
        Test corridor_ids property
        """
        test_value = {"test": "test"}
        self.instance.corridor_ids = test_value
        self.assertEqual(self.instance.corridor_ids, test_value)
    
    def test_start_datetime_property(self):
        """
        Test start_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_datetime = test_value
        self.assertEqual(self.instance.start_datetime, test_value)
    
    def test_end_datetime_property(self):
        """
        Test end_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.end_datetime = test_value
        self.assertEqual(self.instance.end_datetime, test_value)
    
    def test_last_modified_time_property(self):
        """
        Test last_modified_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.last_modified_time = test_value
        self.assertEqual(self.instance.last_modified_time, test_value)
    
    def test_level_of_interest_property(self):
        """
        Test level_of_interest property
        """
        test_value = 'vhkfhldhmqjryratsget'
        self.instance.level_of_interest = test_value
        self.assertEqual(self.instance.level_of_interest, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'fudfxxmfexskcjwgrwcc'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_is_provisional_property(self):
        """
        Test is_provisional property
        """
        test_value = True
        self.instance.is_provisional = test_value
        self.assertEqual(self.instance.is_provisional, test_value)
    
    def test_has_closures_property(self):
        """
        Test has_closures property
        """
        test_value = False
        self.instance.has_closures = test_value
        self.assertEqual(self.instance.has_closures, test_value)
    
    def test_streets_property(self):
        """
        Test streets property
        """
        test_value = {"test": "test"}
        self.instance.streets = test_value
        self.assertEqual(self.instance.streets, test_value)
    
    def test_geography_property(self):
        """
        Test geography property
        """
        test_value = 'gqyqckeevvnndpqovrun'
        self.instance.geography = test_value
        self.assertEqual(self.instance.geography, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = 'tffzzaypmxwoebyivhlr'
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'tznmfnquopjknkjcqzdj'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_is_active_property(self):
        """
        Test is_active property
        """
        test_value = True
        self.instance.is_active = test_value
        self.assertEqual(self.instance.is_active, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadDisruption.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RoadDisruption.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

