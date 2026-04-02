"""
Test case for Document
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_producer_data.kystverket_ais_producer_data.document import Document


class Test_Document(unittest.TestCase):
    """
    Test case for Document
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Document.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Document for testing
        """
        instance = Document(
            mmsi=int(75),
            imo_number=int(15),
            callsign='zlwflpymjpnpgdgzoxmm',
            ship_name='idciymilqaqpifwxeksa',
            ship_type=int(4),
            dimension_to_bow=int(85),
            dimension_to_stern=int(89),
            dimension_to_port=int(44),
            dimension_to_starboard=int(71),
            draught=float(78.08654437265497),
            destination='polvtuhfpmxpivdrmlkr',
            eta_month=int(34),
            eta_day=int(74),
            eta_hour=int(14),
            eta_minute=int(66),
            timestamp='wdfurwsxrsebwebnzpzf',
            station_id='ifysluvyfqasdnpefxmq'
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(75)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_imo_number_property(self):
        """
        Test imo_number property
        """
        test_value = int(15)
        self.instance.imo_number = test_value
        self.assertEqual(self.instance.imo_number, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'zlwflpymjpnpgdgzoxmm'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_ship_name_property(self):
        """
        Test ship_name property
        """
        test_value = 'idciymilqaqpifwxeksa'
        self.instance.ship_name = test_value
        self.assertEqual(self.instance.ship_name, test_value)
    
    def test_ship_type_property(self):
        """
        Test ship_type property
        """
        test_value = int(4)
        self.instance.ship_type = test_value
        self.assertEqual(self.instance.ship_type, test_value)
    
    def test_dimension_to_bow_property(self):
        """
        Test dimension_to_bow property
        """
        test_value = int(85)
        self.instance.dimension_to_bow = test_value
        self.assertEqual(self.instance.dimension_to_bow, test_value)
    
    def test_dimension_to_stern_property(self):
        """
        Test dimension_to_stern property
        """
        test_value = int(89)
        self.instance.dimension_to_stern = test_value
        self.assertEqual(self.instance.dimension_to_stern, test_value)
    
    def test_dimension_to_port_property(self):
        """
        Test dimension_to_port property
        """
        test_value = int(44)
        self.instance.dimension_to_port = test_value
        self.assertEqual(self.instance.dimension_to_port, test_value)
    
    def test_dimension_to_starboard_property(self):
        """
        Test dimension_to_starboard property
        """
        test_value = int(71)
        self.instance.dimension_to_starboard = test_value
        self.assertEqual(self.instance.dimension_to_starboard, test_value)
    
    def test_draught_property(self):
        """
        Test draught property
        """
        test_value = float(78.08654437265497)
        self.instance.draught = test_value
        self.assertEqual(self.instance.draught, test_value)
    
    def test_destination_property(self):
        """
        Test destination property
        """
        test_value = 'polvtuhfpmxpivdrmlkr'
        self.instance.destination = test_value
        self.assertEqual(self.instance.destination, test_value)
    
    def test_eta_month_property(self):
        """
        Test eta_month property
        """
        test_value = int(34)
        self.instance.eta_month = test_value
        self.assertEqual(self.instance.eta_month, test_value)
    
    def test_eta_day_property(self):
        """
        Test eta_day property
        """
        test_value = int(74)
        self.instance.eta_day = test_value
        self.assertEqual(self.instance.eta_day, test_value)
    
    def test_eta_hour_property(self):
        """
        Test eta_hour property
        """
        test_value = int(14)
        self.instance.eta_hour = test_value
        self.assertEqual(self.instance.eta_hour, test_value)
    
    def test_eta_minute_property(self):
        """
        Test eta_minute property
        """
        test_value = int(66)
        self.instance.eta_minute = test_value
        self.assertEqual(self.instance.eta_minute, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'wdfurwsxrsebwebnzpzf'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'ifysluvyfqasdnpefxmq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Document.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
