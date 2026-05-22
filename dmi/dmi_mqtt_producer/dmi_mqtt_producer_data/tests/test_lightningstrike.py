"""
Test case for LightningStrike
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_mqtt_producer_data.lightningstrike import LightningStrike


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
            strike_id='tzhcduljifkfxlrcseku',
            observed='dppwutpshhzavzfsgukk',
            created='hynncxwpeudpvystgxjv',
            type=int(33),
            amp=float(72.95927211850322),
            strokes=int(42),
            sensors='vdybqyhmtdssnqfgqkeo',
            latitude=float(10.468950888203366),
            longitude=float(47.7251661382302)
        )
        return instance

    
    def test_strike_id_property(self):
        """
        Test strike_id property
        """
        test_value = 'tzhcduljifkfxlrcseku'
        self.instance.strike_id = test_value
        self.assertEqual(self.instance.strike_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = 'dppwutpshhzavzfsgukk'
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'hynncxwpeudpvystgxjv'
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
        test_value = float(72.95927211850322)
        self.instance.amp = test_value
        self.assertEqual(self.instance.amp, test_value)
    
    def test_strokes_property(self):
        """
        Test strokes property
        """
        test_value = int(42)
        self.instance.strokes = test_value
        self.assertEqual(self.instance.strokes, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = 'vdybqyhmtdssnqfgqkeo'
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(10.468950888203366)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(47.7251661382302)
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

