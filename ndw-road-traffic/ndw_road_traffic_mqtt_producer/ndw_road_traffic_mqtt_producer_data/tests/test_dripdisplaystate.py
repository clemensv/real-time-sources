"""
Test case for DripDisplayState
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndw_road_traffic_mqtt_producer_data.dripdisplaystate import DripDisplayState


class Test_DripDisplayState(unittest.TestCase):
    """
    Test case for DripDisplayState
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DripDisplayState.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DripDisplayState for testing
        """
        instance = DripDisplayState(
            vms_controller_id='yfvxtjxaewsacjhdnivh',
            vms_index='uxfnprnnkdpxqcmbgtjz',
            publication_time='qqowamqirllzaubjktwe',
            active=False,
            vms_text='rwlnazfcrdwahzioriat',
            pictogram_code='vftuxzkkbaphngfsejza',
            state='ufoulkowkaihvjixzqol'
        )
        return instance

    
    def test_vms_controller_id_property(self):
        """
        Test vms_controller_id property
        """
        test_value = 'yfvxtjxaewsacjhdnivh'
        self.instance.vms_controller_id = test_value
        self.assertEqual(self.instance.vms_controller_id, test_value)
    
    def test_vms_index_property(self):
        """
        Test vms_index property
        """
        test_value = 'uxfnprnnkdpxqcmbgtjz'
        self.instance.vms_index = test_value
        self.assertEqual(self.instance.vms_index, test_value)
    
    def test_publication_time_property(self):
        """
        Test publication_time property
        """
        test_value = 'qqowamqirllzaubjktwe'
        self.instance.publication_time = test_value
        self.assertEqual(self.instance.publication_time, test_value)
    
    def test_active_property(self):
        """
        Test active property
        """
        test_value = False
        self.instance.active = test_value
        self.assertEqual(self.instance.active, test_value)
    
    def test_vms_text_property(self):
        """
        Test vms_text property
        """
        test_value = 'rwlnazfcrdwahzioriat'
        self.instance.vms_text = test_value
        self.assertEqual(self.instance.vms_text, test_value)
    
    def test_pictogram_code_property(self):
        """
        Test pictogram_code property
        """
        test_value = 'vftuxzkkbaphngfsejza'
        self.instance.pictogram_code = test_value
        self.assertEqual(self.instance.pictogram_code, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'ufoulkowkaihvjixzqol'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DripDisplayState.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DripDisplayState.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

