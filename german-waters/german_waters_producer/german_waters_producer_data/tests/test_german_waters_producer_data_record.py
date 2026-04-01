"""
Test case for Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from german_waters_producer_data.record import Record


class Test_Record(unittest.TestCase):
    """
    Test case for Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Record for testing
        """
        instance = Record(
            station_id='lxaffviezonipkuazsbu',
            station_name='ndmiyyenbqsvsejxytmu',
            water_body='yccjqdxrcndwvkynhqfw',
            state='vsxpewbntqbowbvpkgkl',
            region='ogcehshqqprdafejsqea',
            provider='zsxbkxgdeujdfiefaery',
            latitude=float(59.2281282269162),
            longitude=float(95.91853398408395),
            river_km=float(2.9857193330812937),
            altitude=float(95.53309893563181),
            station_type='thilvtxubpkhnvkivgsb',
            warn_level_cm=float(75.55868742259018),
            alarm_level_cm=float(75.40385965974106),
            warn_level_m3s=float(69.50805642557393),
            alarm_level_m3s=float(73.64342644269898)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'lxaffviezonipkuazsbu'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'ndmiyyenbqsvsejxytmu'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_water_body_property(self):
        """
        Test water_body property
        """
        test_value = 'yccjqdxrcndwvkynhqfw'
        self.instance.water_body = test_value
        self.assertEqual(self.instance.water_body, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'vsxpewbntqbowbvpkgkl'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'ogcehshqqprdafejsqea'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_provider_property(self):
        """
        Test provider property
        """
        test_value = 'zsxbkxgdeujdfiefaery'
        self.instance.provider = test_value
        self.assertEqual(self.instance.provider, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(59.2281282269162)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(95.91853398408395)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_river_km_property(self):
        """
        Test river_km property
        """
        test_value = float(2.9857193330812937)
        self.instance.river_km = test_value
        self.assertEqual(self.instance.river_km, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(95.53309893563181)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'thilvtxubpkhnvkivgsb'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_warn_level_cm_property(self):
        """
        Test warn_level_cm property
        """
        test_value = float(75.55868742259018)
        self.instance.warn_level_cm = test_value
        self.assertEqual(self.instance.warn_level_cm, test_value)
    
    def test_alarm_level_cm_property(self):
        """
        Test alarm_level_cm property
        """
        test_value = float(75.40385965974106)
        self.instance.alarm_level_cm = test_value
        self.assertEqual(self.instance.alarm_level_cm, test_value)
    
    def test_warn_level_m3s_property(self):
        """
        Test warn_level_m3s property
        """
        test_value = float(69.50805642557393)
        self.instance.warn_level_m3s = test_value
        self.assertEqual(self.instance.warn_level_m3s, test_value)
    
    def test_alarm_level_m3s_property(self):
        """
        Test alarm_level_m3s property
        """
        test_value = float(73.64342644269898)
        self.instance.alarm_level_m3s = test_value
        self.assertEqual(self.instance.alarm_level_m3s, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
