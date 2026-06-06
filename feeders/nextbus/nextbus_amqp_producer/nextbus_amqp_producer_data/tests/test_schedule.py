"""
Test case for Schedule
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nextbus_amqp_producer_data.schedule import Schedule


class Test_Schedule(unittest.TestCase):
    """
    Test case for Schedule
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Schedule.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Schedule for testing
        """
        instance = Schedule(
            agency_id='mcedaqgiysqxxtpwsbpr',
            route_tag='upqyocgixbdntjsegikb',
            stop_or_vehicle_id='cjrikzngyvknzxzyfugw',
            event_type='rhwmkwidhjjmrpzjhxmg',
            schedule='bavldiihksiinttgkadj'
        )
        return instance

    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'mcedaqgiysqxxtpwsbpr'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_tag_property(self):
        """
        Test route_tag property
        """
        test_value = 'upqyocgixbdntjsegikb'
        self.instance.route_tag = test_value
        self.assertEqual(self.instance.route_tag, test_value)
    
    def test_stop_or_vehicle_id_property(self):
        """
        Test stop_or_vehicle_id property
        """
        test_value = 'cjrikzngyvknzxzyfugw'
        self.instance.stop_or_vehicle_id = test_value
        self.assertEqual(self.instance.stop_or_vehicle_id, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'rhwmkwidhjjmrpzjhxmg'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_schedule_property(self):
        """
        Test schedule property
        """
        test_value = 'bavldiihksiinttgkadj'
        self.instance.schedule = test_value
        self.assertEqual(self.instance.schedule, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Schedule.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Schedule.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

