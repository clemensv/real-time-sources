"""
Test case for DoseRateMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bfs_odl_producer_data.de.bfs.odl.doseratemeasurement import DoseRateMeasurement


class Test_DoseRateMeasurement(unittest.TestCase):
    """
    Test case for DoseRateMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DoseRateMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DoseRateMeasurement for testing
        """
        instance = DoseRateMeasurement(
            station_id='edogknasiyizuvogugpj',
            start_measure='wqkoryojjsweynelaobf',
            end_measure='ohqxdeceytlzskpnxrsk',
            value=float(85.89248733302924),
            value_cosmic=float(20.30218714063553),
            value_terrestrial=float(55.25935559556538),
            validated=int(48),
            nuclide='srwmoyrzxlvzgbvswmkg'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'edogknasiyizuvogugpj'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'wqkoryojjsweynelaobf'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'ohqxdeceytlzskpnxrsk'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(85.89248733302924)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_value_cosmic_property(self):
        """
        Test value_cosmic property
        """
        test_value = float(20.30218714063553)
        self.instance.value_cosmic = test_value
        self.assertEqual(self.instance.value_cosmic, test_value)
    
    def test_value_terrestrial_property(self):
        """
        Test value_terrestrial property
        """
        test_value = float(55.25935559556538)
        self.instance.value_terrestrial = test_value
        self.assertEqual(self.instance.value_terrestrial, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(48)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'srwmoyrzxlvzgbvswmkg'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DoseRateMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
