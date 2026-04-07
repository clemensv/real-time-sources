"""
Test case for Departure
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_producer_data.be.irail.departure import Departure


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
            destination_station_id='qdatdrycesgdglbhabuk',
            destination_name='lgzjmwwgeqssypynmgoa',
            scheduled_time='imxlvgmkqcihwydcboyw',
            delay_seconds=int(59),
            is_canceled=False,
            has_left=True,
            is_extra_stop=True,
            vehicle_id='skwwhsfzrpaddsrjghju',
            vehicle_short_name='gdodsgzkopwyswabblqe',
            vehicle_type='qagbomskbcseechljpvr',
            vehicle_number='clqgpsnjgkispasugpti',
            platform='ivshezuupdgxbshjmhtb',
            is_normal_platform=True,
            occupancy='sbwqjfnpmajipmakoyoq',
            departure_connection_uri='wsmgbwcmmortrsqrdatq'
        )
        return instance

    
    def test_destination_station_id_property(self):
        """
        Test destination_station_id property
        """
        test_value = 'qdatdrycesgdglbhabuk'
        self.instance.destination_station_id = test_value
        self.assertEqual(self.instance.destination_station_id, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'lgzjmwwgeqssypynmgoa'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_scheduled_time_property(self):
        """
        Test scheduled_time property
        """
        test_value = 'imxlvgmkqcihwydcboyw'
        self.instance.scheduled_time = test_value
        self.assertEqual(self.instance.scheduled_time, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(59)
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
        test_value = 'skwwhsfzrpaddsrjghju'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_vehicle_short_name_property(self):
        """
        Test vehicle_short_name property
        """
        test_value = 'gdodsgzkopwyswabblqe'
        self.instance.vehicle_short_name = test_value
        self.assertEqual(self.instance.vehicle_short_name, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'qagbomskbcseechljpvr'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'clqgpsnjgkispasugpti'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_platform_property(self):
        """
        Test platform property
        """
        test_value = 'ivshezuupdgxbshjmhtb'
        self.instance.platform = test_value
        self.assertEqual(self.instance.platform, test_value)
    
    def test_is_normal_platform_property(self):
        """
        Test is_normal_platform property
        """
        test_value = True
        self.instance.is_normal_platform = test_value
        self.assertEqual(self.instance.is_normal_platform, test_value)
    
    def test_occupancy_property(self):
        """
        Test occupancy property
        """
        test_value = 'sbwqjfnpmajipmakoyoq'
        self.instance.occupancy = test_value
        self.assertEqual(self.instance.occupancy, test_value)
    
    def test_departure_connection_uri_property(self):
        """
        Test departure_connection_uri property
        """
        test_value = 'wsmgbwcmmortrsqrdatq'
        self.instance.departure_connection_uri = test_value
        self.assertEqual(self.instance.departure_connection_uri, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Departure.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
