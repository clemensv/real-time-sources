"""
Test case for TollRate
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.tolls.tollrate import TollRate


class Test_TollRate(unittest.TestCase):
    """
    Test case for TollRate
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TollRate.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TollRate for testing
        """
        instance = TollRate(
            trip_name='jgoppaeuqyqyhrdssmhk',
            state_route='wmolsewkbqxasizbzidu',
            travel_direction='fuemqbblfdsxfobqjaib',
            current_toll=int(59),
            current_message='kmxaisnguknuiydkyqwn',
            time_updated='fzumrqhzoqvqcjrtyprq',
            start_location_name='ojvmfgvjxvhbrvkksakk',
            start_latitude=float(4.264500080812372),
            start_longitude=float(96.82119884475794),
            start_milepost=float(29.602245006435503),
            end_location_name='ithxmgyickdhkiglddhe',
            end_latitude=float(87.91344958828267),
            end_longitude=float(15.549879981038217),
            end_milepost=float(55.888186482112154)
        )
        return instance

    
    def test_trip_name_property(self):
        """
        Test trip_name property
        """
        test_value = 'jgoppaeuqyqyhrdssmhk'
        self.instance.trip_name = test_value
        self.assertEqual(self.instance.trip_name, test_value)
    
    def test_state_route_property(self):
        """
        Test state_route property
        """
        test_value = 'wmolsewkbqxasizbzidu'
        self.instance.state_route = test_value
        self.assertEqual(self.instance.state_route, test_value)
    
    def test_travel_direction_property(self):
        """
        Test travel_direction property
        """
        test_value = 'fuemqbblfdsxfobqjaib'
        self.instance.travel_direction = test_value
        self.assertEqual(self.instance.travel_direction, test_value)
    
    def test_current_toll_property(self):
        """
        Test current_toll property
        """
        test_value = int(59)
        self.instance.current_toll = test_value
        self.assertEqual(self.instance.current_toll, test_value)
    
    def test_current_message_property(self):
        """
        Test current_message property
        """
        test_value = 'kmxaisnguknuiydkyqwn'
        self.instance.current_message = test_value
        self.assertEqual(self.instance.current_message, test_value)
    
    def test_time_updated_property(self):
        """
        Test time_updated property
        """
        test_value = 'fzumrqhzoqvqcjrtyprq'
        self.instance.time_updated = test_value
        self.assertEqual(self.instance.time_updated, test_value)
    
    def test_start_location_name_property(self):
        """
        Test start_location_name property
        """
        test_value = 'ojvmfgvjxvhbrvkksakk'
        self.instance.start_location_name = test_value
        self.assertEqual(self.instance.start_location_name, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(4.264500080812372)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(96.82119884475794)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(29.602245006435503)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_end_location_name_property(self):
        """
        Test end_location_name property
        """
        test_value = 'ithxmgyickdhkiglddhe'
        self.instance.end_location_name = test_value
        self.assertEqual(self.instance.end_location_name, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(87.91344958828267)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(15.549879981038217)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(55.888186482112154)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TollRate.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TollRate.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

