"""
Test case for DetectorParticipation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from blitzortung_producer_data.blitzortung.lightning.detectorparticipation import DetectorParticipation


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
            station_id=int(74),
            status=int(55)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(74)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = int(55)
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DetectorParticipation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
