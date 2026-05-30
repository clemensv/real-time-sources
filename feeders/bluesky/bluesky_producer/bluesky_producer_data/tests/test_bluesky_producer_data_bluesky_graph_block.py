"""
Test case for Block
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_producer_data.bluesky.graph.block import Block


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
            uri='spqhbndhkrunestnicrg',
            cid='vtklvushzwsmwpxegjgw',
            did='gmsdjydreoqmcqyhcvel',
            handle='czmcrfypmvruzjzfhssu',
            subject='jedfpxtzqscddwmgrsms',
            subject_handle='bqiiyvtxgvkjqghvqxvx',
            created_at='wzqtpnpyyhhjjrxsyswj',
            indexed_at='xmxmnzarrflimknwdgem',
            seq=int(68),
            collection='ukrqjzhmfharureazyar',
            lang='zwqmyauvutbjdvusnxth'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'spqhbndhkrunestnicrg'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'vtklvushzwsmwpxegjgw'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'gmsdjydreoqmcqyhcvel'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'czmcrfypmvruzjzfhssu'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_property(self):
        """
        Test subject property
        """
        test_value = 'jedfpxtzqscddwmgrsms'
        self.instance.subject = test_value
        self.assertEqual(self.instance.subject, test_value)
    
    def test_subject_handle_property(self):
        """
        Test subject_handle property
        """
        test_value = 'bqiiyvtxgvkjqghvqxvx'
        self.instance.subject_handle = test_value
        self.assertEqual(self.instance.subject_handle, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'wzqtpnpyyhhjjrxsyswj'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'xmxmnzarrflimknwdgem'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(68)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'ukrqjzhmfharureazyar'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'zwqmyauvutbjdvusnxth'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Block.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
