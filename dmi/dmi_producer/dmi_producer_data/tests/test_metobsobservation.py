"""
Test case for MetObsObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.metobsobservation import MetObsObservation


class Test_MetObsObservation(unittest.TestCase):
    """
    Test case for MetObsObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MetObsObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MetObsObservation for testing
        """
        instance = MetObsObservation(
            observation_id='tpckpjlllzpbazchoukt',
            station_id='rzljgsmfivantlysnrgf',
            parameter_id='lkrqxubxoevnpneveaxd',
            observed='wizvluusxgdlbasyufpw',
            value=float(71.66578739703111),
            latitude=float(77.97059752243543),
            longitude=float(12.408786897222612)
        )
        return instance

    
    def test_observation_id_property(self):
        """
        Test observation_id property
        """
        test_value = 'tpckpjlllzpbazchoukt'
        self.instance.observation_id = test_value
        self.assertEqual(self.instance.observation_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rzljgsmfivantlysnrgf'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = 'lkrqxubxoevnpneveaxd'
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_observed_property(self):
        """
        Test observed property
        """
        test_value = 'wizvluusxgdlbasyufpw'
        self.instance.observed = test_value
        self.assertEqual(self.instance.observed, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(71.66578739703111)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(77.97059752243543)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(12.408786897222612)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MetObsObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MetObsObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

