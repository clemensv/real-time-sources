"""
Test case for OceanStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.oceanstation import OceanStation


class Test_OceanStation(unittest.TestCase):
    """
    Test case for OceanStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OceanStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OceanStation for testing
        """
        instance = OceanStation(
            station_id='gpnoihgjmdxpixzjyccg',
            name='adelvikdzcxpzhgjwxsf',
            country='bnollwsyxujlozqcfasf',
            owner='zbqehaiczojwvcwserxj',
            type='lfvstpeugihbruxepslz',
            status='cveupidtnvtjkreguama',
            parameter_id=['hqqphpcjjpeiifnorhmw', 'vtemqzwtzrkkuhcsikcg', 'wccxoorwyuoysgmlefpr', 'ypnmmfscfipkistrppfa'],
            latitude=float(84.85317904474944),
            longitude=float(90.0248961330952),
            valid_from='bpkjvknuwlriuojjzmyy',
            valid_to='xtcuwbzzycxkqvcywsnq',
            operation_from='izwzezjvesilqobjnwrh',
            operation_to='olplkwphyqsetcjgxaks',
            created='acosavqwmsmhwujrjzgk',
            updated='zctmxvntcvdgwajziiaa'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gpnoihgjmdxpixzjyccg'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'adelvikdzcxpzhgjwxsf'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'bnollwsyxujlozqcfasf'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'zbqehaiczojwvcwserxj'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'lfvstpeugihbruxepslz'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'cveupidtnvtjkreguama'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_id_property(self):
        """
        Test parameter_id property
        """
        test_value = ['hqqphpcjjpeiifnorhmw', 'vtemqzwtzrkkuhcsikcg', 'wccxoorwyuoysgmlefpr', 'ypnmmfscfipkistrppfa']
        self.instance.parameter_id = test_value
        self.assertEqual(self.instance.parameter_id, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(84.85317904474944)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(90.0248961330952)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_valid_from_property(self):
        """
        Test valid_from property
        """
        test_value = 'bpkjvknuwlriuojjzmyy'
        self.instance.valid_from = test_value
        self.assertEqual(self.instance.valid_from, test_value)
    
    def test_valid_to_property(self):
        """
        Test valid_to property
        """
        test_value = 'xtcuwbzzycxkqvcywsnq'
        self.instance.valid_to = test_value
        self.assertEqual(self.instance.valid_to, test_value)
    
    def test_operation_from_property(self):
        """
        Test operation_from property
        """
        test_value = 'izwzezjvesilqobjnwrh'
        self.instance.operation_from = test_value
        self.assertEqual(self.instance.operation_from, test_value)
    
    def test_operation_to_property(self):
        """
        Test operation_to property
        """
        test_value = 'olplkwphyqsetcjgxaks'
        self.instance.operation_to = test_value
        self.assertEqual(self.instance.operation_to, test_value)
    
    def test_created_property(self):
        """
        Test created property
        """
        test_value = 'acosavqwmsmhwujrjzgk'
        self.instance.created = test_value
        self.assertEqual(self.instance.created, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'zctmxvntcvdgwajziiaa'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OceanStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = OceanStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

