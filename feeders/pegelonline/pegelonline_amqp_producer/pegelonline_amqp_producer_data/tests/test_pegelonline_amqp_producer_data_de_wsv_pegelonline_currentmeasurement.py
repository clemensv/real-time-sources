"""
Test case for CurrentMeasurement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_amqp_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement


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
            station_id='fquxdlujljimnnnxlqkz',
            timestamp='eziagdubvxikwanfzrlq',
            value=float(83.90403927546558),
            stateMnwMhw='vrfijivjyvlrgsxgocrt',
            stateNswHsw='okelnllxyqlmvilyzlzl',
            trend=int(20)
        )
        return instance


    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'fquxdlujljimnnnxlqkz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)

    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'eziagdubvxikwanfzrlq'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)

    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(83.90403927546558)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)

    def test_stateMnwMhw_property(self):
        """
        Test stateMnwMhw property
        """
        test_value = 'vrfijivjyvlrgsxgocrt'
        self.instance.stateMnwMhw = test_value
        self.assertEqual(self.instance.stateMnwMhw, test_value)

    def test_stateNswHsw_property(self):
        """
        Test stateNswHsw property
        """
        test_value = 'okelnllxyqlmvilyzlzl'
        self.instance.stateNswHsw = test_value
        self.assertEqual(self.instance.stateNswHsw, test_value)

    def test_trend_property(self):
        """
        Test trend property
        """
        test_value = int(20)
        self.instance.trend = test_value
        self.assertEqual(self.instance.trend, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CurrentMeasurement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
