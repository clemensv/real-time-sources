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
            change_type='etszfwfpjecxalvkejsk',
            element_type='udqmikpptqspjubfcrkg',
            element_id=int(38),
            geohash5='trihytyiamzwysoboodo',
            version=int(88),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            changeset_id=int(68),
            user_name='iupminodrqjpbarcdsyh',
            user_id=int(38),
            latitude=float(79.79775288294415),
            longitude=float(95.91527798692695),
            tags='yslnqwxggghfcvyswion',
            sequence_number=int(57)
        )
        return instance

    
    def test_change_type_property(self):
        """
        Test change_type property
        """
        test_value = 'etszfwfpjecxalvkejsk'
        self.instance.change_type = test_value
        self.assertEqual(self.instance.change_type, test_value)
    
    def test_element_type_property(self):
        """
        Test element_type property
        """
        test_value = 'udqmikpptqspjubfcrkg'
        self.instance.element_type = test_value
        self.assertEqual(self.instance.element_type, test_value)
    
    def test_element_id_property(self):
        """
        Test element_id property
        """
        test_value = int(38)
        self.instance.element_id = test_value
        self.assertEqual(self.instance.element_id, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'trihytyiamzwysoboodo'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(88)
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
        test_value = int(68)
        self.instance.changeset_id = test_value
        self.assertEqual(self.instance.changeset_id, test_value)
    
    def test_user_name_property(self):
        """
        Test user_name property
        """
        test_value = 'iupminodrqjpbarcdsyh'
        self.instance.user_name = test_value
        self.assertEqual(self.instance.user_name, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(38)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(79.79775288294415)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(95.91527798692695)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_tags_property(self):
        """
        Test tags property
        """
        test_value = 'yslnqwxggghfcvyswion'
        self.instance.tags = test_value
        self.assertEqual(self.instance.tags, test_value)
    
    def test_sequence_number_property(self):
        """
        Test sequence_number property
        """
        test_value = int(57)
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

