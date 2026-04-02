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
            station_id='hlxynmdlywnrzygysetc',
            dbc='fjxefkzezoyycnsuemhz',
            station_name='etgeqfukfedkkbbdpsgw',
            stream_name='jhfofylcflkjunamayye',
            latitude=float(88.72528211196608),
            longitude=float(63.6187675654032),
            flood_level_1=float(4.639688368090866),
            flood_level_2=float(2.555906138505948),
            flood_level_3=float(78.35427722703908),
            flood_level_4=float(79.38403275154316),
            has_forecast=True
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hlxynmdlywnrzygysetc'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_dbc_property(self):
        """
        Test dbc property
        """
        test_value = 'fjxefkzezoyycnsuemhz'
        self.instance.dbc = test_value
        self.assertEqual(self.instance.dbc, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'etgeqfukfedkkbbdpsgw'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_stream_name_property(self):
        """
        Test stream_name property
        """
        test_value = 'jhfofylcflkjunamayye'
        self.instance.stream_name = test_value
        self.assertEqual(self.instance.stream_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(88.72528211196608)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(63.6187675654032)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_flood_level_1_property(self):
        """
        Test flood_level_1 property
        """
        test_value = float(4.639688368090866)
        self.instance.flood_level_1 = test_value
        self.assertEqual(self.instance.flood_level_1, test_value)
    
    def test_flood_level_2_property(self):
        """
        Test flood_level_2 property
        """
        test_value = float(2.555906138505948)
        self.instance.flood_level_2 = test_value
        self.assertEqual(self.instance.flood_level_2, test_value)
    
    def test_flood_level_3_property(self):
        """
        Test flood_level_3 property
        """
        test_value = float(78.35427722703908)
        self.instance.flood_level_3 = test_value
        self.assertEqual(self.instance.flood_level_3, test_value)
    
    def test_flood_level_4_property(self):
        """
        Test flood_level_4 property
        """
        test_value = float(79.38403275154316)
        self.instance.flood_level_4 = test_value
        self.assertEqual(self.instance.flood_level_4, test_value)
    
    def test_has_forecast_property(self):
        """
        Test has_forecast property
        """
        test_value = True
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
