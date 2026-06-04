"""
Test case for MapChange
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wikimedia_osm_diffs_producer_data.mapchange import MapChange
import datetime


class Test_MapChange(unittest.TestCase):
    """
    Test case for MapChange
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MapChange.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MapChange for testing
        """
        instance = MapChange(
            change_type='qswzolxmjhjqnbzbenar',
            element_type='rbeeeimljytznmvmebhb',
            element_id=int(86),
            geohash5='yothjyzupjzyhezfegqy',
            version=int(42),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            changeset_id=int(93),
            user_name='qrfxzmgcbmecfhgybljy',
            user_id=int(74),
            latitude=float(59.77712121711628),
            longitude=float(39.76279761215301),
            tags='lrdgqunkxhqhqxvvgxeu',
            sequence_number=int(97)
        )
        return instance

    
    def test_change_type_property(self):
        """
        Test change_type property
        """
        test_value = 'qswzolxmjhjqnbzbenar'
        self.instance.change_type = test_value
        self.assertEqual(self.instance.change_type, test_value)
    
    def test_element_type_property(self):
        """
        Test element_type property
        """
        test_value = 'rbeeeimljytznmvmebhb'
        self.instance.element_type = test_value
        self.assertEqual(self.instance.element_type, test_value)
    
    def test_element_id_property(self):
        """
        Test element_id property
        """
        test_value = int(86)
        self.instance.element_id = test_value
        self.assertEqual(self.instance.element_id, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'yothjyzupjzyhezfegqy'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(42)
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_changeset_id_property(self):
        """
        Test changeset_id property
        """
        test_value = int(93)
        self.instance.changeset_id = test_value
        self.assertEqual(self.instance.changeset_id, test_value)
    
    def test_user_name_property(self):
        """
        Test user_name property
        """
        test_value = 'qrfxzmgcbmecfhgybljy'
        self.instance.user_name = test_value
        self.assertEqual(self.instance.user_name, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(74)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.77712121711628)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(39.76279761215301)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_tags_property(self):
        """
        Test tags property
        """
        test_value = 'lrdgqunkxhqhqxvvgxeu'
        self.instance.tags = test_value
        self.assertEqual(self.instance.tags, test_value)
    
    def test_sequence_number_property(self):
        """
        Test sequence_number property
        """
        test_value = int(97)
        self.instance.sequence_number = test_value
        self.assertEqual(self.instance.sequence_number, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MapChange.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MapChange.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

