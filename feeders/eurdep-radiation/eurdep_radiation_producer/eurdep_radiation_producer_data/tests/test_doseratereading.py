"""
Test case for DoseRateReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eurdep_radiation_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading


class Test_DoseRateReading(unittest.TestCase):
    """
    Test case for DoseRateReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DoseRateReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DoseRateReading for testing
        """
        instance = DoseRateReading(
            station_id='bpewnnpkzrlidwjxuppr',
            name='euxjclfxsimaeagadoxz',
            value=float(22.046198415959882),
            unit='fnpbsrubeowndstpdhfo',
            start_measure='eifebfvfbjrabwedhtbe',
            end_measure='fyqwxobjqechoogddnpx',
            nuclide='pxymywqbjrmijzppeumm',
            duration='uysmtkksciipkajmkuun',
            validated=int(1),
            country='yfmtxbtumnzgxopgtegy'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bpewnnpkzrlidwjxuppr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'euxjclfxsimaeagadoxz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(22.046198415959882)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'fnpbsrubeowndstpdhfo'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_start_measure_property(self):
        """
        Test start_measure property
        """
        test_value = 'eifebfvfbjrabwedhtbe'
        self.instance.start_measure = test_value
        self.assertEqual(self.instance.start_measure, test_value)
    
    def test_end_measure_property(self):
        """
        Test end_measure property
        """
        test_value = 'fyqwxobjqechoogddnpx'
        self.instance.end_measure = test_value
        self.assertEqual(self.instance.end_measure, test_value)
    
    def test_nuclide_property(self):
        """
        Test nuclide property
        """
        test_value = 'pxymywqbjrmijzppeumm'
        self.instance.nuclide = test_value
        self.assertEqual(self.instance.nuclide, test_value)
    
    def test_duration_property(self):
        """
        Test duration property
        """
        test_value = 'uysmtkksciipkajmkuun'
        self.instance.duration = test_value
        self.assertEqual(self.instance.duration, test_value)
    
    def test_validated_property(self):
        """
        Test validated property
        """
        test_value = int(1)
        self.instance.validated = test_value
        self.assertEqual(self.instance.validated, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'yfmtxbtumnzgxopgtegy'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DoseRateReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DoseRateReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

