"""
Test case for DoseRateMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bfs_odl_amqp_producer_data.de.bfs.odl.doseratemeasurement import DoseRateMeasurement


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
            station_id='gdhedtsjzajkplhfecqi',
            start_measure='zohuxetnpsdlcprhtath',
            end_measure='gupbvabrlqjzpxqhilbd',
            value=float(74.10041762835155),
            value_cosmic=float(28.084907906282552),
            value_terrestrial=float(74.66240325387045),
            validated=int(100),
            nuclide='mkfsrzyfvfxakzyntmmy',
            canton='rcbzooizsdxkwfejhjhd'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gdhedtsjzajkplhfecqi'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'zohuxetnpsdlcprhtath'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'gupbvabrlqjzpxqhilbd'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(74.10041762835155)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_value_cosmic_property(self):
        """
        Test value_cosmic property
        """
        test_value = float(28.084907906282552)
        self.instance.value_cosmic = test_value
        self.assertEqual(self.instance.value_cosmic, test_value)
    
    def test_value_terrestrial_property(self):
        """
        Test value_terrestrial property
        """
        test_value = float(74.66240325387045)
        self.instance.value_terrestrial = test_value
        self.assertEqual(self.instance.value_terrestrial, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(100)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'mkfsrzyfvfxakzyntmmy'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_canton_property(self):
        """
        Test canton property
        """
        test_value = 'rcbzooizsdxkwfejhjhd'
        self.instance.canton = test_value
        self.assertEqual(self.instance.canton, test_value)
    
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

