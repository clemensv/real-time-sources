"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from defra_aurn_producer_data.uk.gov.defra.aurn.observation import Observation


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            timeseries_id='anietwnozszpxsrldedt',
            timestamp='rafyjxyorosevjtftyzr',
            value=float(42.35961558899209),
            uom='sbwajxgjhwetokwephqr'
        )
        return instance

    
    def test_timeseries_id_property(self):
        """
        Test timeseries_id property
        """
        test_value = 'anietwnozszpxsrldedt'
        self.instance.timeseries_id = test_value
        self.assertEqual(self.instance.timeseries_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'rafyjxyorosevjtftyzr'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(42.35961558899209)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_uom_property(self):
        """
        Test uom property
        """
        test_value = 'sbwajxgjhwetokwephqr'
        self.instance.uom = test_value
        self.assertEqual(self.instance.uom, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
