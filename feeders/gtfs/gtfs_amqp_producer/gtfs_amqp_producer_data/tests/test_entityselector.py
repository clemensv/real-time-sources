"""
Test case for EntitySelector
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.entityselector import EntitySelector
from gtfs_amqp_producer_data.generaltransitfeedrealtime.alert.tripdescriptor import TripDescriptor


class Test_EntitySelector(unittest.TestCase):
    """
    Test case for EntitySelector
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EntitySelector.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EntitySelector for testing
        """
        instance = EntitySelector(
            agency_id='eynqxedavqwrtssabkel',
            route_id='fqhgdoyqgoeagkcthihu',
            route_type=int(23),
            trip=None,
            stop_id='rewhibpwfcwgfdnmpxbm'
        )
        return instance

    
    def test_agency_id_property(self):
        """
        Test agency_id property
        """
        test_value = 'eynqxedavqwrtssabkel'
        self.instance.agency_id = test_value
        self.assertEqual(self.instance.agency_id, test_value)
    
    def test_route_id_property(self):
        """
        Test route_id property
        """
        test_value = 'fqhgdoyqgoeagkcthihu'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_route_type_property(self):
        """
        Test route_type property
        """
        test_value = int(23)
        self.instance.route_type = test_value
        self.assertEqual(self.instance.route_type, test_value)
    
    def test_trip_property(self):
        """
        Test trip property
        """
        test_value = None
        self.instance.trip = test_value
        self.assertEqual(self.instance.trip, test_value)
    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'rewhibpwfcwgfdnmpxbm'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EntitySelector.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EntitySelector.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

