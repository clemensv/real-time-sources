"""
Test case for StaticVoyageData
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.no.kystverket.ais.staticvoyagedata import StaticVoyageData


class Test_StaticVoyageData(unittest.TestCase):
    """
    Test case for StaticVoyageData
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StaticVoyageData.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StaticVoyageData for testing
        """
        instance = StaticVoyageData(
            mmsi=int(61),
            imo_number=int(84),
            callsign='qeqghsuzscgyuzxvsubc',
            ship_name='recjeugegoafjzxoliyl',
            ship_type=int(14),
            dimension_to_bow=int(82),
            dimension_to_stern=int(33),
            dimension_to_port=int(55),
            dimension_to_starboard=int(1),
            draught=float(91.71277483073095),
            destination='klpniutmsrazhvpuyxpx',
            eta_month=int(6),
            eta_day=int(43),
            eta_hour=int(0),
            eta_minute=int(95),
            timestamp='mgmlzuzobvrwjhukrqhb',
            station_id='jdxhfsyjklzudhjmlpqy'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(61)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(84)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'qeqghsuzscgyuzxvsubc'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'recjeugegoafjzxoliyl'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = int(14)
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_dimension_to_bow_property(self):
        """
        Test dimension_to_bow property
        """
        test_value = int(82)
        self.instance.dimension_to_bow = test_value
        self.assertEqual(self.instance.dimension_to_bow, test_value)
    
    def test_dimension_to_stern_property(self):
        """
        Test dimension_to_stern property
        """
        test_value = int(33)
        self.instance.dimension_to_stern = test_value
        self.assertEqual(self.instance.dimension_to_stern, test_value)
    
    def test_dimension_to_port_property(self):
        """
        Test dimension_to_port property
        """
        test_value = int(55)
        self.instance.dimension_to_port = test_value
        self.assertEqual(self.instance.dimension_to_port, test_value)
    
    def test_dimension_to_starboard_property(self):
        """
        Test dimension_to_starboard property
        """
        test_value = int(1)
        self.instance.dimension_to_starboard = test_value
        self.assertEqual(self.instance.dimension_to_starboard, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(91.71277483073095)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'klpniutmsrazhvpuyxpx'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_month_property(self):
        """
        Test eta_month property
        """
        test_value = int(6)
        self.instance.eta_month = test_value
        self.assertEqual(self.instance.eta_month, test_value)
    
    def test_eta_day_property(self):
        """
        Test eta_day property
        """
        test_value = int(43)
        self.instance.eta_day = test_value
        self.assertEqual(self.instance.eta_day, test_value)
    
    def test_eta_hour_property(self):
        """
        Test eta_hour property
        """
        test_value = int(0)
        self.instance.eta_hour = test_value
        self.assertEqual(self.instance.eta_hour, test_value)
    
    def test_eta_minute_property(self):
        """
        Test eta_minute property
        """
        test_value = int(95)
        self.instance.eta_minute = test_value
        self.assertEqual(self.instance.eta_minute, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'mgmlzuzobvrwjhukrqhb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jdxhfsyjklzudhjmlpqy'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StaticVoyageData.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
