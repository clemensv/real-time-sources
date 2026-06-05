"""
Test case for TidewaterPrediction
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.tidewaterprediction import TidewaterPrediction
import datetime


class Test_TidewaterPrediction(unittest.TestCase):
    """
    Test case for TidewaterPrediction
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TidewaterPrediction.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TidewaterPrediction for testing
        """
        instance = TidewaterPrediction(
            prediction_id='nwiwkoodmkqcznooivto',
            station_id='mvvwgkihdjezbvasvoiw',
            prediction_type='oexzrhxluawkymblztlv',
            prediction_time=datetime.datetime.now(datetime.timezone.utc),
            value=float(59.676097127409896),
            latitude=float(15.784246603413976),
            longitude=float(6.5329988926361215)
        )
        return instance

    
    def test_prediction_id_property(self):
        """
        Test prediction_id property
        """
        test_value = 'nwiwkoodmkqcznooivto'
        self.instance.prediction_id = test_value
        self.assertEqual(self.instance.prediction_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'mvvwgkihdjezbvasvoiw'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_prediction_type_property(self):
        """
        Test prediction_type property
        """
        test_value = 'oexzrhxluawkymblztlv'
        self.instance.prediction_type = test_value
        self.assertEqual(self.instance.prediction_type, test_value)
    
    def test_prediction_time_property(self):
        """
        Test prediction_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.prediction_time = test_value
        self.assertEqual(self.instance.prediction_time, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(59.676097127409896)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(15.784246603413976)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(6.5329988926361215)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TidewaterPrediction.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TidewaterPrediction.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

