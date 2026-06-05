"""
Test case for MaintenanceTracking
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.maintenancetracking import MaintenanceTracking


class Test_MaintenanceTracking(unittest.TestCase):
    """
    Test case for MaintenanceTracking
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MaintenanceTracking.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MaintenanceTracking for testing
        """
        instance = MaintenanceTracking(
            domain='bdtqcgdtmcvfdfloiuxo',
            time=int(50),
            source='inyduwfyenxbiutyhjlk',
            tasks=['fyysykdfpjujiuccwkrm'],
            x=float(15.129539018552796),
            y=float(78.96174862678018),
            direction=float(82.4945036723031)
        )
        return instance

    
    def test_domain_property(self):
        """
        Test domain property
        """
        test_value = 'bdtqcgdtmcvfdfloiuxo'
        self.instance.domain = test_value
        self.assertEqual(self.instance.domain, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(50)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'inyduwfyenxbiutyhjlk'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_tasks_property(self):
        """
        Test tasks property
        """
        test_value = ['fyysykdfpjujiuccwkrm']
        self.instance.tasks = test_value
        self.assertEqual(self.instance.tasks, test_value)
    
    def test_x_property(self):
        """
        Test x property
        """
        test_value = float(15.129539018552796)
        self.instance.x = test_value
        self.assertEqual(self.instance.x, test_value)
    
    def test_y_property(self):
        """
        Test y property
        """
        test_value = float(78.96174862678018)
        self.instance.y = test_value
        self.assertEqual(self.instance.y, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = float(82.4945036723031)
        self.instance.direction = test_value
        self.assertEqual(self.instance.direction, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MaintenanceTracking.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MaintenanceTracking.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

