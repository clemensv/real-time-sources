"""
Test case for CurrentMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement

class Test_CurrentMeasurement(unittest.TestCase):
    """
    Test case for CurrentMeasurement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CurrentMeasurement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CurrentMeasurement for testing
        """
        instance = CurrentMeasurement(
            station_uuid='gsffydwifedxfpaopebq',
            timestamp='xmhsqrgkqrqwpvixvgbb',
            value=float(6.312102505425477),
            stateMnwMhw='scspspytmyexajpyvddy',
            stateNswHsw='ijbusiwibplvnhrqjbfx'
        )
        return instance

    
    def test_station_uuid_property(self):
        """
        Test station_uuid property
        """
        test_value = 'gsffydwifedxfpaopebq'
        self.instance.station_uuid = test_value
        self.assertEqual(self.instance.station_uuid, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'xmhsqrgkqrqwpvixvgbb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(6.312102505425477)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_stateMnwMhw_property(self):
        """
        Test stateMnwMhw property
        """
        test_value = 'scspspytmyexajpyvddy'
        self.instance.stateMnwMhw = test_value
        self.assertEqual(self.instance.stateMnwMhw, test_value)
    
    def test_stateNswHsw_property(self):
        """
        Test stateNswHsw property
        """
        test_value = 'ijbusiwibplvnhrqjbfx'
        self.instance.stateNswHsw = test_value
        self.assertEqual(self.instance.stateNswHsw, test_value)
    