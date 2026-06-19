"""
Test case for Earthquake
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fdsn_seismology_amqp_producer_data.org.fdsn.event.earthquake import Earthquake
import datetime


class Test_Earthquake(unittest.TestCase):
    """
    Test case for Earthquake
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Earthquake.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Earthquake for testing
        """
        instance = Earthquake(
            event_id='apjlrjwhdppbgwdtrnzq',
            time=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(82.51995768000879),
            longitude=float(54.70425003414312),
            depth_km=float(64.63124301386162),
            author='iecvduooftdnhfmyfggk',
            catalog='lrlocbwvgcojnmniqqhb',
            contributor='wrpxcwgvlsajzcwgecns',
            contributor_id='pawibkrqizbwsadfjkrt',
            magnitude_type='rpbvokeyvzoisibbyjdy',
            magnitude=float(70.98133305220406),
            magnitude_author='tsbypfalasgxepxmafms',
            event_location_name='hlpqebguetzysxuvheei',
            event_type='vnqxfhgfxnisuvzsfnzk',
            node_url='ktwqttlypccivudwfggh'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'apjlrjwhdppbgwdtrnzq'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(82.51995768000879)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(54.70425003414312)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_km_property(self):
        """
        Test depth_km property
        """
        test_value = float(64.63124301386162)
        self.instance.depth_km = test_value
        self.assertEqual(self.instance.depth_km, test_value)
    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = 'iecvduooftdnhfmyfggk'
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_catalog_property(self):
        """
        Test catalog property
        """
        test_value = 'lrlocbwvgcojnmniqqhb'
        self.instance.catalog = test_value
        self.assertEqual(self.instance.catalog, test_value)
    
    def test_contributor_property(self):
        """
        Test contributor property
        """
        test_value = 'wrpxcwgvlsajzcwgecns'
        self.instance.contributor = test_value
        self.assertEqual(self.instance.contributor, test_value)
    
    def test_contributor_id_property(self):
        """
        Test contributor_id property
        """
        test_value = 'pawibkrqizbwsadfjkrt'
        self.instance.contributor_id = test_value
        self.assertEqual(self.instance.contributor_id, test_value)
    
    def test_magnitude_type_property(self):
        """
        Test magnitude_type property
        """
        test_value = 'rpbvokeyvzoisibbyjdy'
        self.instance.magnitude_type = test_value
        self.assertEqual(self.instance.magnitude_type, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(70.98133305220406)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_magnitude_author_property(self):
        """
        Test magnitude_author property
        """
        test_value = 'tsbypfalasgxepxmafms'
        self.instance.magnitude_author = test_value
        self.assertEqual(self.instance.magnitude_author, test_value)
    
    def test_event_location_name_property(self):
        """
        Test event_location_name property
        """
        test_value = 'hlpqebguetzysxuvheei'
        self.instance.event_location_name = test_value
        self.assertEqual(self.instance.event_location_name, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'vnqxfhgfxnisuvzsfnzk'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_node_url_property(self):
        """
        Test node_url property
        """
        test_value = 'ktwqttlypccivudwfggh'
        self.instance.node_url = test_value
        self.assertEqual(self.instance.node_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Earthquake.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Earthquake.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

