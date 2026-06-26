"""
Test case for WaitTime
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime
from cbp_border_wait_producer_data.gov.cbp.borderwait.borderslugenum import BorderSlugenum


class Test_WaitTime(unittest.TestCase):
    """
    Test case for WaitTime
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaitTime.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaitTime for testing
        """
        instance = WaitTime(
            port_number='dqffrzgshkopmlmeiuiw',
            port_name='hltmbykdwphldmefmpry',
            border='sqmnlzjbvfaudpwxeqlz',
            crossing_name='jrrxqvvgglzxabozxnpi',
            port_status='brpoyzwmhqckonznihnp',
            date='jpmcwrnifaxouxqlqagd',
            time='lenmrunamgtqgnidretd',
            passenger_vehicle_standard_delay=int(78),
            passenger_vehicle_standard_lanes_open=int(27),
            passenger_vehicle_standard_operational_status='qabqrxunrpsztmsljiwr',
            passenger_vehicle_nexus_sentri_delay=int(11),
            passenger_vehicle_nexus_sentri_lanes_open=int(53),
            passenger_vehicle_nexus_sentri_operational_status='aqvpslaseaaxlbgfowyq',
            passenger_vehicle_ready_delay=int(19),
            passenger_vehicle_ready_lanes_open=int(65),
            passenger_vehicle_ready_operational_status='atlqsbgzpvkmlkymiybb',
            pedestrian_standard_delay=int(16),
            pedestrian_standard_lanes_open=int(76),
            pedestrian_standard_operational_status='hyahfmfguhdcyqvectjz',
            pedestrian_ready_delay=int(98),
            pedestrian_ready_lanes_open=int(14),
            pedestrian_ready_operational_status='twkeogkxydppgbtpaddd',
            commercial_vehicle_standard_delay=int(15),
            commercial_vehicle_standard_lanes_open=int(9),
            commercial_vehicle_standard_operational_status='dccyrssocqqycookucbi',
            commercial_vehicle_fast_delay=int(31),
            commercial_vehicle_fast_lanes_open=int(99),
            commercial_vehicle_fast_operational_status='zcgyrolnhnqzlmdxvzqg',
            construction_notice='kenngvsjqzjsmmzjzwak',
            border_slug=BorderSlugenum.canadian_MINUSborder
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'dqffrzgshkopmlmeiuiw'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'hltmbykdwphldmefmpry'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'sqmnlzjbvfaudpwxeqlz'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'jrrxqvvgglzxabozxnpi'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_port_status_property(self):
        """
        Test port_status property
        """
        test_value = 'brpoyzwmhqckonznihnp'
        self.instance.port_status = test_value
        self.assertEqual(self.instance.port_status, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'jpmcwrnifaxouxqlqagd'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'lenmrunamgtqgnidretd'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_passenger_vehicle_standard_delay_property(self):
        """
        Test passenger_vehicle_standard_delay property
        """
        test_value = int(78)
        self.instance.passenger_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_delay, test_value)
    
    def test_passenger_vehicle_standard_lanes_open_property(self):
        """
        Test passenger_vehicle_standard_lanes_open property
        """
        test_value = int(27)
        self.instance.passenger_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_lanes_open, test_value)
    
    def test_passenger_vehicle_standard_operational_status_property(self):
        """
        Test passenger_vehicle_standard_operational_status property
        """
        test_value = 'qabqrxunrpsztmsljiwr'
        self.instance.passenger_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_operational_status, test_value)
    
    def test_passenger_vehicle_nexus_sentri_delay_property(self):
        """
        Test passenger_vehicle_nexus_sentri_delay property
        """
        test_value = int(11)
        self.instance.passenger_vehicle_nexus_sentri_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_delay, test_value)
    
    def test_passenger_vehicle_nexus_sentri_lanes_open_property(self):
        """
        Test passenger_vehicle_nexus_sentri_lanes_open property
        """
        test_value = int(53)
        self.instance.passenger_vehicle_nexus_sentri_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_lanes_open, test_value)
    
    def test_passenger_vehicle_nexus_sentri_operational_status_property(self):
        """
        Test passenger_vehicle_nexus_sentri_operational_status property
        """
        test_value = 'aqvpslaseaaxlbgfowyq'
        self.instance.passenger_vehicle_nexus_sentri_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_operational_status, test_value)
    
    def test_passenger_vehicle_ready_delay_property(self):
        """
        Test passenger_vehicle_ready_delay property
        """
        test_value = int(19)
        self.instance.passenger_vehicle_ready_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_delay, test_value)
    
    def test_passenger_vehicle_ready_lanes_open_property(self):
        """
        Test passenger_vehicle_ready_lanes_open property
        """
        test_value = int(65)
        self.instance.passenger_vehicle_ready_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_lanes_open, test_value)
    
    def test_passenger_vehicle_ready_operational_status_property(self):
        """
        Test passenger_vehicle_ready_operational_status property
        """
        test_value = 'atlqsbgzpvkmlkymiybb'
        self.instance.passenger_vehicle_ready_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_operational_status, test_value)
    
    def test_pedestrian_standard_delay_property(self):
        """
        Test pedestrian_standard_delay property
        """
        test_value = int(16)
        self.instance.pedestrian_standard_delay = test_value
        self.assertEqual(self.instance.pedestrian_standard_delay, test_value)
    
    def test_pedestrian_standard_lanes_open_property(self):
        """
        Test pedestrian_standard_lanes_open property
        """
        test_value = int(76)
        self.instance.pedestrian_standard_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_standard_lanes_open, test_value)
    
    def test_pedestrian_standard_operational_status_property(self):
        """
        Test pedestrian_standard_operational_status property
        """
        test_value = 'hyahfmfguhdcyqvectjz'
        self.instance.pedestrian_standard_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_standard_operational_status, test_value)
    
    def test_pedestrian_ready_delay_property(self):
        """
        Test pedestrian_ready_delay property
        """
        test_value = int(98)
        self.instance.pedestrian_ready_delay = test_value
        self.assertEqual(self.instance.pedestrian_ready_delay, test_value)
    
    def test_pedestrian_ready_lanes_open_property(self):
        """
        Test pedestrian_ready_lanes_open property
        """
        test_value = int(14)
        self.instance.pedestrian_ready_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_ready_lanes_open, test_value)
    
    def test_pedestrian_ready_operational_status_property(self):
        """
        Test pedestrian_ready_operational_status property
        """
        test_value = 'twkeogkxydppgbtpaddd'
        self.instance.pedestrian_ready_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_ready_operational_status, test_value)
    
    def test_commercial_vehicle_standard_delay_property(self):
        """
        Test commercial_vehicle_standard_delay property
        """
        test_value = int(15)
        self.instance.commercial_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_delay, test_value)
    
    def test_commercial_vehicle_standard_lanes_open_property(self):
        """
        Test commercial_vehicle_standard_lanes_open property
        """
        test_value = int(9)
        self.instance.commercial_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_lanes_open, test_value)
    
    def test_commercial_vehicle_standard_operational_status_property(self):
        """
        Test commercial_vehicle_standard_operational_status property
        """
        test_value = 'dccyrssocqqycookucbi'
        self.instance.commercial_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_operational_status, test_value)
    
    def test_commercial_vehicle_fast_delay_property(self):
        """
        Test commercial_vehicle_fast_delay property
        """
        test_value = int(31)
        self.instance.commercial_vehicle_fast_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_delay, test_value)
    
    def test_commercial_vehicle_fast_lanes_open_property(self):
        """
        Test commercial_vehicle_fast_lanes_open property
        """
        test_value = int(99)
        self.instance.commercial_vehicle_fast_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_lanes_open, test_value)
    
    def test_commercial_vehicle_fast_operational_status_property(self):
        """
        Test commercial_vehicle_fast_operational_status property
        """
        test_value = 'zcgyrolnhnqzlmdxvzqg'
        self.instance.commercial_vehicle_fast_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_operational_status, test_value)
    
    def test_construction_notice_property(self):
        """
        Test construction_notice property
        """
        test_value = 'kenngvsjqzjsmmzjzwak'
        self.instance.construction_notice = test_value
        self.assertEqual(self.instance.construction_notice, test_value)
    
    def test_border_slug_property(self):
        """
        Test border_slug property
        """
        test_value = BorderSlugenum.canadian_MINUSborder
        self.instance.border_slug = test_value
        self.assertEqual(self.instance.border_slug, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaitTime.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaitTime.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

