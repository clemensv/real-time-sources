"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from smhi_weather_producer_data.station import Station


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
            station_id='bmfviebttismslvwvibr',
            name='fgwuugycagiadvekcldd',
            owner='ysvrklckmlmxqjuofboo',
            owner_category='zzvudbvpsylquklwqcul',
            measuring_stations='kdptxmroymgvwduwzehq',
            height=float(27.366626382154568),
            latitude=float(70.30924218573045),
            longitude=float(87.62634493315437),
            lan='mgawkbydbzdtxvcyqvfi'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'bmfviebttismslvwvibr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'fgwuugycagiadvekcldd'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'ysvrklckmlmxqjuofboo'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_owner_category_property(self):
        """
        Test owner_category property
        """
        test_value = 'zzvudbvpsylquklwqcul'
        self.instance.owner_category = test_value
        self.assertEqual(self.instance.owner_category, test_value)
    
    def test_measuring_stations_property(self):
        """
        Test measuring_stations property
        """
        test_value = 'kdptxmroymgvwduwzehq'
        self.instance.measuring_stations = test_value
        self.assertEqual(self.instance.measuring_stations, test_value)
    
    def test_height_property(self):
        """
        Test height property
        """
        test_value = float(27.366626382154568)
        self.instance.height = test_value
        self.assertEqual(self.instance.height, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(70.30924218573045)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(87.62634493315437)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_lan_property(self):
        """
        Test lan property
        """
        test_value = 'mgawkbydbzdtxvcyqvfi'
        self.instance.lan = test_value
        self.assertEqual(self.instance.lan, test_value)
    
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

