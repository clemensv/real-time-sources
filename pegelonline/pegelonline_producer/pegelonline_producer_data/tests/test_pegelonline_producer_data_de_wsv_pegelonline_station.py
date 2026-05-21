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
            station_id='pqigghnaeijyfbsskpqg',
            number='ogxvntpmwnsiprlbqzhk',
            shortname='vpxtenwmvgnfidhhtqvh',
            longname='awupfcvjplweypcpyjvm',
            km=float(28.29493127654984),
            agency='iutlgwspujvehwodpklr',
            longitude=float(75.54886439277999),
            latitude=float(35.21687465304193),
            water=Test_Water.create_instance()
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'pqigghnaeijyfbsskpqg'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_number_property(self):
        """
        Test number property
        """
        test_value = 'ogxvntpmwnsiprlbqzhk'
        self.instance.number = test_value
        self.assertEqual(self.instance.number, test_value)
    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'vpxtenwmvgnfidhhtqvh'
        self.instance.shortname = test_value
        self.assertEqual(self.instance.shortname, test_value)
    
    def test_longname_property(self):
        """
        Test longname property
        """
        test_value = 'awupfcvjplweypcpyjvm'
        self.instance.longname = test_value
        self.assertEqual(self.instance.longname, test_value)
    
    def test_km_property(self):
        """
        Test km property
        """
        test_value = float(28.29493127654984)
        self.instance.km = test_value
        self.assertEqual(self.instance.km, test_value)
    
    def test_agency_property(self):
        """
        Test agency property
        """
        test_value = 'iutlgwspujvehwodpklr'
        self.instance.agency = test_value
        self.assertEqual(self.instance.agency, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(75.54886439277999)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(35.21687465304193)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_water_property(self):
        """
        Test water property
        """
        test_value = Test_Water.create_instance()
        self.instance.water = test_value
        self.assertEqual(self.instance.water, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
