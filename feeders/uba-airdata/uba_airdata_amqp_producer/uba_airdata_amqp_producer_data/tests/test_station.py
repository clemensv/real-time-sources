"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_amqp_producer_data.de.uba.airdata.station import Station


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
            station_id=int(48),
            station_code='mzocxnvzupvkqhuhsows',
            station_name='kpqrjknnkwvxizqyhojv',
            station_city='cqzaoogigqohwovbotly',
            station_synonym='cnyhwfvqktrnkoofcddi',
            active_from='otjxgcgxhspncbtpshke',
            active_to='znyxlxpoipvneonjmjfu',
            longitude=float(50.87735065393011),
            latitude=float(16.449424346430476),
            network_id=int(6),
            network_code='uokdkooighqfytgakecu',
            network_name='jsmenvazyrggqrfbpqqi',
            setting_name='fdyfebyobekqgopfujdm',
            setting_short='jkinzicyhkoaoufcbsgf',
            type_name='wxasptabdnedauojwmif',
            street='qmnjalsjxhiikesuvtlq',
            street_nr='evsvbdlzexxzekzhqhwn',
            zip_code='mfmpievbslmwkvxlwdwc'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(48)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'mzocxnvzupvkqhuhsows'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'kpqrjknnkwvxizqyhojv'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_city_property(self):
        """
        Test station_city property
        """
        test_value = 'cqzaoogigqohwovbotly'
        self.instance.station_city = test_value
        self.assertEqual(self.instance.station_city, test_value)
    
    def test_station_synonym_property(self):
        """
        Test station_synonym property
        """
        test_value = 'cnyhwfvqktrnkoofcddi'
        self.instance.station_synonym = test_value
        self.assertEqual(self.instance.station_synonym, test_value)
    
    def test_active_from_property(self):
        """
        Test active_from property
        """
        test_value = 'otjxgcgxhspncbtpshke'
        self.instance.active_from = test_value
        self.assertEqual(self.instance.active_from, test_value)
    
    def test_active_to_property(self):
        """
        Test active_to property
        """
        test_value = 'znyxlxpoipvneonjmjfu'
        self.instance.active_to = test_value
        self.assertEqual(self.instance.active_to, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(50.87735065393011)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(16.449424346430476)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_network_id_property(self):
        """
        Test network_id property
        """
        test_value = int(6)
        self.instance.network_id = test_value
        self.assertEqual(self.instance.network_id, test_value)
    
    def test_network_code_property(self):
        """
        Test network_code property
        """
        test_value = 'uokdkooighqfytgakecu'
        self.instance.network_code = test_value
        self.assertEqual(self.instance.network_code, test_value)
    
    def test_network_name_property(self):
        """
        Test network_name property
        """
        test_value = 'jsmenvazyrggqrfbpqqi'
        self.instance.network_name = test_value
        self.assertEqual(self.instance.network_name, test_value)
    
    def test_setting_name_property(self):
        """
        Test setting_name property
        """
        test_value = 'fdyfebyobekqgopfujdm'
        self.instance.setting_name = test_value
        self.assertEqual(self.instance.setting_name, test_value)
    
    def test_setting_short_property(self):
        """
        Test setting_short property
        """
        test_value = 'jkinzicyhkoaoufcbsgf'
        self.instance.setting_short = test_value
        self.assertEqual(self.instance.setting_short, test_value)
    
    def test_type_name_property(self):
        """
        Test type_name property
        """
        test_value = 'wxasptabdnedauojwmif'
        self.instance.type_name = test_value
        self.assertEqual(self.instance.type_name, test_value)
    
    def test_street_property(self):
        """
        Test street property
        """
        test_value = 'qmnjalsjxhiikesuvtlq'
        self.instance.street = test_value
        self.assertEqual(self.instance.street, test_value)
    
    def test_street_nr_property(self):
        """
        Test street_nr property
        """
        test_value = 'evsvbdlzexxzekzhqhwn'
        self.instance.street_nr = test_value
        self.assertEqual(self.instance.street_nr, test_value)
    
    def test_zip_code_property(self):
        """
        Test zip_code property
        """
        test_value = 'mfmpievbslmwkvxlwdwc'
        self.instance.zip_code = test_value
        self.assertEqual(self.instance.zip_code, test_value)
    
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

