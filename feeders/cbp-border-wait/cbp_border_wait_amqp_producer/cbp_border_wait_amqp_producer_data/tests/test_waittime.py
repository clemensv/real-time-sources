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
            port_number='isfgwonhqmlmkywoxmxn',
            port_name='jgslambhgknprmdktabu',
            border='zqpeeugsyqdnoptbruuz',
            crossing_name='yyzjyxwaikckfbdlnuvc',
            port_status='kcuqfqjkybjqlypuyjww',
            date='mwqxqfzrclxhiduqcsuu',
            time='ntoicynsdldhophwnwnq',
            passenger_vehicle_standard_delay=int(5),
            passenger_vehicle_standard_lanes_open=int(56),
            passenger_vehicle_standard_operational_status='ouyyqaimtabbwiuducdu',
            passenger_vehicle_nexus_sentri_delay=int(63),
            passenger_vehicle_nexus_sentri_lanes_open=int(57),
            passenger_vehicle_nexus_sentri_operational_status='mjeulxddmvjvxiimqghm',
            passenger_vehicle_ready_delay=int(59),
            passenger_vehicle_ready_lanes_open=int(11),
            passenger_vehicle_ready_operational_status='wnppfpwgrqpcafevfjay',
            pedestrian_standard_delay=int(92),
            pedestrian_standard_lanes_open=int(65),
            pedestrian_standard_operational_status='vpyfeqcxjedjlztoapbe',
            pedestrian_ready_delay=int(50),
            pedestrian_ready_lanes_open=int(13),
            pedestrian_ready_operational_status='yjdaddxlyfunmedvgfdl',
            commercial_vehicle_standard_delay=int(37),
            commercial_vehicle_standard_lanes_open=int(44),
            commercial_vehicle_standard_operational_status='ceezkrgnaprdtkviyrql',
            commercial_vehicle_fast_delay=int(20),
            commercial_vehicle_fast_lanes_open=int(96),
            commercial_vehicle_fast_operational_status='emrmagstpsnvuagdhznr',
            construction_notice='lkcnqervrdtlmwtwfvhm',
            border_slug=BorderSlugenum.canadian_MINUSborder
        )
        return instance

    
    def test_port_number_property(self):
        """
        Test port_number property
        """
        test_value = 'isfgwonhqmlmkywoxmxn'
        self.instance.port_number = test_value
        self.assertEqual(self.instance.port_number, test_value)
    
    def test_port_name_property(self):
        """
        Test port_name property
        """
        test_value = 'jgslambhgknprmdktabu'
        self.instance.port_name = test_value
        self.assertEqual(self.instance.port_name, test_value)
    
    def test_border_property(self):
        """
        Test border property
        """
        test_value = 'zqpeeugsyqdnoptbruuz'
        self.instance.border = test_value
        self.assertEqual(self.instance.border, test_value)
    
    def test_crossing_name_property(self):
        """
        Test crossing_name property
        """
        test_value = 'yyzjyxwaikckfbdlnuvc'
        self.instance.crossing_name = test_value
        self.assertEqual(self.instance.crossing_name, test_value)
    
    def test_port_status_property(self):
        """
        Test port_status property
        """
        test_value = 'kcuqfqjkybjqlypuyjww'
        self.instance.port_status = test_value
        self.assertEqual(self.instance.port_status, test_value)
    
    def test_date_property(self):
        """
        Test date property
        """
        test_value = 'mwqxqfzrclxhiduqcsuu'
        self.instance.date = test_value
        self.assertEqual(self.instance.date, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = 'ntoicynsdldhophwnwnq'
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_passenger_vehicle_standard_delay_property(self):
        """
        Test passenger_vehicle_standard_delay property
        """
        test_value = int(5)
        self.instance.passenger_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_delay, test_value)
    
    def test_passenger_vehicle_standard_lanes_open_property(self):
        """
        Test passenger_vehicle_standard_lanes_open property
        """
        test_value = int(56)
        self.instance.passenger_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_lanes_open, test_value)
    
    def test_passenger_vehicle_standard_operational_status_property(self):
        """
        Test passenger_vehicle_standard_operational_status property
        """
        test_value = 'ouyyqaimtabbwiuducdu'
        self.instance.passenger_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_standard_operational_status, test_value)
    
    def test_passenger_vehicle_nexus_sentri_delay_property(self):
        """
        Test passenger_vehicle_nexus_sentri_delay property
        """
        test_value = int(63)
        self.instance.passenger_vehicle_nexus_sentri_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_delay, test_value)
    
    def test_passenger_vehicle_nexus_sentri_lanes_open_property(self):
        """
        Test passenger_vehicle_nexus_sentri_lanes_open property
        """
        test_value = int(57)
        self.instance.passenger_vehicle_nexus_sentri_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_lanes_open, test_value)
    
    def test_passenger_vehicle_nexus_sentri_operational_status_property(self):
        """
        Test passenger_vehicle_nexus_sentri_operational_status property
        """
        test_value = 'mjeulxddmvjvxiimqghm'
        self.instance.passenger_vehicle_nexus_sentri_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_nexus_sentri_operational_status, test_value)
    
    def test_passenger_vehicle_ready_delay_property(self):
        """
        Test passenger_vehicle_ready_delay property
        """
        test_value = int(59)
        self.instance.passenger_vehicle_ready_delay = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_delay, test_value)
    
    def test_passenger_vehicle_ready_lanes_open_property(self):
        """
        Test passenger_vehicle_ready_lanes_open property
        """
        test_value = int(11)
        self.instance.passenger_vehicle_ready_lanes_open = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_lanes_open, test_value)
    
    def test_passenger_vehicle_ready_operational_status_property(self):
        """
        Test passenger_vehicle_ready_operational_status property
        """
        test_value = 'wnppfpwgrqpcafevfjay'
        self.instance.passenger_vehicle_ready_operational_status = test_value
        self.assertEqual(self.instance.passenger_vehicle_ready_operational_status, test_value)
    
    def test_pedestrian_standard_delay_property(self):
        """
        Test pedestrian_standard_delay property
        """
        test_value = int(92)
        self.instance.pedestrian_standard_delay = test_value
        self.assertEqual(self.instance.pedestrian_standard_delay, test_value)
    
    def test_pedestrian_standard_lanes_open_property(self):
        """
        Test pedestrian_standard_lanes_open property
        """
        test_value = int(65)
        self.instance.pedestrian_standard_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_standard_lanes_open, test_value)
    
    def test_pedestrian_standard_operational_status_property(self):
        """
        Test pedestrian_standard_operational_status property
        """
        test_value = 'vpyfeqcxjedjlztoapbe'
        self.instance.pedestrian_standard_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_standard_operational_status, test_value)
    
    def test_pedestrian_ready_delay_property(self):
        """
        Test pedestrian_ready_delay property
        """
        test_value = int(50)
        self.instance.pedestrian_ready_delay = test_value
        self.assertEqual(self.instance.pedestrian_ready_delay, test_value)
    
    def test_pedestrian_ready_lanes_open_property(self):
        """
        Test pedestrian_ready_lanes_open property
        """
        test_value = int(13)
        self.instance.pedestrian_ready_lanes_open = test_value
        self.assertEqual(self.instance.pedestrian_ready_lanes_open, test_value)
    
    def test_pedestrian_ready_operational_status_property(self):
        """
        Test pedestrian_ready_operational_status property
        """
        test_value = 'yjdaddxlyfunmedvgfdl'
        self.instance.pedestrian_ready_operational_status = test_value
        self.assertEqual(self.instance.pedestrian_ready_operational_status, test_value)
    
    def test_commercial_vehicle_standard_delay_property(self):
        """
        Test commercial_vehicle_standard_delay property
        """
        test_value = int(37)
        self.instance.commercial_vehicle_standard_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_delay, test_value)
    
    def test_commercial_vehicle_standard_lanes_open_property(self):
        """
        Test commercial_vehicle_standard_lanes_open property
        """
        test_value = int(44)
        self.instance.commercial_vehicle_standard_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_lanes_open, test_value)
    
    def test_commercial_vehicle_standard_operational_status_property(self):
        """
        Test commercial_vehicle_standard_operational_status property
        """
        test_value = 'ceezkrgnaprdtkviyrql'
        self.instance.commercial_vehicle_standard_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_standard_operational_status, test_value)
    
    def test_commercial_vehicle_fast_delay_property(self):
        """
        Test commercial_vehicle_fast_delay property
        """
        test_value = int(20)
        self.instance.commercial_vehicle_fast_delay = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_delay, test_value)
    
    def test_commercial_vehicle_fast_lanes_open_property(self):
        """
        Test commercial_vehicle_fast_lanes_open property
        """
        test_value = int(96)
        self.instance.commercial_vehicle_fast_lanes_open = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_lanes_open, test_value)
    
    def test_commercial_vehicle_fast_operational_status_property(self):
        """
        Test commercial_vehicle_fast_operational_status property
        """
        test_value = 'emrmagstpsnvuagdhznr'
        self.instance.commercial_vehicle_fast_operational_status = test_value
        self.assertEqual(self.instance.commercial_vehicle_fast_operational_status, test_value)
    
    def test_construction_notice_property(self):
        """
        Test construction_notice property
        """
        test_value = 'lkcnqervrdtlmwtwfvhm'
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

