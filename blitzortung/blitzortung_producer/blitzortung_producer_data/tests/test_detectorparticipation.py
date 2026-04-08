"""
Test case for DetectorParticipation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from blitzortung_producer_data.detectorparticipation import DetectorParticipation


class Test_DetectorParticipation(unittest.TestCase):
    """
    Test case for DetectorParticipation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DetectorParticipation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DetectorParticipation for testing
        """
        instance = DetectorParticipation(
            station_id=int(52),
            status=int(72)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(52)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = int(72)
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DetectorParticipation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DetectorParticipation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

