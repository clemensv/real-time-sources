"""
Test case for Like
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_producer_data.bluesky.feed.like import Like


class Test_Like(unittest.TestCase):
    """
    Test case for Like
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Like.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Like for testing
        """
        instance = Like(
            uri='zyjoslxcydzrotbmwscm',
            cid='ifpxlivlguuaptorokks',
            did='lfivnpvpgvjemkkhizmk',
            handle='aerjmakpdiwwwovfhrls',
            subject_uri='gjcyztjgvmdjqjxmrcud',
            subject_cid='cnmxybdsaakyulhmjlcj',
            created_at='olzdfccroqycckqrtnqh',
            indexed_at='hunntbmvhnojwqcfwyrn',
            seq=int(93),
            collection='zammhfdwqglkmmnfbspf',
            lang='kovcomjzmieuuflpnrqp'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'zyjoslxcydzrotbmwscm'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'ifpxlivlguuaptorokks'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'lfivnpvpgvjemkkhizmk'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'aerjmakpdiwwwovfhrls'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_uri_property(self):
        """
        Test subject_uri property
        """
        test_value = 'gjcyztjgvmdjqjxmrcud'
        self.instance.subject_uri = test_value
        self.assertEqual(self.instance.subject_uri, test_value)
    
    def test_subject_cid_property(self):
        """
        Test subject_cid property
        """
        test_value = 'cnmxybdsaakyulhmjlcj'
        self.instance.subject_cid = test_value
        self.assertEqual(self.instance.subject_cid, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'olzdfccroqycckqrtnqh'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'hunntbmvhnojwqcfwyrn'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(93)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'zammhfdwqglkmmnfbspf'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'kovcomjzmieuuflpnrqp'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Like.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
