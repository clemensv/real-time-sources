"""
Test case for TravelTimeRoute
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.traveltimes.traveltimeroute import TravelTimeRoute


class Test_TravelTimeRoute(unittest.TestCase):
    """
    Test case for TravelTimeRoute
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TravelTimeRoute.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TravelTimeRoute for testing
        """
        instance = TravelTimeRoute(
            travel_time_id='vakuzokyxpraoxqqhghy',
            name='cqaycdkxicqenyawikvy',
            description='kgpvxfebgmgcvpiwvmhi',
            distance=float(91.27570635010272),
            average_time=int(100),
            current_time=int(10),
            time_updated='naqozqxflrxscjkxpang',
            start_description='zbvzurgnnikgiuirxako',
            start_road_name='wbsdwggwwhjwaxpviyqg',
            start_direction='szxozpxvxsqkypbcprgg',
            start_milepost=float(92.73103988135719),
            start_latitude=float(30.66179498785496),
            start_longitude=float(35.935969823721905),
            end_description='elhoeanjpqfecdzujheg',
            end_road_name='xhfalzjwpphsglmpxczc',
            end_direction='kokxqgmwvrayhookrvqb',
            end_milepost=float(19.483561535412043),
            end_latitude=float(12.69646035360129),
            end_longitude=float(33.812246486290256)
        )
        return instance

    
    def test_travel_time_id_property(self):
        """
        Test travel_time_id property
        """
        test_value = 'vakuzokyxpraoxqqhghy'
        self.instance.travel_time_id = test_value
        self.assertEqual(self.instance.travel_time_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'cqaycdkxicqenyawikvy'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'kgpvxfebgmgcvpiwvmhi'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_distance_property(self):
        """
        Test distance property
        """
        test_value = float(91.27570635010272)
        self.instance.distance = test_value
        self.assertEqual(self.instance.distance, test_value)
    
    def test_average_time_property(self):
        """
        Test average_time property
        """
        test_value = int(100)
        self.instance.average_time = test_value
        self.assertEqual(self.instance.average_time, test_value)
    
    def test_current_time_property(self):
        """
        Test current_time property
        """
        test_value = int(10)
        self.instance.current_time = test_value
        self.assertEqual(self.instance.current_time, test_value)
    
    def test_time_updated_property(self):
        """
        Test time_updated property
        """
        test_value = 'naqozqxflrxscjkxpang'
        self.instance.time_updated = test_value
        self.assertEqual(self.instance.time_updated, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'zbvzurgnnikgiuirxako'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'wbsdwggwwhjwaxpviyqg'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'szxozpxvxsqkypbcprgg'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(92.73103988135719)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(30.66179498785496)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(35.935969823721905)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'elhoeanjpqfecdzujheg'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'xhfalzjwpphsglmpxczc'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'kokxqgmwvrayhookrvqb'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(19.483561535412043)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(12.69646035360129)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(33.812246486290256)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TravelTimeRoute.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TravelTimeRoute.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

