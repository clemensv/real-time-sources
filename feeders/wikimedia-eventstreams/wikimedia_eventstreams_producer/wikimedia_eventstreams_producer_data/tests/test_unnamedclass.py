"""
Test case for UnnamedClass
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wikimedia_eventstreams_producer_data.unnamedclass import UnnamedClass


class Test_UnnamedClass(unittest.TestCase):
    """
    Test case for UnnamedClass
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_UnnamedClass.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of UnnamedClass for testing
        """
        instance = UnnamedClass(
            uri='dtxiilfyovhipgcfnwqd',
            request_id='mbycbqaqfvlbbktdexvd',
            id='hxfcmitwnwhkdxgfbpfs',
            domain='jnsuwlwinmzhtdocnrvj',
            stream='pmavbvmdfzkxrpslrmdi',
            topic='vgxvdtnayxwxcygmsbeh',
            partition=int(63),
            offset='sgubgjbnvycxznxnhxbg',
            dt='sqjflpntejqhpzhvyjza'
        )
        return instance

    
    def test_uri_property(self):
        """
        Test uri property
        """
        test_value = 'dtxiilfyovhipgcfnwqd'
        self.instance.uri = test_value
        self.assertEqual(self.instance.uri, test_value)
    
    def test_request_id_property(self):
        """
        Test request_id property
        """
        test_value = 'mbycbqaqfvlbbktdexvd'
        self.instance.request_id = test_value
        self.assertEqual(self.instance.request_id, test_value)
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'hxfcmitwnwhkdxgfbpfs'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_domain_property(self):
        """
        Test domain property
        """
        test_value = 'jnsuwlwinmzhtdocnrvj'
        self.instance.domain = test_value
        self.assertEqual(self.instance.domain, test_value)
    
    def test_stream_property(self):
        """
        Test stream property
        """
        test_value = 'pmavbvmdfzkxrpslrmdi'
        self.instance.stream = test_value
        self.assertEqual(self.instance.stream, test_value)
    
    def test_topic_property(self):
        """
        Test topic property
        """
        test_value = 'vgxvdtnayxwxcygmsbeh'
        self.instance.topic = test_value
        self.assertEqual(self.instance.topic, test_value)
    
    def test_partition_property(self):
        """
        Test partition property
        """
        test_value = int(63)
        self.instance.partition = test_value
        self.assertEqual(self.instance.partition, test_value)
    
    def test_offset_property(self):
        """
        Test offset property
        """
        test_value = 'sgubgjbnvycxznxnhxbg'
        self.instance.offset = test_value
        self.assertEqual(self.instance.offset, test_value)
    
    def test_dt_property(self):
        """
        Test dt property
        """
        test_value = 'sqjflpntejqhpzhvyjza'
        self.instance.dt = test_value
        self.assertEqual(self.instance.dt, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = UnnamedClass.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = UnnamedClass.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

