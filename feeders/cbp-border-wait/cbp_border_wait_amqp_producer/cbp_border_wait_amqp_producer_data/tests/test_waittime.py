"""
Test case for WaitTime
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cbp_border_wait_amqp_producer_data.gov.cbp.borderwait.waittime import WaitTime
from cbp_border_wait_amqp_producer_data.gov.cbp.borderwait.borderslugenum import BorderSlugenum


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
            port_number='hxzpmpuhpskprioidbpg',
            port_name='ldemhtezhyjfuyeitwbj',
            border='hskubkyfdhxvmerrvkco',
            crossing_name='fvvqmycnnmibtegypovd',
            port_status='qzgwtzdamcuwqacbwhyu',
            date='uftwhlioqxzkfjefvraa',
            time='cqvfesfugunykmizifqy',
            passenger_vehicle_standard_delay=int(89),
            passenger_vehicle_standard_lanes_open=int(29),
            passenger_vehicle_standard_operational_status='jfmzulsvnugyspxxbsky',
            passenger_vehicle_nexus_sentri_delay=int(38),
            passenger_vehicle_nexus_sentri_lanes_open=int(66),
            passenger_vehicle_nexus_sentri_operational_status='ozhzttdjdzeajpkrbptf',
            passenger_vehicle_ready_delay=int(81),
            passenger_vehicle_ready_lanes_open=int(99),
            passenger_vehicle_ready_operational_status='yxwtxhugzebccwlwzayp',
            pedestrian_standard_delay=int(83),
            pedestrian_standard_lanes_open=int(19),
            pedestrian_standard_operational_status='ijkrmzifuvpxcpqjenwk',
            pedestrian_ready_delay=int(24),
            pedestrian_ready_lanes_open=int(28),
            pedestrian_ready_operational_status='hietiohmpxkgzlwjbpsr',
            commercial_vehicle_standard_delay=int(12),
            commercial_vehicle_standard_lanes_open=int(32),
            commercial_vehicle_standard_operational_status='feniyaeyvrschofoxyrl',
            commercial_vehicle_fast_delay=int(60),
            commercial_vehicle_fast_lanes_open=int(62),
            commercial_vehicle_fast_operational_status='fgpnwjqcqvhecrnhuott',
            construction_notice='nbqoxstoaweelmcuowah',
            border_slug=BorderSlugenum.canadian_border
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'hxzpmpuhpskprioidbpg'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'ldemhtezhyjfuyeitwbj'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'hskubkyfdhxvmerrvkco'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'fvvqmycnnmibtegypovd'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_port_status_property(self):
        """
        Test port_status property
        """
        test_value = 'qzgwtzdamcuwqacbwhyu'
        self.instance.port_status = test_value
        self.assertEqual(self.instance.port_status, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'uftwhlioqxzkfjefvraa'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'cqvfesfugunykmizifqy'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_passenger_vehicle_standard_delay_property(self):
        """
        Test passenger_vehicle_standard_delay property
        """
        test_value = int(89)
        self.instance.passenger_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_delay, test_value)
    
    def test_passenger_vehicle_standard_lanes_open_property(self):
        """
        Test passenger_vehicle_standard_lanes_open property
        """
        test_value = int(29)
        self.instance.passenger_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_lanes_open, test_value)
    
    def test_passenger_vehicle_standard_operational_status_property(self):
        """
        Test passenger_vehicle_standard_operational_status property
        """
        test_value = 'jfmzulsvnugyspxxbsky'
        self.instance.passenger_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_operational_status, test_value)
    
    def test_passenger_vehicle_nexus_sentri_delay_property(self):
        """
        Test passenger_vehicle_nexus_sentri_delay property
        """
        test_value = int(38)
        self.instance.passenger_vehicle_nexus_sentri_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_delay, test_value)
    
    def test_passenger_vehicle_nexus_sentri_lanes_open_property(self):
        """
        Test passenger_vehicle_nexus_sentri_lanes_open property
        """
        test_value = int(66)
        self.instance.passenger_vehicle_nexus_sentri_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_lanes_open, test_value)
    
    def test_passenger_vehicle_nexus_sentri_operational_status_property(self):
        """
        Test passenger_vehicle_nexus_sentri_operational_status property
        """
        test_value = 'ozhzttdjdzeajpkrbptf'
        self.instance.passenger_vehicle_nexus_sentri_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_operational_status, test_value)
    
    def test_passenger_vehicle_ready_delay_property(self):
        """
        Test passenger_vehicle_ready_delay property
        """
        test_value = int(81)
        self.instance.passenger_vehicle_ready_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_delay, test_value)
    
    def test_passenger_vehicle_ready_lanes_open_property(self):
        """
        Test passenger_vehicle_ready_lanes_open property
        """
        test_value = int(99)
        self.instance.passenger_vehicle_ready_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_lanes_open, test_value)
    
    def test_passenger_vehicle_ready_operational_status_property(self):
        """
        Test passenger_vehicle_ready_operational_status property
        """
        test_value = 'yxwtxhugzebccwlwzayp'
        self.instance.passenger_vehicle_ready_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_operational_status, test_value)
    
    def test_pedestrian_standard_delay_property(self):
        """
        Test pedestrian_standard_delay property
        """
        test_value = int(83)
        self.instance.pedestrian_standard_delay = test_value
        self.assertEqual(self.instance.pedestrian_standard_delay, test_value)
    
    def test_pedestrian_standard_lanes_open_property(self):
        """
        Test pedestrian_standard_lanes_open property
        """
        test_value = int(19)
        self.instance.pedestrian_standard_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_standard_lanes_open, test_value)
    
    def test_pedestrian_standard_operational_status_property(self):
        """
        Test pedestrian_standard_operational_status property
        """
        test_value = 'ijkrmzifuvpxcpqjenwk'
        self.instance.pedestrian_standard_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_standard_operational_status, test_value)
    
    def test_pedestrian_ready_delay_property(self):
        """
        Test pedestrian_ready_delay property
        """
        test_value = int(24)
        self.instance.pedestrian_ready_delay = test_value
        self.assertEqual(self.instance.pedestrian_ready_delay, test_value)
    
    def test_pedestrian_ready_lanes_open_property(self):
        """
        Test pedestrian_ready_lanes_open property
        """
        test_value = int(28)
        self.instance.pedestrian_ready_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_ready_lanes_open, test_value)
    
    def test_pedestrian_ready_operational_status_property(self):
        """
        Test pedestrian_ready_operational_status property
        """
        test_value = 'hietiohmpxkgzlwjbpsr'
        self.instance.pedestrian_ready_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_ready_operational_status, test_value)
    
    def test_commercial_vehicle_standard_delay_property(self):
        """
        Test commercial_vehicle_standard_delay property
        """
        test_value = int(12)
        self.instance.commercial_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_delay, test_value)
    
    def test_commercial_vehicle_standard_lanes_open_property(self):
        """
        Test commercial_vehicle_standard_lanes_open property
        """
        test_value = int(32)
        self.instance.commercial_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_lanes_open, test_value)
    
    def test_commercial_vehicle_standard_operational_status_property(self):
        """
        Test commercial_vehicle_standard_operational_status property
        """
        test_value = 'feniyaeyvrschofoxyrl'
        self.instance.commercial_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_operational_status, test_value)
    
    def test_commercial_vehicle_fast_delay_property(self):
        """
        Test commercial_vehicle_fast_delay property
        """
        test_value = int(60)
        self.instance.commercial_vehicle_fast_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_delay, test_value)
    
    def test_commercial_vehicle_fast_lanes_open_property(self):
        """
        Test commercial_vehicle_fast_lanes_open property
        """
        test_value = int(62)
        self.instance.commercial_vehicle_fast_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_lanes_open, test_value)
    
    def test_commercial_vehicle_fast_operational_status_property(self):
        """
        Test commercial_vehicle_fast_operational_status property
        """
        test_value = 'fgpnwjqcqvhecrnhuott'
        self.instance.commercial_vehicle_fast_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_operational_status, test_value)
    
    def test_construction_notice_property(self):
        """
        Test construction_notice property
        """
        test_value = 'nbqoxstoaweelmcuowah'
        self.instance.construction_notice = test_value
        self.assertEqual(self.instance.construction_notice, test_value)
    
    def test_border_slug_property(self):
        """
        Test border_slug property
        """
        test_value = BorderSlugenum.canadian_border
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

