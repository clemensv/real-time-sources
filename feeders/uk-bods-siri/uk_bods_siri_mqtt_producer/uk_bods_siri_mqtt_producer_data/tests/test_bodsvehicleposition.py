"""
Test case for BodsVehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_bods_siri_mqtt_producer_data.bodsvehicleposition import BodsVehiclePosition


class Test_BodsVehiclePosition(unittest.TestCase):
    """
    Test case for BodsVehiclePosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BodsVehiclePosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BodsVehiclePosition for testing
        """
        instance = BodsVehiclePosition(
            operator_ref='zlbnpydzowmgacycoyqx',
            vehicle_ref='bejfoobkphkebthxkemu',
            line_ref='zjjvhhwzqiopmawhljgv',
            direction_ref='mfegtucqijbxqjjyhbez',
            published_line_name='wgfuvqhaisrwtgeweltc',
            origin_ref='zifemggiztkhvhbgkfyu',
            origin_name='rfafndmtazgfwayrgcrt',
            destination_ref='dkpevaqsyfzbneojweje',
            destination_name='jkzrmevnqcrhmqmyakfm',
            longitude=float(38.42086060295868),
            latitude=float(58.09528113767166),
            bearing=int(7),
            recorded_at_time='hsgeoqclgbbnqkjimbjq',
            valid_until_time='ykjdpktsjoexqeaisaxd',
            block_ref='vsjxzvxnejluximpamib',
            vehicle_journey_ref='xyrobuedskrwyuttgmkk',
            origin_aimed_departure_time='vnmoeunngjlmjknoxtay',
            data_frame_ref='xqoaqjfhqzjwozxgbwfh',
            dated_vehicle_journey_ref='fmxrtzpvfbzrwohlqijy',
            item_identifier='lgovqhqxwgayakahrlgc'
        )
        return instance

    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'zlbnpydzowmgacycoyqx'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_vehicle_ref_property(self):
        """
        Test vehicle_ref property
        """
        test_value = 'bejfoobkphkebthxkemu'
        self.instance.vehicle_ref = test_value
        self.assertEqual(self.instance.vehicle_ref, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'zjjvhhwzqiopmawhljgv'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'mfegtucqijbxqjjyhbez'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'wgfuvqhaisrwtgeweltc'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_origin_ref_property(self):
        """
        Test origin_ref property
        """
        test_value = 'zifemggiztkhvhbgkfyu'
        self.instance.origin_ref = test_value
        self.assertEqual(self.instance.origin_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'rfafndmtazgfwayrgcrt'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_ref_property(self):
        """
        Test destination_ref property
        """
        test_value = 'dkpevaqsyfzbneojweje'
        self.instance.destination_ref = test_value
        self.assertEqual(self.instance.destination_ref, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'jkzrmevnqcrhmqmyakfm'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(38.42086060295868)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(58.09528113767166)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(7)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_recorded_at_time_property(self):
        """
        Test recorded_at_time property
        """
        test_value = 'hsgeoqclgbbnqkjimbjq'
        self.instance.recorded_at_time = test_value
        self.assertEqual(self.instance.recorded_at_time, test_value)
    
    def test_valid_until_time_property(self):
        """
        Test valid_until_time property
        """
        test_value = 'ykjdpktsjoexqeaisaxd'
        self.instance.valid_until_time = test_value
        self.assertEqual(self.instance.valid_until_time, test_value)
    
    def test_block_ref_property(self):
        """
        Test block_ref property
        """
        test_value = 'vsjxzvxnejluximpamib'
        self.instance.block_ref = test_value
        self.assertEqual(self.instance.block_ref, test_value)
    
    def test_vehicle_journey_ref_property(self):
        """
        Test vehicle_journey_ref property
        """
        test_value = 'xyrobuedskrwyuttgmkk'
        self.instance.vehicle_journey_ref = test_value
        self.assertEqual(self.instance.vehicle_journey_ref, test_value)
    
    def test_origin_aimed_departure_time_property(self):
        """
        Test origin_aimed_departure_time property
        """
        test_value = 'vnmoeunngjlmjknoxtay'
        self.instance.origin_aimed_departure_time = test_value
        self.assertEqual(self.instance.origin_aimed_departure_time, test_value)
    
    def test_data_frame_ref_property(self):
        """
        Test data_frame_ref property
        """
        test_value = 'xqoaqjfhqzjwozxgbwfh'
        self.instance.data_frame_ref = test_value
        self.assertEqual(self.instance.data_frame_ref, test_value)
    
    def test_dated_vehicle_journey_ref_property(self):
        """
        Test dated_vehicle_journey_ref property
        """
        test_value = 'fmxrtzpvfbzrwohlqijy'
        self.instance.dated_vehicle_journey_ref = test_value
        self.assertEqual(self.instance.dated_vehicle_journey_ref, test_value)
    
    def test_item_identifier_property(self):
        """
        Test item_identifier property
        """
        test_value = 'lgovqhqxwgayakahrlgc'
        self.instance.item_identifier = test_value
        self.assertEqual(self.instance.item_identifier, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BodsVehiclePosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BodsVehiclePosition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

