"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bfs_odl_amqp_producer_data.de.bfs.odl.station import Station


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
            station_id='nmubttjjpqtscbkhmjxd',
            state='ymqawwpuqketlewhfwyi',
            station_code='ctslwdwfcksscstlohef',
            name='nyfkiqdrqyvlximinnxx',
            postal_code='dypkmpqahnxbzspbfijg',
            site_status=int(26),
            site_status_text='tqerbykskaoyizigcibz',
            kid=int(53),
            height_above_sea=float(12.76103824246616),
            longitude=float(93.95945802617227),
            latitude=float(52.29406969826965)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'nmubttjjpqtscbkhmjxd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'ymqawwpuqketlewhfwyi'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'ctslwdwfcksscstlohef'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'nyfkiqdrqyvlximinnxx'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'dypkmpqahnxbzspbfijg'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_site_status_property(self):
        """
        Test site_status property
        """
        test_value = int(26)
        self.instance.site_status = test_value
        self.assertEqual(self.instance.site_status, test_value)
    
    def test_site_status_text_property(self):
        """
        Test site_status_text property
        """
        test_value = 'tqerbykskaoyizigcibz'
        self.instance.site_status_text = test_value
        self.assertEqual(self.instance.site_status_text, test_value)
    
    def test_kid_property(self):
        """
        Test kid property
        """
        test_value = int(53)
        self.instance.kid = test_value
        self.assertEqual(self.instance.kid, test_value)
    
    def test_height_above_sea_property(self):
        """
        Test height_above_sea property
        """
        test_value = float(12.76103824246616)
        self.instance.height_above_sea = test_value
        self.assertEqual(self.instance.height_above_sea, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(93.95945802617227)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(52.29406969826965)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
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

