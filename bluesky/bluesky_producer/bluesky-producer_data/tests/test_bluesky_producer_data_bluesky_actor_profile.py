"""
Test case for Profile
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bluesky_producer_data.bluesky.actor.profile import Profile


class Test_Profile(unittest.TestCase):
    """
    Test case for Profile
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Profile.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Profile for testing
        """
        instance = Profile(
            did='qokzcercvaauqtphcydj',
            handle='igxthysiozrdryzidusf',
            display_name='nbcetyvtnimdwnkxvdld',
            description='tgcndpldenldyygwesag',
            avatar='ykpusttpfjowalgrfkgp',
            banner='rsijcmmykscrezwpovyt',
            created_at='wxizovsmtsqzcnchxkkw',
            indexed_at='ypmgsribaqvnpsvryiqf',
            seq=int(19)
        )
        return instance

    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'qokzcercvaauqtphcydj'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'igxthysiozrdryzidusf'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_display_name_property(self):
        """
        Test display_name property
        """
        test_value = 'nbcetyvtnimdwnkxvdld'
        self.instance.display_name = test_value
        self.assertEqual(self.instance.display_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'tgcndpldenldyygwesag'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_avatar_property(self):
        """
        Test avatar property
        """
        test_value = 'ykpusttpfjowalgrfkgp'
        self.instance.avatar = test_value
        self.assertEqual(self.instance.avatar, test_value)
    
    def test_banner_property(self):
        """
        Test banner property
        """
        test_value = 'rsijcmmykscrezwpovyt'
        self.instance.banner = test_value
        self.assertEqual(self.instance.banner, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'wxizovsmtsqzcnchxkkw'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'ypmgsribaqvnpsvryiqf'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(19)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Profile.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
