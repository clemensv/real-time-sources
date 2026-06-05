"""
Test case for DoseRateMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bfs_odl_mqtt_producer_data.de.bfs.odl.doseratemeasurement import DoseRateMeasurement


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
            station_id='kpulpghbjbbyugwdjzxc',
            state='dpbyebjzpnwjpgxwdoff',
            start_measure='vvrzeogedlmzbwbaqveh',
            end_measure='bxfqbwcigtyxzcdjxyic',
            value=float(13.478491327569674),
            value_cosmic=float(42.26235573027402),
            value_terrestrial=float(41.11640931324363),
            validated=int(37),
            nuclide='qyqfczmmgqgnqhcacfjf'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'kpulpghbjbbyugwdjzxc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'dpbyebjzpnwjpgxwdoff'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'vvrzeogedlmzbwbaqveh'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'bxfqbwcigtyxzcdjxyic'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(13.478491327569674)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_value_cosmic_property(self):
        """
        Test value_cosmic property
        """
        test_value = float(42.26235573027402)
        self.instance.value_cosmic = test_value
        self.assertEqual(self.instance.value_cosmic, test_value)
    
    def test_value_terrestrial_property(self):
        """
        Test value_terrestrial property
        """
        test_value = float(41.11640931324363)
        self.instance.value_terrestrial = test_value
        self.assertEqual(self.instance.value_terrestrial, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(37)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'qyqfczmmgqgnqhcacfjf'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DoseRateMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DoseRateMeasurement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

