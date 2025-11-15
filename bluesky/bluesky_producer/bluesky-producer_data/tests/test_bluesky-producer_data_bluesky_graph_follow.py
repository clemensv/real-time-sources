"""
Test case for Follow
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky-producer_data.bluesky.graph.follow import Follow


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
            uri='ishxdfdnzwnpyegbggrn',
            cid='zqewnwmwevbwvmiwsneu',
            did='hdszkcfuutzjmlrvdtvd',
            handle='lbaluwyjizbrddivpuxw',
            subject='hsnhngedvxrctpjluxmp',
            subject_handle='mryosuemiodwyaphmugl',
            created_at='bxxgvelakgspumxwcdhg',
            indexed_at='yexhblmhknqyhozybqct',
            seq=int(7)
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'ishxdfdnzwnpyegbggrn'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = 'zqewnwmwevbwvmiwsneu'
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'hdszkcfuutzjmlrvdtvd'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'lbaluwyjizbrddivpuxw'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_subject_property(self):
        """
        Test subject property
        """
        test_value = 'hsnhngedvxrctpjluxmp'
        self.instance.subject = test_value
        self.assertEqual(self.instance.subject, test_value)
    
    def test_subject_handle_property(self):
        """
        Test subject_handle property
        """
        test_value = 'mryosuemiodwyaphmugl'
        self.instance.subject_handle = test_value
        self.assertEqual(self.instance.subject_handle, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'bxxgvelakgspumxwcdhg'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'yexhblmhknqyhozybqct'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(7)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Follow.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
