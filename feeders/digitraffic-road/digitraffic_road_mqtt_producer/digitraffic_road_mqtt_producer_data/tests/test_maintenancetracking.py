"""
Test case for MaintenanceTracking
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_mqtt_producer_data.maintenancetracking import MaintenanceTracking


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
            domain='vjirilgvreyyizfzrkfu',
            time=int(14),
            source='xheipawjaolxhysovczf',
            tasks=['qekmtrososzjwcbtaaqk', 'lyxpozzqwxsrlumgbgjb', 'twsowzfkgwpepovwvvqg'],
            x=float(16.012464443488174),
            y=float(7.139815261878324),
            direction=float(71.84001085265362)
        )
        return instance

    
    def test_domain_property(self):
        """
        Test domain property
        """
        test_value = 'vjirilgvreyyizfzrkfu'
        self.instance.domain = test_value
        self.assertEqual(self.instance.domain, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(14)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'xheipawjaolxhysovczf'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_tasks_property(self):
        """
        Test tasks property
        """
        test_value = ['qekmtrososzjwcbtaaqk', 'lyxpozzqwxsrlumgbgjb', 'twsowzfkgwpepovwvvqg']
        self.instance.tasks = test_value
        self.assertEqual(self.instance.tasks, test_value)
    
    def test_x_property(self):
        """
        Test x property
        """
        test_value = float(16.012464443488174)
        self.instance.x = test_value
        self.assertEqual(self.instance.x, test_value)
    
    def test_y_property(self):
        """
        Test y property
        """
        test_value = float(7.139815261878324)
        self.instance.y = test_value
        self.assertEqual(self.instance.y, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = float(71.84001085265362)
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

