"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uba_airdata_producer_data.de.uba.airdata.station import Station


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
            station_id=int(30),
            station_code='vfnftkdllqjwwpqkbfzx',
            station_name='vulnbdjnenufbhlcqfgb',
            station_city='plelvdgobrdtjzcnlqxv',
            station_synonym='npunuuqgkxsbiahhumye',
            active_from='kpkkesyshvzdqgbsfjhf',
            active_to='bzokliwvvbsmusporqau',
            longitude=float(72.66714333305863),
            latitude=float(68.57648893445189),
            network_id=int(41),
            network_code='zrqivskvdrkldlawrbry',
            network_name='aoxzdqcedluurzjbouzk',
            setting_name='eekhxmmwgdtxlixkjzmt',
            setting_short='ptzgwpabhsidgqvyhzht',
            type_name='epxkzkotvultwqusfboe',
            street='evapqbhcfhrkofjoahtu',
            street_nr='zyutuvnldyvvqmcbpklq',
            zip_code='ckybsbvbxooundwntlzv'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(30)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'vfnftkdllqjwwpqkbfzx'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'vulnbdjnenufbhlcqfgb'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_station_city_property(self):
        """
        Test station_city property
        """
        test_value = 'plelvdgobrdtjzcnlqxv'
        self.instance.station_city = test_value
        self.assertEqual(self.instance.station_city, test_value)
    
    def test_station_synonym_property(self):
        """
        Test station_synonym property
        """
        test_value = 'npunuuqgkxsbiahhumye'
        self.instance.station_synonym = test_value
        self.assertEqual(self.instance.station_synonym, test_value)
    
    def test_active_from_property(self):
        """
        Test active_from property
        """
        test_value = 'kpkkesyshvzdqgbsfjhf'
        self.instance.active_from = test_value
        self.assertEqual(self.instance.active_from, test_value)
    
    def test_active_to_property(self):
        """
        Test active_to property
        """
        test_value = 'bzokliwvvbsmusporqau'
        self.instance.active_to = test_value
        self.assertEqual(self.instance.active_to, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(72.66714333305863)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(68.57648893445189)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_network_id_property(self):
        """
        Test network_id property
        """
        test_value = int(41)
        self.instance.network_id = test_value
        self.assertEqual(self.instance.network_id, test_value)
    
    def test_network_code_property(self):
        """
        Test network_code property
        """
        test_value = 'zrqivskvdrkldlawrbry'
        self.instance.network_code = test_value
        self.assertEqual(self.instance.network_code, test_value)
    
    def test_network_name_property(self):
        """
        Test network_name property
        """
        test_value = 'aoxzdqcedluurzjbouzk'
        self.instance.network_name = test_value
        self.assertEqual(self.instance.network_name, test_value)
    
    def test_setting_name_property(self):
        """
        Test setting_name property
        """
        test_value = 'eekhxmmwgdtxlixkjzmt'
        self.instance.setting_name = test_value
        self.assertEqual(self.instance.setting_name, test_value)
    
    def test_setting_short_property(self):
        """
        Test setting_short property
        """
        test_value = 'ptzgwpabhsidgqvyhzht'
        self.instance.setting_short = test_value
        self.assertEqual(self.instance.setting_short, test_value)
    
    def test_type_name_property(self):
        """
        Test type_name property
        """
        test_value = 'epxkzkotvultwqusfboe'
        self.instance.type_name = test_value
        self.assertEqual(self.instance.type_name, test_value)
    
    def test_street_property(self):
        """
        Test street property
        """
        test_value = 'evapqbhcfhrkofjoahtu'
        self.instance.street = test_value
        self.assertEqual(self.instance.street, test_value)
    
    def test_street_nr_property(self):
        """
        Test street_nr property
        """
        test_value = 'zyutuvnldyvvqmcbpklq'
        self.instance.street_nr = test_value
        self.assertEqual(self.instance.street_nr, test_value)
    
    def test_zip_code_property(self):
        """
        Test zip_code property
        """
        test_value = 'ckybsbvbxooundwntlzv'
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

