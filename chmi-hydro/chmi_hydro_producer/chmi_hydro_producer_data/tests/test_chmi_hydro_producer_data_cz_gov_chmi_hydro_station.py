"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from chmi_hydro_producer_data.cz.gov.chmi.hydro.station import Station


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
            station_id='cqclnfvxfiezgafcrztg',
            dbc='scrcaeppnliijpuabwet',
            station_name='ohqxrhsxpdljynnqkblv',
            stream_name='umbhrionuvpjncfgjjpd',
            latitude=float(99.70124437344256),
            longitude=float(83.89466141875438),
            flood_level_1=float(9.456344707822439),
            flood_level_2=float(58.90695014106758),
            flood_level_3=float(82.05243304544815),
            flood_level_4=float(69.13328716449031),
            has_forecast=False
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'cqclnfvxfiezgafcrztg'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_dbc_property(self):
        """
        Test dbc property
        """
        test_value = 'scrcaeppnliijpuabwet'
        self.instance.dbc = test_value
        self.assertEqual(self.instance.dbc, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'ohqxrhsxpdljynnqkblv'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_stream_name_property(self):
        """
        Test stream_name property
        """
        test_value = 'umbhrionuvpjncfgjjpd'
        self.instance.stream_name = test_value
        self.assertEqual(self.instance.stream_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(99.70124437344256)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(83.89466141875438)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_flood_level_1_property(self):
        """
        Test flood_level_1 property
        """
        test_value = float(9.456344707822439)
        self.instance.flood_level_1 = test_value
        self.assertEqual(self.instance.flood_level_1, test_value)
    
    def test_flood_level_2_property(self):
        """
        Test flood_level_2 property
        """
        test_value = float(58.90695014106758)
        self.instance.flood_level_2 = test_value
        self.assertEqual(self.instance.flood_level_2, test_value)
    
    def test_flood_level_3_property(self):
        """
        Test flood_level_3 property
        """
        test_value = float(82.05243304544815)
        self.instance.flood_level_3 = test_value
        self.assertEqual(self.instance.flood_level_3, test_value)
    
    def test_flood_level_4_property(self):
        """
        Test flood_level_4 property
        """
        test_value = float(69.13328716449031)
        self.instance.flood_level_4 = test_value
        self.assertEqual(self.instance.flood_level_4, test_value)
    
    def test_has_forecast_property(self):
        """
        Test has_forecast property
        """
        test_value = False
        self.instance.has_forecast = test_value
        self.assertEqual(self.instance.has_forecast, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
