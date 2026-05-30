"""
Test case for Block
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_mqtt_producer_data.bluesky.graph.block import Block


class Test_Block(unittest.TestCase):
    """
    Test case for Block
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Block.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Block for testing
        """
        instance = Block(
            uri='ixztxvrlrxdpdujrsjnp',
            cid='cimwuzhudqsihzwcheon',
            did='utjscsihkwilxsxgapqi',
            handle='iwwsystrnuxycdvnzciv',
            subject='jrxlbpoqvseiamllsqpl',
            subject_handle='uwydijlvdbwsgjwucxzx',
            created_at='dzhurzpcrvavszlvopta',
            indexed_at='gotdibchzsmgsvnbiasu',
            seq=int(14),
            collection='tqdtdcrrndppvluubuhx',
            lang='pqhlpvlnzbkxjimvdtvk'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'ixztxvrlrxdpdujrsjnp'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'cimwuzhudqsihzwcheon'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'utjscsihkwilxsxgapqi'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'iwwsystrnuxycdvnzciv'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_property(self):
        """
        Test subject property
        """
        test_value = 'jrxlbpoqvseiamllsqpl'
        self.instance.subject = test_value
        self.assertEqual(self.instance.subject, test_value)
    
    def test_subject_handle_property(self):
        """
        Test subject_handle property
        """
        test_value = 'uwydijlvdbwsgjwucxzx'
        self.instance.subject_handle = test_value
        self.assertEqual(self.instance.subject_handle, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'dzhurzpcrvavszlvopta'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'gotdibchzsmgsvnbiasu'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(14)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'tqdtdcrrndppvluubuhx'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'pqhlpvlnzbkxjimvdtvk'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Block.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Block.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

