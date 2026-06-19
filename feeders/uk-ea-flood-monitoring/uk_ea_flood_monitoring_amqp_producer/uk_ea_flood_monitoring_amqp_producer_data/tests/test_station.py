"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_ea_flood_monitoring_amqp_producer_data.station import Station


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
            station_reference='bnxvhdwjyanhoprzexly',
            label='zixewibvqyhhlipezfvr',
            river_name='xskdusqbsazcyxsonpyd',
            catchment_name='jxdlymchydaapobdpfhy',
            town='wlieluiclawqwnwbbals',
            lat=float(7.397747013262879),
            long=float(69.47190529528895),
            notation='tbuzwcbkvhoeywulmxea',
            status='sgextluhblrhgrzpjbyv',
            date_opened='cpgvidclaejvornulgng',
            river='enqjzzvjzxagdtbbrdww'
        )
        return instance

    
    def test_station_reference_property(self):
        """
        Test station_reference property
        """
        test_value = 'bnxvhdwjyanhoprzexly'
        self.instance.station_reference = test_value
        self.assertEqual(self.instance.station_reference, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'zixewibvqyhhlipezfvr'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'xskdusqbsazcyxsonpyd'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_catchment_name_property(self):
        """
        Test catchment_name property
        """
        test_value = 'jxdlymchydaapobdpfhy'
        self.instance.catchment_name = test_value
        self.assertEqual(self.instance.catchment_name, test_value)
    
    def test_town_property(self):
        """
        Test town property
        """
        test_value = 'wlieluiclawqwnwbbals'
        self.instance.town = test_value
        self.assertEqual(self.instance.town, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(7.397747013262879)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(69.47190529528895)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_notation_property(self):
        """
        Test notation property
        """
        test_value = 'tbuzwcbkvhoeywulmxea'
        self.instance.notation = test_value
        self.assertEqual(self.instance.notation, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'sgextluhblrhgrzpjbyv'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_date_opened_property(self):
        """
        Test date_opened property
        """
        test_value = 'cpgvidclaejvornulgng'
        self.instance.date_opened = test_value
        self.assertEqual(self.instance.date_opened, test_value)
    
    def test_river_property(self):
        """
        Test river property
        """
        test_value = 'enqjzzvjzxagdtbbrdww'
        self.instance.river = test_value
        self.assertEqual(self.instance.river, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

