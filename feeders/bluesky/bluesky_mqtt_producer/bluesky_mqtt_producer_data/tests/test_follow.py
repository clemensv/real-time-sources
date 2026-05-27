"""
Test case for Follow
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_mqtt_producer_data.bluesky.graph.follow import Follow


class Test_Follow(unittest.TestCase):
    """
    Test case for Follow
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Follow.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Follow for testing
        """
        instance = Follow(
            uri='unjverlpuclvwqqhanpu',
            cid='wmbcfepxyeycjdbuxarb',
            did='umbgjgpxgesrondauaqc',
            handle='tptqhbtmiomqfxwrgwne',
            subject='tlwoclsbwymiclzbcmvz',
            subject_handle='avarfwicsgvwpjyjgofp',
            created_at='rduywteaipaareyqhdqk',
            indexed_at='umoecizblopkphervsyl',
            seq=int(56),
            collection='marpfndoohicedvboagx',
            lang='qrybufmzxfeavdbjjkef'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'unjverlpuclvwqqhanpu'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'wmbcfepxyeycjdbuxarb'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'umbgjgpxgesrondauaqc'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'tptqhbtmiomqfxwrgwne'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_property(self):
        """
        Test subject property
        """
        test_value = 'tlwoclsbwymiclzbcmvz'
        self.instance.subject = test_value
        self.assertEqual(self.instance.subject, test_value)
    
    def test_subject_handle_property(self):
        """
        Test subject_handle property
        """
        test_value = 'avarfwicsgvwpjyjgofp'
        self.instance.subject_handle = test_value
        self.assertEqual(self.instance.subject_handle, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'rduywteaipaareyqhdqk'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'umoecizblopkphervsyl'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(56)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'marpfndoohicedvboagx'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'qrybufmzxfeavdbjjkef'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Follow.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Follow.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

