"""
Test case for FireDetection
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nasa_firms_mqtt_producer_data.nasa.firms.firedetection import FireDetection
from nasa_firms_mqtt_producer_data.nasa.firms.instrumentenum import InstrumentEnum
from nasa_firms_mqtt_producer_data.nasa.firms.daynightenum import DaynightEnum
from nasa_firms_mqtt_producer_data.nasa.firms.confidencelevelenum import ConfidenceLevelenum
import datetime


class Test_FireDetection(unittest.TestCase):
    """
    Test case for FireDetection
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FireDetection.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FireDetection for testing
        """
        instance = FireDetection(
            source='iwehfxptqeqivgolnpcd',
            record_id='anzwhjcbpozgpkpleesn',
            latitude=float(44.616716071535),
            longitude=float(75.36401139217513),
            brightness=float(48.423711266995326),
            bright_t31=float(40.326654468511435),
            bright_ti4=float(82.95615729267455),
            bright_ti5=float(71.42472540297446),
            scan=float(68.14145042587138),
            track=float(59.122994905347795),
            acq_date=datetime.date.today(),
            acq_time='tbdkvjxtwyunejsapmfx',
            acq_datetime=datetime.datetime.now(datetime.timezone.utc),
            satellite='sgzghkhipnzwwdgybgqs',
            instrument=InstrumentEnum.VIIRS,
            confidence='jcxgbuqsutedrhxhtado',
            confidence_level=ConfidenceLevelenum.low,
            version='czhghdhjsevmdglrsmsd',
            frp=float(97.72707133774222),
            daynight=DaynightEnum.D,
            tile='cbzgvnmlndomvytpulap'
        )
        return instance

    
    def test_source_property(self):
        """
        Test source property
        """
        test_value = 'iwehfxptqeqivgolnpcd'
        self.instance.source = test_value
        self.assertEqual(self.instance.source, test_value)
    
    def test_record_id_property(self):
        """
        Test record_id property
        """
        test_value = 'anzwhjcbpozgpkpleesn'
        self.instance.record_id = test_value
        self.assertEqual(self.instance.record_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(44.616716071535)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(75.36401139217513)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_brightness_property(self):
        """
        Test brightness property
        """
        test_value = float(48.423711266995326)
        self.instance.brightness = test_value
        self.assertEqual(self.instance.brightness, test_value)
    
    def test_bright_t31_property(self):
        """
        Test bright_t31 property
        """
        test_value = float(40.326654468511435)
        self.instance.bright_t31 = test_value
        self.assertEqual(self.instance.bright_t31, test_value)
    
    def test_bright_ti4_property(self):
        """
        Test bright_ti4 property
        """
        test_value = float(82.95615729267455)
        self.instance.bright_ti4 = test_value
        self.assertEqual(self.instance.bright_ti4, test_value)
    
    def test_bright_ti5_property(self):
        """
        Test bright_ti5 property
        """
        test_value = float(71.42472540297446)
        self.instance.bright_ti5 = test_value
        self.assertEqual(self.instance.bright_ti5, test_value)
    
    def test_scan_property(self):
        """
        Test scan property
        """
        test_value = float(68.14145042587138)
        self.instance.scan = test_value
        self.assertEqual(self.instance.scan, test_value)
    
    def test_track_property(self):
        """
        Test track property
        """
        test_value = float(59.122994905347795)
        self.instance.track = test_value
        self.assertEqual(self.instance.track, test_value)
    
    def test_acq_date_property(self):
        """
        Test acq_date property
        """
        test_value = datetime.date.today()
        self.instance.acq_date = test_value
        self.assertEqual(self.instance.acq_date, test_value)
    
    def test_acq_time_property(self):
        """
        Test acq_time property
        """
        test_value = 'tbdkvjxtwyunejsapmfx'
        self.instance.acq_time = test_value
        self.assertEqual(self.instance.acq_time, test_value)
    
    def test_acq_datetime_property(self):
        """
        Test acq_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.acq_datetime = test_value
        self.assertEqual(self.instance.acq_datetime, test_value)
    
    def test_satellite_property(self):
        """
        Test satellite property
        """
        test_value = 'sgzghkhipnzwwdgybgqs'
        self.instance.satellite = test_value
        self.assertEqual(self.instance.satellite, test_value)
    
    def test_instrument_property(self):
        """
        Test instrument property
        """
        test_value = InstrumentEnum.VIIRS
        self.instance.instrument = test_value
        self.assertEqual(self.instance.instrument, test_value)
    
    def test_confidence_property(self):
        """
        Test confidence property
        """
        test_value = 'jcxgbuqsutedrhxhtado'
        self.instance.confidence = test_value
        self.assertEqual(self.instance.confidence, test_value)
    
    def test_confidence_level_property(self):
        """
        Test confidence_level property
        """
        test_value = ConfidenceLevelenum.low
        self.instance.confidence_level = test_value
        self.assertEqual(self.instance.confidence_level, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'czhghdhjsevmdglrsmsd'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_frp_property(self):
        """
        Test frp property
        """
        test_value = float(97.72707133774222)
        self.instance.frp = test_value
        self.assertEqual(self.instance.frp, test_value)
    
    def test_daynight_property(self):
        """
        Test daynight property
        """
        test_value = DaynightEnum.D
        self.instance.daynight = test_value
        self.assertEqual(self.instance.daynight, test_value)
    
    def test_tile_property(self):
        """
        Test tile property
        """
        test_value = 'cbzgvnmlndomvytpulap'
        self.instance.tile = test_value
        self.assertEqual(self.instance.tile, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FireDetection.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FireDetection.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

