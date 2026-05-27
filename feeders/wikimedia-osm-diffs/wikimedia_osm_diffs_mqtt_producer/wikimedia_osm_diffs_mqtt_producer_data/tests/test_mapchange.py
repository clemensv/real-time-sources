"""
Test case for MapChange
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wikimedia_osm_diffs_mqtt_producer_data.mapchange import MapChange
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
            change_type='jldrfiemlelogzqfpmqk',
            element_type='osgmzjavluqjlxsqcoct',
            element_id=int(15),
            geohash5='zkwfpmffxrypjsmcejto',
            version=int(2),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            changeset_id=int(0),
            user_name='jclntqgaabznwlcnckkm',
            user_id=int(19),
            latitude=float(35.639272025132904),
            longitude=float(64.04351684568181),
            tags='lmxrmazedazxluxkgvpz',
            sequence_number=int(54)
        )
        return instance

    
    def test_change_type_property(self):
        """
        Test change_type property
        """
        test_value = 'jldrfiemlelogzqfpmqk'
        self.instance.change_type = test_value
        self.assertEqual(self.instance.change_type, test_value)
    
    def test_element_type_property(self):
        """
        Test element_type property
        """
        test_value = 'osgmzjavluqjlxsqcoct'
        self.instance.element_type = test_value
        self.assertEqual(self.instance.element_type, test_value)
    
    def test_element_id_property(self):
        """
        Test element_id property
        """
        test_value = int(15)
        self.instance.element_id = test_value
        self.assertEqual(self.instance.element_id, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'zkwfpmffxrypjsmcejto'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = int(2)
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
        test_value = int(0)
        self.instance.changeset_id = test_value
        self.assertEqual(self.instance.changeset_id, test_value)
    
    def test_user_name_property(self):
        """
        Test user_name property
        """
        test_value = 'jclntqgaabznwlcnckkm'
        self.instance.user_name = test_value
        self.assertEqual(self.instance.user_name, test_value)
    
    def test_user_id_property(self):
        """
        Test user_id property
        """
        test_value = int(19)
        self.instance.user_id = test_value
        self.assertEqual(self.instance.user_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(35.639272025132904)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(64.04351684568181)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_tags_property(self):
        """
        Test tags property
        """
        test_value = 'lmxrmazedazxluxkgvpz'
        self.instance.tags = test_value
        self.assertEqual(self.instance.tags, test_value)
    
    def test_sequence_number_property(self):
        """
        Test sequence_number property
        """
        test_value = int(54)
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

