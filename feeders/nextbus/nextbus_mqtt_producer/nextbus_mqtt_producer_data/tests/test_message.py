"""
Test case for Message
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nextbus_mqtt_producer_data.message import Message


class Test_Message(unittest.TestCase):
    """
    Test case for Message
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Message.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Message for testing
        """
        instance = Message(
            agency_id='zmpgxpxsbvmbfvefnbev',
            route_tag='wtxttpqvywnagkqdnuon',
            stop_or_vehicle_id='vriuxalyhiwgvlldetha',
            event_type='jijmjowmcgoydgpvnpqm',
            message='cxhjsevafpxisijbgpyv'
        )
        return instance

    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'zmpgxpxsbvmbfvefnbev'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_tag_property(self):
        """
        Test route_tag property
        """
        test_value = 'wtxttpqvywnagkqdnuon'
        self.instance.route_tag = test_value
        self.assertEqual(self.instance.route_tag, test_value)
    
    def test_stop_or_vehicle_id_property(self):
        """
        Test stop_or_vehicle_id property
        """
        test_value = 'vriuxalyhiwgvlldetha'
        self.instance.stop_or_vehicle_id = test_value
        self.assertEqual(self.instance.stop_or_vehicle_id, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'jijmjowmcgoydgpvnpqm'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_message_property(self):
        """
        Test message property
        """
        test_value = 'cxhjsevafpxisijbgpyv'
        self.instance.message = test_value
        self.assertEqual(self.instance.message, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Message.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Message.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

