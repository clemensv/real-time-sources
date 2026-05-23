"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from smhi_hydro_mqtt_producer_data.station import Station


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
            station_id='dllmtecasmivdwynktrk',
            name='psdrwaggpeshznoqrjqs',
            owner='hjlwbclhgbbbrpuaogtd',
            measuring_stations='joejsjzaavsjourmalnr',
            region=int(26),
            catchment_name='txejrkhihljdnnkwutaz',
            catchment_number=int(43),
            catchment_size=float(51.46192597028716),
            latitude=float(94.32912478036232),
            longitude=float(82.27770438208032)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'dllmtecasmivdwynktrk'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'psdrwaggpeshznoqrjqs'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'hjlwbclhgbbbrpuaogtd'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_measuring_stations_property(self):
        """
        Test measuring_stations property
        """
        test_value = 'joejsjzaavsjourmalnr'
        self.instance.measuring_stations = test_value
        self.assertEqual(self.instance.measuring_stations, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = int(26)
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_catchment_name_property(self):
        """
        Test catchment_name property
        """
        test_value = 'txejrkhihljdnnkwutaz'
        self.instance.catchment_name = test_value
        self.assertEqual(self.instance.catchment_name, test_value)
    
    def test_catchment_number_property(self):
        """
        Test catchment_number property
        """
        test_value = int(43)
        self.instance.catchment_number = test_value
        self.assertEqual(self.instance.catchment_number, test_value)
    
    def test_catchment_size_property(self):
        """
        Test catchment_size property
        """
        test_value = float(51.46192597028716)
        self.instance.catchment_size = test_value
        self.assertEqual(self.instance.catchment_size, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(94.32912478036232)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(82.27770438208032)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
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

