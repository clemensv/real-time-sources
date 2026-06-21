"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kiwis_amqp_producer_data.station import Station


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
            kiwis_id='umgeftqqbyxktjqjrppz',
            base_url='ondtmdjgnfvtudnllugo',
            station_id='zzsjuoqxnhwpfuomdbmp',
            station_no='xmqrwoqynjeyzhmaaeva',
            station_name='chxjzkmjjhgmcjwhgzag',
            latitude=float(3.4831362492394713),
            longitude=float(93.22511660601135),
            river_name='yxfgkpxcorchbgfmonvi',
            catchment_name='hmmnhigldbxfxbnpbijv'
        )
        return instance

    
    def test_kiwis_id_property(self):
        """
        Test kiwis_id property
        """
        test_value = 'umgeftqqbyxktjqjrppz'
        self.instance.kiwis_id = test_value
        self.assertEqual(self.instance.kiwis_id, test_value)
    
    def test_base_url_property(self):
        """
        Test base_url property
        """
        test_value = 'ondtmdjgnfvtudnllugo'
        self.instance.base_url = test_value
        self.assertEqual(self.instance.base_url, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'zzsjuoqxnhwpfuomdbmp'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_no_property(self):
        """
        Test station_no property
        """
        test_value = 'xmqrwoqynjeyzhmaaeva'
        self.instance.station_no = test_value
        self.assertEqual(self.instance.station_no, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'chxjzkmjjhgmcjwhgzag'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(3.4831362492394713)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(93.22511660601135)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'yxfgkpxcorchbgfmonvi'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)
    
    def test_catchment_name_property(self):
        """
        Test catchment_name property
        """
        test_value = 'hmmnhigldbxfxbnpbijv'
        self.instance.catchment_name = test_value
        self.assertEqual(self.instance.catchment_name, test_value)
    
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

