"""
Test case for Timeseries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irceline_belgium_producer_data.be.irceline.timeseries import Timeseries
from test_irceline_belgium_producer_data_be_irceline_statusinterval import Test_StatusInterval


class Test_Timeseries(unittest.TestCase):
    """
    Test case for Timeseries
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Timeseries.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Timeseries for testing
        """
        instance = Timeseries(
            timeseries_id='amkwkhzlwpncqcvujwlm',
            label='hrhruorpzxuvughbhreo',
            uom='czkbvnjggsodkyojwaoo',
            station_id='erqcnnqdeedgsrmlgklv',
            station_label='guwlcmwkucsutvmqivcn',
            latitude=float(18.270973328215778),
            longitude=float(83.9799306010969),
            phenomenon_id='ydsldhpblmxxhunowkyz',
            phenomenon_label='gsikiazofimdhstqswdb',
            category_id='wtdncdsgqiqnlmzpruex',
            category_label='jfctegmxxtfrnerefhwq',
            status_intervals=[Test_StatusInterval.create_instance(), Test_StatusInterval.create_instance()]
        )
        return instance

    
    def test_timeseries_id_property(self):
        """
        Test timeseries_id property
        """
        test_value = 'amkwkhzlwpncqcvujwlm'
        self.instance.timeseries_id = test_value
        self.assertEqual(self.instance.timeseries_id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'hrhruorpzxuvughbhreo'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_uom_property(self):
        """
        Test uom property
        """
        test_value = 'czkbvnjggsodkyojwaoo'
        self.instance.uom = test_value
        self.assertEqual(self.instance.uom, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'erqcnnqdeedgsrmlgklv'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_label_property(self):
        """
        Test station_label property
        """
        test_value = 'guwlcmwkucsutvmqivcn'
        self.instance.station_label = test_value
        self.assertEqual(self.instance.station_label, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(18.270973328215778)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(83.9799306010969)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_phenomenon_id_property(self):
        """
        Test phenomenon_id property
        """
        test_value = 'ydsldhpblmxxhunowkyz'
        self.instance.phenomenon_id = test_value
        self.assertEqual(self.instance.phenomenon_id, test_value)
    
    def test_phenomenon_label_property(self):
        """
        Test phenomenon_label property
        """
        test_value = 'gsikiazofimdhstqswdb'
        self.instance.phenomenon_label = test_value
        self.assertEqual(self.instance.phenomenon_label, test_value)
    
    def test_category_id_property(self):
        """
        Test category_id property
        """
        test_value = 'wtdncdsgqiqnlmzpruex'
        self.instance.category_id = test_value
        self.assertEqual(self.instance.category_id, test_value)
    
    def test_category_label_property(self):
        """
        Test category_label property
        """
        test_value = 'jfctegmxxtfrnerefhwq'
        self.instance.category_label = test_value
        self.assertEqual(self.instance.category_label, test_value)
    
    def test_status_intervals_property(self):
        """
        Test status_intervals property
        """
        test_value = [Test_StatusInterval.create_instance(), Test_StatusInterval.create_instance()]
        self.instance.status_intervals = test_value
        self.assertEqual(self.instance.status_intervals, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Timeseries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
