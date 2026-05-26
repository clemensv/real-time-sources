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
            station_id='dfggkryonnwvjbasdgfw',
            start_measure='tdagqtghxwxhqjtjqnlp',
            end_measure='kjsuozxedncywtvnjcvk',
            value=float(84.8974453337415),
            value_cosmic=float(98.341472964917),
            value_terrestrial=float(16.86751796387793),
            validated=int(36),
            nuclide='ncqhwhpnetbskhtuiswv',
            canton='qsgxxewadtzjajqfmgbx'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'dfggkryonnwvjbasdgfw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'tdagqtghxwxhqjtjqnlp'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'kjsuozxedncywtvnjcvk'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(84.8974453337415)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_value_cosmic_property(self):
        """
        Test value_cosmic property
        """
        test_value = float(98.341472964917)
        self.instance.value_cosmic = test_value
        self.assertEqual(self.instance.value_cosmic, test_value)
    
    def test_value_terrestrial_property(self):
        """
        Test value_terrestrial property
        """
        test_value = float(16.86751796387793)
        self.instance.value_terrestrial = test_value
        self.assertEqual(self.instance.value_terrestrial, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(36)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'ncqhwhpnetbskhtuiswv'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_canton_property(self):
        """
        Test canton property
        """
        test_value = 'qsgxxewadtzjajqfmgbx'
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

