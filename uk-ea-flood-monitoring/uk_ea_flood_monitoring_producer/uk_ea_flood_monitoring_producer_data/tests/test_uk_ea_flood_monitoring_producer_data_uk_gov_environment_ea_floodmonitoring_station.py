"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_ea_flood_monitoring_producer_data.uk.gov.environment.ea.floodmonitoring.station import Station


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            station_reference='nimncrtvonqmymyiukpe',
            label='tnfbthcmnfdkfujusjrn',
            river_name='aqufllmtkpuivxyqgmmu',
            catchment_name='csdxtvwwhppfgljwpohm',
            town='wfxvqujeqstbqstxecla',
            lat=float(62.133854678827404),
            long=float(88.01967547557142),
            notation='yvcfyajsywsbxuejykkf',
            status='jalbhkpqvuvneotmzxfl',
            date_opened='sgqgxqscabzuqcdefuch'
        )
        return instance

    
    def test_station_reference_property(self):
        """
        Test station_reference property
        """
        test_value = 'nimncrtvonqmymyiukpe'
        self.instance.station_reference = test_value
        self.assertEqual(self.instance.station_reference, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'tnfbthcmnfdkfujusjrn'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'aqufllmtkpuivxyqgmmu'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_catchment_name_property(self):
        """
        Test catchment_name property
        """
        test_value = 'csdxtvwwhppfgljwpohm'
        self.instance.catchment_name = test_value
        self.assertEqual(self.instance.catchment_name, test_value)
    
    def test_town_property(self):
        """
        Test town property
        """
        test_value = 'wfxvqujeqstbqstxecla'
        self.instance.town = test_value
        self.assertEqual(self.instance.town, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(62.133854678827404)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(88.01967547557142)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_notation_property(self):
        """
        Test notation property
        """
        test_value = 'yvcfyajsywsbxuejykkf'
        self.instance.notation = test_value
        self.assertEqual(self.instance.notation, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'jalbhkpqvuvneotmzxfl'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_date_opened_property(self):
        """
        Test date_opened property
        """
        test_value = 'sgqgxqscabzuqcdefuch'
        self.instance.date_opened = test_value
        self.assertEqual(self.instance.date_opened, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
