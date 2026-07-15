"""
Test case for SubmissionStatusType
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_producer_data.io.openchargemap.submissionstatustype import SubmissionStatusType


class Test_SubmissionStatusType(unittest.TestCase):
    """
    Test case for SubmissionStatusType
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SubmissionStatusType.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SubmissionStatusType for testing
        """
        instance = SubmissionStatusType(
            reference_type='jefgpdtouwcgavxuusat',
            reference_id=int(70),
            title='rcvjdnkgizybpztrewlv',
            is_live=False
        )
        return instance

    
    def test_reference_type_property(self):
        """
        Test reference_type property
        """
        test_value = 'jefgpdtouwcgavxuusat'
        self.instance.reference_type = test_value
        self.assertEqual(self.instance.reference_type, test_value)
    
    def test_reference_id_property(self):
        """
        Test reference_id property
        """
        test_value = int(70)
        self.instance.reference_id = test_value
        self.assertEqual(self.instance.reference_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'rcvjdnkgizybpztrewlv'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_is_live_property(self):
        """
        Test is_live property
        """
        test_value = False
        self.instance.is_live = test_value
        self.assertEqual(self.instance.is_live, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SubmissionStatusType.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SubmissionStatusType.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

