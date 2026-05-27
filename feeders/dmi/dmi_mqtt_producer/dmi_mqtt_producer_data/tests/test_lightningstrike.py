"""
Test case for LightningStrike
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_mqtt_producer_data.lightningstrike import LightningStrike
import datetime


class Test_LightningStrike(unittest.TestCase):
    """
    Test case for LightningStrike
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LightningStrike.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LightningStrike for testing
        """
        instance = LightningStrike(
            strike_id='umaamttyjepvrwhuapuc',
            observed=datetime.datetime.now(datetime.timezone.utc),
            created=datetime.datetime.now(datetime.timezone.utc),
            type=int(33),
            amp=float(91.82665528864162),
            strokes=int(57),
            sensors='nfahutgwvxucpujynlzr',
            latitude=float(51.93553981184006),
            longitude=float(3.937811361554866)
        )
        return instance

    
    def test_strike_id_property(self):
        """
        Test strike_id property
        """
        test_value = 'umaamttyjepvrwhuapuc'
        self.instance.strike_id = test_value
        self.assertEqual(self.instance.strike_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = int(33)
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_amp_property(self):
        """
        Test amp property
        """
        test_value = float(91.82665528864162)
        self.instance.amp = test_value
        self.assertEqual(self.instance.amp, test_value)
    
    def test_strokes_property(self):
        """
        Test strokes property
        """
        test_value = int(57)
        self.instance.strokes = test_value
        self.assertEqual(self.instance.strokes, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = 'nfahutgwvxucpujynlzr'
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(51.93553981184006)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(3.937811361554866)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LightningStrike.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LightningStrike.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

