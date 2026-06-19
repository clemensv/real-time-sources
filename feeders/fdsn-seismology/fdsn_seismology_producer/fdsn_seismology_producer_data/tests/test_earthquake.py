"""
Test case for Earthquake
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fdsn_seismology_producer_data.org.fdsn.event.earthquake import Earthquake
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
            event_id='lxwhbxcivapznokbplmx',
            time=datetime.datetime.now(datetime.timezone.utc),
            latitude=float(58.44462692874745),
            longitude=float(24.049811072005134),
            depth_km=float(11.407028755782001),
            author='kfysotcxqtjgdavxvamj',
            catalog='rfqmjcycbpngdiowrghm',
            contributor='aojrjlytfotlsrboeflm',
            contributor_id='hxcevsunlyqztoopvlei',
            magnitude_type='jjvcqecsafjkjgkvegyl',
            magnitude=float(98.12203727163813),
            magnitude_author='aniiwpkgzxqvbyyevtlv',
            event_location_name='cxxubmtourcddhgkvtll',
            event_type='sufanyyrjsengqidzcmj',
            node_url='pozgwdaiwfgaakwfrssb'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'lxwhbxcivapznokbplmx'
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
        test_value = float(58.44462692874745)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(24.049811072005134)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_km_property(self):
        """
        Test depth_km property
        """
        test_value = float(11.407028755782001)
        self.instance.depth_km = test_value
        self.assertEqual(self.instance.depth_km, test_value)
    
    def test_author_property(self):
        """
        Test author property
        """
        test_value = 'kfysotcxqtjgdavxvamj'
        self.instance.author = test_value
        self.assertEqual(self.instance.author, test_value)
    
    def test_catalog_property(self):
        """
        Test catalog property
        """
        test_value = 'rfqmjcycbpngdiowrghm'
        self.instance.catalog = test_value
        self.assertEqual(self.instance.catalog, test_value)
    
    def test_contributor_property(self):
        """
        Test contributor property
        """
        test_value = 'aojrjlytfotlsrboeflm'
        self.instance.contributor = test_value
        self.assertEqual(self.instance.contributor, test_value)
    
    def test_contributor_id_property(self):
        """
        Test contributor_id property
        """
        test_value = 'hxcevsunlyqztoopvlei'
        self.instance.contributor_id = test_value
        self.assertEqual(self.instance.contributor_id, test_value)
    
    def test_magnitude_type_property(self):
        """
        Test magnitude_type property
        """
        test_value = 'jjvcqecsafjkjgkvegyl'
        self.instance.magnitude_type = test_value
        self.assertEqual(self.instance.magnitude_type, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(98.12203727163813)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_magnitude_author_property(self):
        """
        Test magnitude_author property
        """
        test_value = 'aniiwpkgzxqvbyyevtlv'
        self.instance.magnitude_author = test_value
        self.assertEqual(self.instance.magnitude_author, test_value)
    
    def test_event_location_name_property(self):
        """
        Test event_location_name property
        """
        test_value = 'cxxubmtourcddhgkvtll'
        self.instance.event_location_name = test_value
        self.assertEqual(self.instance.event_location_name, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'sufanyyrjsengqidzcmj'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_node_url_property(self):
        """
        Test node_url property
        """
        test_value = 'pozgwdaiwfgaakwfrssb'
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

