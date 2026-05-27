"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eurdep_radiation_producer_data.eu.jrc.eurdep.station import Station


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
            station_id='dqstyaiifuaglfzxaidz',
            name='xpktugkdxkyzctqofhmm',
            latitude=float(70.18100834972664),
            longitude=float(25.167174011908877),
            height_above_sea=float(34.02516173174952),
            site_status=int(24),
            site_status_text='msgksvtudjwqdxphigub',
            country='gdzsmrqlgjgpkqdmtkvy'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'dqstyaiifuaglfzxaidz'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xpktugkdxkyzctqofhmm'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(70.18100834972664)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(25.167174011908877)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_height_above_sea_property(self):
        """
        Test height_above_sea property
        """
        test_value = float(34.02516173174952)
        self.instance.height_above_sea = test_value
        self.assertEqual(self.instance.height_above_sea, test_value)
    
    def test_site_status_property(self):
        """
        Test site_status property
        """
        test_value = int(24)
        self.instance.site_status = test_value
        self.assertEqual(self.instance.site_status, test_value)
    
    def test_site_status_text_property(self):
        """
        Test site_status_text property
        """
        test_value = 'msgksvtudjwqdxphigub'
        self.instance.site_status_text = test_value
        self.assertEqual(self.instance.site_status_text, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'gdzsmrqlgjgpkqdmtkvy'
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

