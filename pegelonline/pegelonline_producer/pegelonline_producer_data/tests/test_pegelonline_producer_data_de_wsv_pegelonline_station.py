"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_producer_data.de.wsv.pegelonline.station import Station
from test_pegelonline_producer_data_de_wsv_pegelonline_water import Test_Water


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
            uuid='ygciorrlaoltnvqlkqog',
            number='aqiqdzfgqbgivqgnrfhs',
            shortname='yoqkvmwiherlqorzygqq',
            longname='vkdwfqyyytjjpnkrrfiv',
            km=float(8.379605816258096),
            agency='zcaurpgpxmmtzjjjxzpi',
            longitude=float(75.01678132618342),
            latitude=float(0.051411525612299336),
            water=Test_Water.create_instance()
        )
        return instance

    
    def test_uuid_property(self):
        """
        Test uuid property
        """
        test_value = 'ygciorrlaoltnvqlkqog'
        self.instance.uuid = test_value
        self.assertEqual(self.instance.uuid, test_value)
    
    def test_number_property(self):
        """
        Test number property
        """
        test_value = 'aqiqdzfgqbgivqgnrfhs'
        self.instance.number = test_value
        self.assertEqual(self.instance.number, test_value)
    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'yoqkvmwiherlqorzygqq'
        self.instance.shortname = test_value
        self.assertEqual(self.instance.shortname, test_value)
    
    def test_longname_property(self):
        """
        Test longname property
        """
        test_value = 'vkdwfqyyytjjpnkrrfiv'
        self.instance.longname = test_value
        self.assertEqual(self.instance.longname, test_value)
    
    def test_km_property(self):
        """
        Test km property
        """
        test_value = float(8.379605816258096)
        self.instance.km = test_value
        self.assertEqual(self.instance.km, test_value)
    
    def test_agency_property(self):
        """
        Test agency property
        """
        test_value = 'zcaurpgpxmmtzjjjxzpi'
        self.instance.agency = test_value
        self.assertEqual(self.instance.agency, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(75.01678132618342)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(0.051411525612299336)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_water_property(self):
        """
        Test water property
        """
        test_value = Test_Water.create_instance()
        self.instance.water = test_value
        self.assertEqual(self.instance.water, test_value)
    
