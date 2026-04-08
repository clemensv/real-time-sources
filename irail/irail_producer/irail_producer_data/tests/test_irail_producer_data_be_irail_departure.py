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
            destination_station_id='kcmoxmpgnhlasnepizpj',
            destination_name='mcubhoxinhrfnggnnbvk',
            scheduled_time='qjakquaqspkqwnyvibyf',
            delay_seconds=int(100),
            is_canceled=False,
            has_left=True,
            is_extra_stop=True,
            vehicle_id='rdalkfceleocfkixxtgc',
            vehicle_short_name='wjtshmxreiyixkyiyawo',
            vehicle_type='qglzzvjodqqvjauibtvj',
            vehicle_number='zztjobomvqpswgfpwnoy',
            platform='dhjvacqmehrnjtokdigg',
            is_normal_platform=True,
            occupancy='qdnprlavvvonvbwlgwie',
            departure_connection_uri='astivzfslhsdhtxcovon'
        )
        return instance

    
    def test_destination_station_id_property(self):
        """
        Test destination_station_id property
        """
        test_value = 'kcmoxmpgnhlasnepizpj'
        self.instance.destination_station_id = test_value
        self.assertEqual(self.instance.destination_station_id, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'mcubhoxinhrfnggnnbvk'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_scheduled_time_property(self):
        """
        Test scheduled_time property
        """
        test_value = 'qjakquaqspkqwnyvibyf'
        self.instance.scheduled_time = test_value
        self.assertEqual(self.instance.scheduled_time, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(100)
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
        test_value = 'rdalkfceleocfkixxtgc'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_vehicle_short_name_property(self):
        """
        Test vehicle_short_name property
        """
        test_value = 'wjtshmxreiyixkyiyawo'
        self.instance.vehicle_short_name = test_value
        self.assertEqual(self.instance.vehicle_short_name, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'qglzzvjodqqvjauibtvj'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'zztjobomvqpswgfpwnoy'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_platform_property(self):
        """
        Test platform property
        """
        test_value = 'dhjvacqmehrnjtokdigg'
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
        test_value = 'qdnprlavvvonvbwlgwie'
        self.instance.occupancy = test_value
        self.assertEqual(self.instance.occupancy, test_value)
    
    def test_departure_connection_uri_property(self):
        """
        Test departure_connection_uri property
        """
        test_value = 'astivzfslhsdhtxcovon'
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
