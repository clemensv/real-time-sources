"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eurdep_radiation_amqp_producer_data.eu.jrc.eurdep.station import Station


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
            station_id='gvnoywsuhfmteesdnmbx',
            name='rfwsotsjxtcyktktdfnj',
            latitude=float(94.84578064248325),
            longitude=float(21.58108456401647),
            height_above_sea=float(22.739357072839226),
            site_status=int(97),
            site_status_text='votopnsavtcgavptyfpj',
            country='lnjkpmvcnxvvpkcbzplh'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'gvnoywsuhfmteesdnmbx'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'rfwsotsjxtcyktktdfnj'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(94.84578064248325)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(21.58108456401647)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_height_above_sea_property(self):
        """
        Test height_above_sea property
        """
        test_value = float(22.739357072839226)
        self.instance.height_above_sea = test_value
        self.assertEqual(self.instance.height_above_sea, test_value)
    
    def test_site_status_property(self):
        """
        Test site_status property
        """
        test_value = int(97)
        self.instance.site_status = test_value
        self.assertEqual(self.instance.site_status, test_value)
    
    def test_site_status_text_property(self):
        """
        Test site_status_text property
        """
        test_value = 'votopnsavtcgavptyfpj'
        self.instance.site_status_text = test_value
        self.assertEqual(self.instance.site_status_text, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'lnjkpmvcnxvvpkcbzplh'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
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

