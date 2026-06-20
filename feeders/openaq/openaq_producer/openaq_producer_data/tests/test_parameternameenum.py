import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from openaq_producer_data.org.openaq.parameternameenum import ParameterNameenum


class Test_ParameterNameenum(unittest.TestCase):
    """
    Test case for ParameterNameenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ParameterNameenum.pm25

    @staticmethod
    def create_instance():
        """
        Create instance of ParameterNameenum
        """
        return ParameterNameenum.pm25

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ParameterNameenum.pm25.value, 'pm25')
        self.assertEqual(ParameterNameenum.pm10.value, 'pm10')
        self.assertEqual(ParameterNameenum.o3.value, 'o3')
        self.assertEqual(ParameterNameenum.no2.value, 'no2')
        self.assertEqual(ParameterNameenum.so2.value, 'so2')
        self.assertEqual(ParameterNameenum.co.value, 'co')
        self.assertEqual(ParameterNameenum.bc.value, 'bc')
        self.assertEqual(ParameterNameenum.no.value, 'no')
        self.assertEqual(ParameterNameenum.nox.value, 'nox')
        self.assertEqual(ParameterNameenum.pm1.value, 'pm1')
        self.assertEqual(ParameterNameenum.co2.value, 'co2')
        self.assertEqual(ParameterNameenum.temperature.value, 'temperature')
        self.assertEqual(ParameterNameenum.relativehumidity.value, 'relativehumidity')
        self.assertEqual(ParameterNameenum.pressure.value, 'pressure')
        self.assertEqual(ParameterNameenum.windspeed.value, 'windspeed')
        self.assertEqual(ParameterNameenum.winddirection.value, 'winddirection')
        self.assertEqual(ParameterNameenum.um003.value, 'um003')
        self.assertEqual(ParameterNameenum.um005.value, 'um005')
        self.assertEqual(ParameterNameenum.um010.value, 'um010')
        self.assertEqual(ParameterNameenum.um025.value, 'um025')
        self.assertEqual(ParameterNameenum.um050.value, 'um050')
        self.assertEqual(ParameterNameenum.um100.value, 'um100')