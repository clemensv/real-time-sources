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
            domain='nbljklppkdujxxdognup',
            time=int(1),
            source='hhtduiysgjihocedfsvq',
            tasks=['dvmabzqvqsgrsqenjlso', 'dnuglfpfwkexycvzrurs', 'wdwqvavrivomvypkvjsc', 'unzbywkpxwvkkwptnori', 'hslwpfmpcbhbqmbhvtwy'],
            x=float(76.99382410493268),
            y=float(2.2388877266298124),
            direction=float(19.963480131582724)
        )
        return instance

    
    def test_domain_property(self):
        """
        Test domain property
        """
        test_value = 'nbljklppkdujxxdognup'
        self.instance.domain = test_value
        self.assertEqual(self.instance.domain, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(1)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'hhtduiysgjihocedfsvq'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_tasks_property(self):
        """
        Test tasks property
        """
        test_value = ['dvmabzqvqsgrsqenjlso', 'dnuglfpfwkexycvzrurs', 'wdwqvavrivomvypkvjsc', 'unzbywkpxwvkkwptnori', 'hslwpfmpcbhbqmbhvtwy']
        self.instance.tasks = test_value
        self.assertEqual(self.instance.tasks, test_value)
    
    def test_x_property(self):
        """
        Test x property
        """
        test_value = float(76.99382410493268)
        self.instance.x = test_value
        self.assertEqual(self.instance.x, test_value)
    
    def test_y_property(self):
        """
        Test y property
        """
        test_value = float(2.2388877266298124)
        self.instance.y = test_value
        self.assertEqual(self.instance.y, test_value)
    
    def test_direction_property(self):
        """
        Test direction property
        """
        test_value = float(19.963480131582724)
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

