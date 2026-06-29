"""
Test case for Arrival
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_amqp_producer_data.be.irail.arrival import Arrival
from irail_amqp_producer_data.be.irail.occupancyenum import OccupancyEnum


class Test_Arrival(unittest.TestCase):
    """
    Test case for Arrival
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Arrival.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Arrival for testing
        """
        instance = Arrival(
            origin_station_id='fbttbsjddidqyudevwrr',
            origin_name='dtmwamrixlhlpwjiopqw',
            scheduled_time='xdzexcgswzqspvzhpqcg',
            delay_seconds=int(25),
            is_canceled=True,
            has_arrived=True,
            is_extra_stop=False,
            vehicle_id='qpqgsysqcntljxuvnkpf',
            vehicle_short_name='whkzjgajbvuoxusldvrw',
            vehicle_type='vpgmsqxekrjqntpxfuep',
            vehicle_number='oqrvsnzdboceihpjmbkf',
            platform='hjuiewexdlwuyrwbuabx',
            is_normal_platform=False,
            occupancy=OccupancyEnum.low,
            connection_uri='wjnmvgwovogeosjgfvay'
        )
        return instance

    
    def test_origin_station_id_property(self):
        """
        Test origin_station_id property
        """
        test_value = 'fbttbsjddidqyudevwrr'
        self.instance.origin_station_id = test_value
        self.assertEqual(self.instance.origin_station_id, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'dtmwamrixlhlpwjiopqw'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_scheduled_time_property(self):
        """
        Test scheduled_time property
        """
        test_value = 'xdzexcgswzqspvzhpqcg'
        self.instance.scheduled_time = test_value
        self.assertEqual(self.instance.scheduled_time, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(25)
        self.instance.delay_seconds = test_value
        self.assertEqual(self.instance.delay_seconds, test_value)
    
    def test_is_canceled_property(self):
        """
        Test is_canceled property
        """
        test_value = True
        self.instance.is_canceled = test_value
        self.assertEqual(self.instance.is_canceled, test_value)
    
    def test_has_arrived_property(self):
        """
        Test has_arrived property
        """
        test_value = True
        self.instance.has_arrived = test_value
        self.assertEqual(self.instance.has_arrived, test_value)
    
    def test_is_extra_stop_property(self):
        """
        Test is_extra_stop property
        """
        test_value = False
        self.instance.is_extra_stop = test_value
        self.assertEqual(self.instance.is_extra_stop, test_value)
    
    def test_vehicle_id_property(self):
        """
        Test vehicle_id property
        """
        test_value = 'qpqgsysqcntljxuvnkpf'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_vehicle_short_name_property(self):
        """
        Test vehicle_short_name property
        """
        test_value = 'whkzjgajbvuoxusldvrw'
        self.instance.vehicle_short_name = test_value
        self.assertEqual(self.instance.vehicle_short_name, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'vpgmsqxekrjqntpxfuep'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'oqrvsnzdboceihpjmbkf'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_platform_property(self):
        """
        Test platform property
        """
        test_value = 'hjuiewexdlwuyrwbuabx'
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
    
    def test_connection_uri_property(self):
        """
        Test connection_uri property
        """
        test_value = 'wjnmvgwovogeosjgfvay'
        self.instance.connection_uri = test_value
        self.assertEqual(self.instance.connection_uri, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Arrival.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Arrival.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

