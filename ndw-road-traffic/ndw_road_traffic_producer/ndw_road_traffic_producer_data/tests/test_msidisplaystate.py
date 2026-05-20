"""
Test case for MsiDisplayState
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_producer_data.msidisplaystate import MsiDisplayState


class Test_MsiDisplayState(unittest.TestCase):
    """
    Test case for MsiDisplayState
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MsiDisplayState.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MsiDisplayState for testing
        """
        instance = MsiDisplayState(
            sign_id='ynxbhynrvxooulrritxw',
            publication_time='jrczgnvozgedxckqfwey',
            image_code='voeeirsblmurlqybiibx',
            state='gulsqyquxgbesviykieo',
            speed_limit=int(38)
        )
        return instance

    
    def test_sign_id_property(self):
        """
        Test sign_id property
        """
        test_value = 'ynxbhynrvxooulrritxw'
        self.instance.sign_id = test_value
        self.assertEqual(self.instance.sign_id, test_value)
    
    def test_publication_time_property(self):
        """
        Test publication_time property
        """
        test_value = 'jrczgnvozgedxckqfwey'
        self.instance.publication_time = test_value
        self.assertEqual(self.instance.publication_time, test_value)
    
    def test_image_code_property(self):
        """
        Test image_code property
        """
        test_value = 'voeeirsblmurlqybiibx'
        self.instance.image_code = test_value
        self.assertEqual(self.instance.image_code, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'gulsqyquxgbesviykieo'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_speed_limit_property(self):
        """
        Test speed_limit property
        """
        test_value = int(38)
        self.instance.speed_limit = test_value
        self.assertEqual(self.instance.speed_limit, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MsiDisplayState.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MsiDisplayState.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

