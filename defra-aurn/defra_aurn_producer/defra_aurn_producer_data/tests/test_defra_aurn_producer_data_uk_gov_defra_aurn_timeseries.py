"""
Test case for Timeseries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from defra_aurn_producer_data.uk.gov.defra.aurn.timeseries import Timeseries


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
            timeseries_id='uhomhdskuttrxtthhrpd',
            label='xfkqlcoedzwtijxdpuef',
            uom='yrzdxffbbdmmzlhbeuhh',
            station_id='cavnybthcucaxnltcfog',
            station_label='xwnxmfnqhmqgwuoevuxx',
            latitude=float(80.6893421151271),
            longitude=float(42.82650734755531),
            phenomenon_id='otwgtdbcyfewtsybsykl',
            phenomenon_label='ovlszquxojuggjvyjzuk',
            category_id='wxahkabngfmeriskgkdb',
            category_label='iuymowadlkaieubmhwgj'
        )
        return instance

    
    def test_timeseries_id_property(self):
        """
        Test timeseries_id property
        """
        test_value = 'uhomhdskuttrxtthhrpd'
        self.instance.timeseries_id = test_value
        self.assertEqual(self.instance.timeseries_id, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'xfkqlcoedzwtijxdpuef'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_uom_property(self):
        """
        Test uom property
        """
        test_value = 'yrzdxffbbdmmzlhbeuhh'
        self.instance.uom = test_value
        self.assertEqual(self.instance.uom, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'cavnybthcucaxnltcfog'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_label_property(self):
        """
        Test station_label property
        """
        test_value = 'xwnxmfnqhmqgwuoevuxx'
        self.instance.station_label = test_value
        self.assertEqual(self.instance.station_label, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(80.6893421151271)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(42.82650734755531)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_phenomenon_id_property(self):
        """
        Test phenomenon_id property
        """
        test_value = 'otwgtdbcyfewtsybsykl'
        self.instance.phenomenon_id = test_value
        self.assertEqual(self.instance.phenomenon_id, test_value)
    
    def test_phenomenon_label_property(self):
        """
        Test phenomenon_label property
        """
        test_value = 'ovlszquxojuggjvyjzuk'
        self.instance.phenomenon_label = test_value
        self.assertEqual(self.instance.phenomenon_label, test_value)
    
    def test_category_id_property(self):
        """
        Test category_id property
        """
        test_value = 'wxahkabngfmeriskgkdb'
        self.instance.category_id = test_value
        self.assertEqual(self.instance.category_id, test_value)
    
    def test_category_label_property(self):
        """
        Test category_label property
        """
        test_value = 'iuymowadlkaieubmhwgj'
        self.instance.category_label = test_value
        self.assertEqual(self.instance.category_label, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Timeseries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
