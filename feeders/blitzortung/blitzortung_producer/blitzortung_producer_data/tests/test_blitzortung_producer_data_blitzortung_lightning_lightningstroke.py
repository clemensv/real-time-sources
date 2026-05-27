"""
Test case for LightningStroke
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from blitzortung_producer_data.blitzortung.lightning.lightningstroke import LightningStroke
from test_blitzortung_producer_data_blitzortung_lightning_detectorparticipation import Test_DetectorParticipation


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
            source_id=int(14),
            stroke_id='focexorsemkqvgpyrxtx',
            event_time='kqsgsgnntgzichqbczmy',
            event_timestamp_ms=int(70),
            latitude=float(86.22120537787853),
            longitude=float(2.1778084001723985),
            geohash5='lxembbsvnjknhnfdfnwn',
            geohash7='wxjmscxqqmzoblkipnig',
            server_id=int(84),
            server_delay_ms=int(43),
            accuracy_diameter_m=float(68.67678849746014),
            detector_participations=[Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance()]
        )
        return instance

    
    def test_source_id_property(self):
        """
        Test source_id property
        """
        test_value = int(14)
        self.instance.source_id = test_value
        self.assertEqual(self.instance.source_id, test_value)
    
    def test_stroke_id_property(self):
        """
        Test stroke_id property
        """
        test_value = 'focexorsemkqvgpyrxtx'
        self.instance.stroke_id = test_value
        self.assertEqual(self.instance.stroke_id, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'kqsgsgnntgzichqbczmy'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_event_timestamp_ms_property(self):
        """
        Test event_timestamp_ms property
        """
        test_value = int(70)
        self.instance.event_timestamp_ms = test_value
        self.assertEqual(self.instance.event_timestamp_ms, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(86.22120537787853)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(2.1778084001723985)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_geohash5_property(self):
        """
        Test geohash5 property
        """
        test_value = 'lxembbsvnjknhnfdfnwn'
        self.instance.geohash5 = test_value
        self.assertEqual(self.instance.geohash5, test_value)
    
    def test_geohash7_property(self):
        """
        Test geohash7 property
        """
        test_value = 'wxjmscxqqmzoblkipnig'
        self.instance.geohash7 = test_value
        self.assertEqual(self.instance.geohash7, test_value)
    
    def test_server_id_property(self):
        """
        Test server_id property
        """
        test_value = int(84)
        self.instance.server_id = test_value
        self.assertEqual(self.instance.server_id, test_value)
    
    def test_server_delay_ms_property(self):
        """
        Test server_delay_ms property
        """
        test_value = int(43)
        self.instance.server_delay_ms = test_value
        self.assertEqual(self.instance.server_delay_ms, test_value)
    
    def test_accuracy_diameter_m_property(self):
        """
        Test accuracy_diameter_m property
        """
        test_value = float(68.67678849746014)
        self.instance.accuracy_diameter_m = test_value
        self.assertEqual(self.instance.accuracy_diameter_m, test_value)
    
    def test_detector_participations_property(self):
        """
        Test detector_participations property
        """
        test_value = [Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance(), Test_DetectorParticipation.create_instance()]
        self.instance.detector_participations = test_value
        self.assertEqual(self.instance.detector_participations, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LightningStroke.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
