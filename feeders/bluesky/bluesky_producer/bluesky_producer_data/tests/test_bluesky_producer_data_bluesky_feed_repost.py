"""
Test case for Repost
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_producer_data.bluesky.feed.repost import Repost


class Test_Repost(unittest.TestCase):
    """
    Test case for Repost
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Repost.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Repost for testing
        """
        instance = Repost(
            uri='quuryyqvtqudquoighaw',
            cid='pncqmwpfhaikrnrinfzt',
            did='bpbyxvmhidnftripzvsh',
            handle='farbtsqvnixcsbmavpbx',
            subject_uri='fupgdidrzphelyyksxvb',
            subject_cid='zukogkxvngtyrpsutliw',
            created_at='fqwbkrbqzscdsiwzlzzf',
            indexed_at='xybicufbvpsvgwmacbfr',
            seq=int(25)
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'quuryyqvtqudquoighaw'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'pncqmwpfhaikrnrinfzt'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'bpbyxvmhidnftripzvsh'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'farbtsqvnixcsbmavpbx'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_uri_property(self):
        """
        Test subject_uri property
        """
        test_value = 'fupgdidrzphelyyksxvb'
        self.instance.subject_uri = test_value
        self.assertEqual(self.instance.subject_uri, test_value)
    
    def test_subject_cid_property(self):
        """
        Test subject_cid property
        """
        test_value = 'zukogkxvngtyrpsutliw'
        self.instance.subject_cid = test_value
        self.assertEqual(self.instance.subject_cid, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'fqwbkrbqzscdsiwzlzzf'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'xybicufbvpsvgwmacbfr'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(25)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Repost.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
