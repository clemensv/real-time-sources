"""
Test case for VehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nextbus_amqp_producer_data.vehicleposition import VehiclePosition


class Test_VehiclePosition(unittest.TestCase):
    """
    Test case for VehiclePosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehiclePosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehiclePosition for testing
        """
        instance = VehiclePosition(
            agency_id='gxtlekkjgscrrvkdjlgt',
            route_tag='nwmmpfwluutoywybiqoe',
            vehicle_id='yntqgyuwagtyljluelgy',
            stop_or_vehicle_id='jpynyrcouzgvzystiyxb',
            event_type='txvjwrjiijatcmkwddkc',
            lat='maebdbqaqqgmxccbyysh',
            lon='atkynlvpubjjkfoqocjq',
            timestamp=float(71.30900112229853)
        )
        return instance

    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'gxtlekkjgscrrvkdjlgt'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_tag_property(self):
        """
        Test route_tag property
        """
        test_value = 'nwmmpfwluutoywybiqoe'
        self.instance.route_tag = test_value
        self.assertEqual(self.instance.route_tag, test_value)
    
    def test_vehicle_id_property(self):
        """
        Test vehicle_id property
        """
        test_value = 'yntqgyuwagtyljluelgy'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_stop_or_vehicle_id_property(self):
        """
        Test stop_or_vehicle_id property
        """
        test_value = 'jpynyrcouzgvzystiyxb'
        self.instance.stop_or_vehicle_id = test_value
        self.assertEqual(self.instance.stop_or_vehicle_id, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'txvjwrjiijatcmkwddkc'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = 'maebdbqaqqgmxccbyysh'
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = 'atkynlvpubjjkfoqocjq'
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = float(71.30900112229853)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehiclePosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehiclePosition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

