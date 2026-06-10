"""
Test case for TravelTimeRoute
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.traveltimes.traveltimeroute import TravelTimeRoute


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
            travel_time_id='vebkgzpxjtqufqarflni',
            name='nduhwcyvpphztlbmuatm',
            description='xpiwobdceozvpkjanhkt',
            distance=float(47.046755211633936),
            average_time=int(68),
            current_time=int(91),
            time_updated='ozqjqmdpfhpdrmlujkrd',
            start_description='vohtcdtzivpyvqlrtnzj',
            start_road_name='wvvhbwzhxnqrshloashi',
            start_direction='qzqxcybfjiwbbigoqckh',
            start_milepost=float(7.155288943835791),
            start_latitude=float(38.423348614271916),
            start_longitude=float(55.11195506805904),
            end_description='gffyqsdrcqcipjfeepcv',
            end_road_name='dmvowjiwdhppkjhnfznu',
            end_direction='ugxyfnufqhojwqjlldmi',
            end_milepost=float(58.33187443949402),
            end_latitude=float(18.930414643636674),
            end_longitude=float(4.6045656089767295)
        )
        return instance

    
    def test_travel_time_id_property(self):
        """
        Test travel_time_id property
        """
        test_value = 'vebkgzpxjtqufqarflni'
        self.instance.travel_time_id = test_value
        self.assertEqual(self.instance.travel_time_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'nduhwcyvpphztlbmuatm'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'xpiwobdceozvpkjanhkt'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_distance_property(self):
        """
        Test distance property
        """
        test_value = float(47.046755211633936)
        self.instance.distance = test_value
        self.assertEqual(self.instance.distance, test_value)
    
    def test_average_time_property(self):
        """
        Test average_time property
        """
        test_value = int(68)
        self.instance.average_time = test_value
        self.assertEqual(self.instance.average_time, test_value)
    
    def test_current_time_property(self):
        """
        Test current_time property
        """
        test_value = int(91)
        self.instance.current_time = test_value
        self.assertEqual(self.instance.current_time, test_value)
    
    def test_time_updated_property(self):
        """
        Test time_updated property
        """
        test_value = 'ozqjqmdpfhpdrmlujkrd'
        self.instance.time_updated = test_value
        self.assertEqual(self.instance.time_updated, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'vohtcdtzivpyvqlrtnzj'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'wvvhbwzhxnqrshloashi'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'qzqxcybfjiwbbigoqckh'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(7.155288943835791)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(38.423348614271916)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(55.11195506805904)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'gffyqsdrcqcipjfeepcv'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'dmvowjiwdhppkjhnfznu'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'ugxyfnufqhojwqjlldmi'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(58.33187443949402)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(18.930414643636674)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(4.6045656089767295)
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

