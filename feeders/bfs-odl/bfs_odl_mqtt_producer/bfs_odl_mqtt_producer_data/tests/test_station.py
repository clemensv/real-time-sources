"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from bfs_odl_mqtt_producer_data.de.bfs.odl.station import Station


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
            station_id='flojbnvfhrpdwdayqkkr',
            state='avptirsqijilqvdxievn',
            station_code='qgasgzvpnwapkzcainpr',
            name='firphvdncvbvuxtufflo',
            postal_code='qxhsijzanwvsjjrdqadv',
            site_status=int(61),
            site_status_text='rhhuoaklywotizhanqyl',
            kid=int(8),
            height_above_sea=float(50.4153310225572),
            longitude=float(99.30003334081627),
            latitude=float(77.94949805595519)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'flojbnvfhrpdwdayqkkr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'avptirsqijilqvdxievn'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_station_code_property(self):
        """
        Test station_code property
        """
        test_value = 'qgasgzvpnwapkzcainpr'
        self.instance.station_code = test_value
        self.assertEqual(self.instance.station_code, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'firphvdncvbvuxtufflo'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'qxhsijzanwvsjjrdqadv'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_site_status_property(self):
        """
        Test site_status property
        """
        test_value = int(61)
        self.instance.site_status = test_value
        self.assertEqual(self.instance.site_status, test_value)
    
    def test_site_status_text_property(self):
        """
        Test site_status_text property
        """
        test_value = 'rhhuoaklywotizhanqyl'
        self.instance.site_status_text = test_value
        self.assertEqual(self.instance.site_status_text, test_value)
    
    def test_kid_property(self):
        """
        Test kid property
        """
        test_value = int(8)
        self.instance.kid = test_value
        self.assertEqual(self.instance.kid, test_value)
    
    def test_height_above_sea_property(self):
        """
        Test height_above_sea property
        """
        test_value = float(50.4153310225572)
        self.instance.height_above_sea = test_value
        self.assertEqual(self.instance.height_above_sea, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(99.30003334081627)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(77.94949805595519)
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

