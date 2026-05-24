"""
Test case for Departure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_mqtt_producer_data.be.irail.departure import Departure
from irail_mqtt_producer_data.be.irail.occupancyenum import OccupancyEnum


class Test_Departure(unittest.TestCase):
    """
    Test case for Departure
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Departure.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Departure for testing
        """
        instance = Departure(
            destination_station_id='kutmsonaximzbvniwttk',
            destination_name='hsphugsyhhpbtuwzrjkb',
            scheduled_time='gogukcycabeimihtalyn',
            delay_seconds=int(94),
            is_canceled=False,
            has_left=True,
            is_extra_stop=True,
            vehicle_id='okgtjdqhhqfiitcfrjls',
            vehicle_short_name='gycfdxkbnomqbcahznwh',
            vehicle_type='cwvptanfysnwyekxynrz',
            vehicle_number='mbjqvhfvcdmzvlekeuge',
            platform='frqjtfnbjhosefpjejna',
            is_normal_platform=False,
            occupancy=OccupancyEnum.low,
            departure_connection_uri='cwcbdpjmauzbztvfgdet'
        )
        return instance

    
    def test_destination_station_id_property(self):
        """
        Test destination_station_id property
        """
        test_value = 'kutmsonaximzbvniwttk'
        self.instance.destination_station_id = test_value
        self.assertEqual(self.instance.destination_station_id, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'hsphugsyhhpbtuwzrjkb'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_scheduled_time_property(self):
        """
        Test scheduled_time property
        """
        test_value = 'gogukcycabeimihtalyn'
        self.instance.scheduled_time = test_value
        self.assertEqual(self.instance.scheduled_time, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(94)
        self.instance.delay_seconds = test_value
        self.assertEqual(self.instance.delay_seconds, test_value)
    
    def test_is_canceled_property(self):
        """
        Test is_canceled property
        """
        test_value = False
        self.instance.is_canceled = test_value
        self.assertEqual(self.instance.is_canceled, test_value)
    
    def test_has_left_property(self):
        """
        Test has_left property
        """
        test_value = True
        self.instance.has_left = test_value
        self.assertEqual(self.instance.has_left, test_value)
    
    def test_is_extra_stop_property(self):
        """
        Test is_extra_stop property
        """
        test_value = True
        self.instance.is_extra_stop = test_value
        self.assertEqual(self.instance.is_extra_stop, test_value)
    
    def test_vehicle_id_property(self):
        """
        Test vehicle_id property
        """
        test_value = 'okgtjdqhhqfiitcfrjls'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_vehicle_short_name_property(self):
        """
        Test vehicle_short_name property
        """
        test_value = 'gycfdxkbnomqbcahznwh'
        self.instance.vehicle_short_name = test_value
        self.assertEqual(self.instance.vehicle_short_name, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'cwvptanfysnwyekxynrz'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'mbjqvhfvcdmzvlekeuge'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_platform_property(self):
        """
        Test platform property
        """
        test_value = 'frqjtfnbjhosefpjejna'
        self.instance.platform = test_value
        self.assertEqual(self.instance.platform, test_value)
    
    def test_is_normal_platform_property(self):
        """
        Test is_normal_platform property
        """
        test_value = False
        self.instance.is_normal_platform = test_value
        self.assertEqual(self.instance.is_normal_platform, test_value)
    
    def test_occupancy_property(self):
        """
        Test occupancy property
        """
        test_value = OccupancyEnum.low
        self.instance.occupancy = test_value
        self.assertEqual(self.instance.occupancy, test_value)
    
    def test_departure_connection_uri_property(self):
        """
        Test departure_connection_uri property
        """
        test_value = 'cwcbdpjmauzbztvfgdet'
        self.instance.departure_connection_uri = test_value
        self.assertEqual(self.instance.departure_connection_uri, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Departure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Departure.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

