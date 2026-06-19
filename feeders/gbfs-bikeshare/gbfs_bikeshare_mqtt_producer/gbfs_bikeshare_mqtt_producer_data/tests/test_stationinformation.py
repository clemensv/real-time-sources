"""
Test case for StationInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gbfs_bikeshare_mqtt_producer_data.stationinformation import StationInformation


class Test_StationInformation(unittest.TestCase):
    """
    Test case for StationInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_StationInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of StationInformation for testing
        """
        instance = StationInformation(
            system_id='coeywxrdboyvihlmdpqk',
            station_id='rarbviwxvyegjjscrsxq',
            name='xxzxpwdxskkxzxrtvlmq',
            short_name='dlposyeacmzrrpnhzzju',
            lat=float(11.387190629324373),
            lon=float(49.03523419466621),
            capacity=int(26),
            region_id='ocrkdruyuqqbtonatrla',
            address='hyocrllegyiayivmfewz',
            post_code='cixstiuvdphyawutfsat'
        )
        return instance

    
    def test_system_id_property(self):
        """
        Test system_id property
        """
        test_value = 'coeywxrdboyvihlmdpqk'
        self.instance.system_id = test_value
        self.assertEqual(self.instance.system_id, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'rarbviwxvyegjjscrsxq'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xxzxpwdxskkxzxrtvlmq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_short_name_property(self):
        """
        Test short_name property
        """
        test_value = 'dlposyeacmzrrpnhzzju'
        self.instance.short_name = test_value
        self.assertEqual(self.instance.short_name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(11.387190629324373)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(49.03523419466621)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_capacity_property(self):
        """
        Test capacity property
        """
        test_value = int(26)
        self.instance.capacity = test_value
        self.assertEqual(self.instance.capacity, test_value)
    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'ocrkdruyuqqbtonatrla'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'hyocrllegyiayivmfewz'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_post_code_property(self):
        """
        Test post_code property
        """
        test_value = 'cixstiuvdphyawutfsat'
        self.instance.post_code = test_value
        self.assertEqual(self.instance.post_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = StationInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = StationInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

