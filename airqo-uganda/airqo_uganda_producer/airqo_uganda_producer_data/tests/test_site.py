"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from airqo_uganda_producer_data.site import Site


class Test_Site(unittest.TestCase):
    """
    Test case for Site
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Site.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Site for testing
        """
        instance = Site(
            site_id='dhffgzvkhljnqfkircbo',
            name='gkocddqdejfvmxarjkxe',
            formatted_name='eryibbscjqotavfqiqug',
            latitude=float(65.88290490020007),
            longitude=float(66.49585435828136),
            country='gapolevwbucdfxsjmvqe',
            region='eurcasxyxzfrvueequbr',
            city='tchdbvrkxblbkvwmrqze',
            is_online=True
        )
        return instance

    
    def test_site_id_property(self):
        """
        Test site_id property
        """
        test_value = 'dhffgzvkhljnqfkircbo'
        self.instance.site_id = test_value
        self.assertEqual(self.instance.site_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'gkocddqdejfvmxarjkxe'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_formatted_name_property(self):
        """
        Test formatted_name property
        """
        test_value = 'eryibbscjqotavfqiqug'
        self.instance.formatted_name = test_value
        self.assertEqual(self.instance.formatted_name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(65.88290490020007)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(66.49585435828136)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'gapolevwbucdfxsjmvqe'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_region_property(self):
        """
        Test region property
        """
        test_value = 'eurcasxyxzfrvueequbr'
        self.instance.region = test_value
        self.assertEqual(self.instance.region, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'tchdbvrkxblbkvwmrqze'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_is_online_property(self):
        """
        Test is_online property
        """
        test_value = True
        self.instance.is_online = test_value
        self.assertEqual(self.instance.is_online, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Site.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

