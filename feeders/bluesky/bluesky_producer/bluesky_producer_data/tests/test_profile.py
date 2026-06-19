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
            did='bjzuxgvdibdgxwesseeh',
            handle='rirwgmvpjuosmyfndusg',
            display_name='ewutsglmphnnwsnwauso',
            description='kgptrevidvmkueawmafv',
            avatar='zqefqlhqrwwbhoajwrnw',
            banner='creughuvlrxbcnovlkfr',
            created_at='mmplzvskmrujgzguahuf',
            indexed_at='fjchrzmfvbcwdncikqvf',
            seq=int(36),
            collection='cnifgndyruyejdbbcfni',
            lang='vmmnmrfzrpcjxcxhasdf'
        )
        return instance

    
    def test_did_property(self):
        """
        Test did property
        """
        test_value = 'bjzuxgvdibdgxwesseeh'
        self.instance.did = test_value
        self.assertEqual(self.instance.did, test_value)
    
    def test_handle_property(self):
        """
        Test handle property
        """
        test_value = 'rirwgmvpjuosmyfndusg'
        self.instance.handle = test_value
        self.assertEqual(self.instance.handle, test_value)
    
    def test_display_name_property(self):
        """
        Test display_name property
        """
        test_value = 'ewutsglmphnnwsnwauso'
        self.instance.display_name = test_value
        self.assertEqual(self.instance.display_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'kgptrevidvmkueawmafv'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_avatar_property(self):
        """
        Test avatar property
        """
        test_value = 'zqefqlhqrwwbhoajwrnw'
        self.instance.avatar = test_value
        self.assertEqual(self.instance.avatar, test_value)
    
    def test_banner_property(self):
        """
        Test banner property
        """
        test_value = 'creughuvlrxbcnovlkfr'
        self.instance.banner = test_value
        self.assertEqual(self.instance.banner, test_value)
    
    def test_created_at_property(self):
        """
        Test created_at property
        """
        test_value = 'mmplzvskmrujgzguahuf'
        self.instance.created_at = test_value
        self.assertEqual(self.instance.created_at, test_value)
    
    def test_indexed_at_property(self):
        """
        Test indexed_at property
        """
        test_value = 'fjchrzmfvbcwdncikqvf'
        self.instance.indexed_at = test_value
        self.assertEqual(self.instance.indexed_at, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(36)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_collection_property(self):
        """
        Test collection property
        """
        test_value = 'cnifgndyruyejdbbcfni'
        self.instance.collection = test_value
        self.assertEqual(self.instance.collection, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'vmmnmrfzrpcjxcxhasdf'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Profile.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Profile.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

