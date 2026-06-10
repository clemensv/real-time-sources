"""
Test case for LightningStroke
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from blitzortung_producer_data.lightningstroke import LightningStroke
from blitzortung_producer_data.detectorparticipation import DetectorParticipation


class Test_LightningStroke(unittest.TestCase):
    """
    Test case for LightningStroke
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LightningStroke.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LightningStroke for testing
        """
        instance = LightningStroke(
            source_id=int(63),
            stroke_id='dvagnwwfvxsnlwxnscfz',
            event_time='lymzdzrgavogoyncddhh',
            event_timestamp_ms=int(71),
            latitude=float(20.374491001085293),
            longitude=float(29.262299168623873),
            server_id=int(59),
            server_delay_ms=int(99),
            accuracy_diameter_m=float(62.28910612277869),
            detector_participations=[None, None, None],
            geohash5='xtblvbnvioglenxytjrc',
            geohash7='bhiqrtqctfcemqyiofpq'
        )
        return instance

    
    def test_source_id_property(self):
        """
        Test source_id property
        """
        test_value = int(63)
        self.instance.source_id = test_value
        self.assertEqual(self.instance.source_id, test_value)
    
    def test_stroke_id_property(self):
        """
        Test stroke_id property
        """
        test_value = 'dvagnwwfvxsnlwxnscfz'
        self.instance.stroke_id = test_value
        self.assertEqual(self.instance.stroke_id, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'lymzdzrgavogoyncddhh'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_event_timestamp_ms_property(self):
        """
        Test event_timestamp_ms property
        """
        test_value = int(71)
        self.instance.event_timestamp_ms = test_value
        self.assertEqual(self.instance.event_timestamp_ms, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(20.374491001085293)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(29.262299168623873)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_server_id_property(self):
        """
        Test server_id property
        """
        test_value = int(59)
        self.instance.server_id = test_value
        self.assertEqual(self.instance.server_id, test_value)
    
    def test_server_delay_ms_property(self):
        """
        Test server_delay_ms property
        """
        test_value = int(99)
        self.instance.server_delay_ms = test_value
        self.assertEqual(self.instance.server_delay_ms, test_value)
    
    def test_accuracy_diameter_m_property(self):
        """
        Test accuracy_diameter_m property
        """
        test_value = float(62.28910612277869)
        self.instance.accuracy_diameter_m = test_value
        self.assertEqual(self.instance.accuracy_diameter_m, test_value)
    
    def test_detector_participations_property(self):
        """
        Test detector_participations property
        """
        test_value = [None, None, None]
        self.instance.detector_participations = test_value
        self.assertEqual(self.instance.detector_participations, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'xtblvbnvioglenxytjrc'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_geohash7_property(self):
        """
        Test geohash7 property
        """
        test_value = 'bhiqrtqctfcemqyiofpq'
        self.instance.geohash7 = test_value
        self.assertEqual(self.instance.geohash7, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LightningStroke.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LightningStroke.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

