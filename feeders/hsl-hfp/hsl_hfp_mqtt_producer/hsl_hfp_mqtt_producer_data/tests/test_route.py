"""
Test case for Route
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_mqtt_producer_data.fi.hsl.gtfs.route import Route


class Test_Route(unittest.TestCase):
    """
    Test case for Route
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Route.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Route for testing
        """
        instance = Route(
            route_id='aduwksxnxcwfrzuzxdlg',
            agency_id='xcoudsnpdztazmdcasjr',
            route_short_name='vagyyunrxyqwvwdwsqag',
            route_long_name='hjdmjhzshlbffxncsluj',
            route_desc='ymaofjuocsdioojjgdyo',
            route_type=int(40),
            route_url='jjghhpdirzblhmvlnkol'
        )
        return instance

    
    def test_route_id_property(self):
        """
        Test route_id property
        """
        test_value = 'aduwksxnxcwfrzuzxdlg'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'xcoudsnpdztazmdcasjr'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_short_name_property(self):
        """
        Test route_short_name property
        """
        test_value = 'vagyyunrxyqwvwdwsqag'
        self.instance.route_short_name = test_value
        self.assertEqual(self.instance.route_short_name, test_value)
    
    def test_route_long_name_property(self):
        """
        Test route_long_name property
        """
        test_value = 'hjdmjhzshlbffxncsluj'
        self.instance.route_long_name = test_value
        self.assertEqual(self.instance.route_long_name, test_value)
    
    def test_route_desc_property(self):
        """
        Test route_desc property
        """
        test_value = 'ymaofjuocsdioojjgdyo'
        self.instance.route_desc = test_value
        self.assertEqual(self.instance.route_desc, test_value)
    
    def test_route_type_property(self):
        """
        Test route_type property
        """
        test_value = int(40)
        self.instance.route_type = test_value
        self.assertEqual(self.instance.route_type, test_value)
    
    def test_route_url_property(self):
        """
        Test route_url property
        """
        test_value = 'jjghhpdirzblhmvlnkol'
        self.instance.route_url = test_value
        self.assertEqual(self.instance.route_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Route.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Route.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

