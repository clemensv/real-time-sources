"""
Test case for Arrival
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from irail_producer_data.be.irail.arrival import Arrival


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
            origin_station_id='dhtlqhtqckladqiiqwkq',
            origin_name='nilhqjxlfndiwmfdsqme',
            scheduled_time='ndktbbktgylngbbvbvhq',
            delay_seconds=int(92),
            is_canceled=False,
            has_arrived=True,
            is_extra_stop=False,
            vehicle_id='rzjfcrqidhudboiwrumv',
            vehicle_short_name='qvwrkdgfhpfplywnfgin',
            vehicle_type='mgiymzcaexavwgttbcda',
            vehicle_number='yaxbblftdsgzghsemztu',
            platform='mgpdgmhnprbeclinwdcl',
            is_normal_platform=True,
            occupancy='avayufrnslpsuyncuheh',
            connection_uri='ghlvhsnvvxldiplaomrn'
        )
        return instance

    
    def test_origin_station_id_property(self):
        """
        Test origin_station_id property
        """
        test_value = 'dhtlqhtqckladqiiqwkq'
        self.instance.origin_station_id = test_value
        self.assertEqual(self.instance.origin_station_id, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'nilhqjxlfndiwmfdsqme'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_scheduled_time_property(self):
        """
        Test scheduled_time property
        """
        test_value = 'ndktbbktgylngbbvbvhq'
        self.instance.scheduled_time = test_value
        self.assertEqual(self.instance.scheduled_time, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(92)
        self.instance.delay_seconds = test_value
        self.assertEqual(self.instance.delay_seconds, test_value)
    
    def test_is_canceled_property(self):
        """
        Test is_canceled property
        """
        test_value = False
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
        test_value = 'rzjfcrqidhudboiwrumv'
        self.instance.vehicle_id = test_value
        self.assertEqual(self.instance.vehicle_id, test_value)
    
    def test_vehicle_short_name_property(self):
        """
        Test vehicle_short_name property
        """
        test_value = 'qvwrkdgfhpfplywnfgin'
        self.instance.vehicle_short_name = test_value
        self.assertEqual(self.instance.vehicle_short_name, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = 'mgiymzcaexavwgttbcda'
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'yaxbblftdsgzghsemztu'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_platform_property(self):
        """
        Test platform property
        """
        test_value = 'mgpdgmhnprbeclinwdcl'
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
        test_value = 'avayufrnslpsuyncuheh'
        self.instance.occupancy = test_value
        self.assertEqual(self.instance.occupancy, test_value)
    
    def test_connection_uri_property(self):
        """
        Test connection_uri property
        """
        test_value = 'ghlvhsnvvxldiplaomrn'
        self.instance.connection_uri = test_value
        self.assertEqual(self.instance.connection_uri, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Arrival.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
