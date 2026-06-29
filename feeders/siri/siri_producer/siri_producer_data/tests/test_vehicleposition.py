"""
Test case for VehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from siri_producer_data.vehicleposition import VehiclePosition
import datetime


class Test_VehiclePosition(unittest.TestCase):
    """
    Test case for VehiclePosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehiclePosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehiclePosition for testing
        """
        instance = VehiclePosition(
            operator_ref='humvtxkpxkxxmzrsfyut',
            vehicle_ref='ribzoxivwircrxwgjtpr',
            line_ref='ylfqnsfcasljxqprzfvm',
            direction_ref='xtbjwqfcmfobqaizyzhp',
            published_line_name='fuaxoaofuyugsceawfxs',
            origin_ref='ctpgeufcypvnvhoavarm',
            origin_name='vmmlszzofszkjxiekdqt',
            destination_ref='ykqrdnwmfmkucbiljvhc',
            destination_name='vozpubczhtjftbqxmshe',
            longitude=float(37.03169398230034),
            latitude=float(99.69318205827365),
            bearing=int(71),
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            valid_until_time=datetime.datetime.now(datetime.timezone.utc),
            block_ref='xunfrhzkszbhmkufqzzf',
            vehicle_journey_ref='utaaxktmxfsiyixvwkda',
            origin_aimed_departure_time=datetime.datetime.now(datetime.timezone.utc),
            data_frame_ref='fvequvyfwpahnnndeger',
            dated_vehicle_journey_ref='mhylokmgrmjzhejrwgsn',
            item_identifier='bqpghbimwxwuehflenwg'
        )
        return instance

    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'humvtxkpxkxxmzrsfyut'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_vehicle_ref_property(self):
        """
        Test vehicle_ref property
        """
        test_value = 'ribzoxivwircrxwgjtpr'
        self.instance.vehicle_ref = test_value
        self.assertEqual(self.instance.vehicle_ref, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'ylfqnsfcasljxqprzfvm'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'xtbjwqfcmfobqaizyzhp'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'fuaxoaofuyugsceawfxs'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_origin_ref_property(self):
        """
        Test origin_ref property
        """
        test_value = 'ctpgeufcypvnvhoavarm'
        self.instance.origin_ref = test_value
        self.assertEqual(self.instance.origin_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'vmmlszzofszkjxiekdqt'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_ref_property(self):
        """
        Test destination_ref property
        """
        test_value = 'ykqrdnwmfmkucbiljvhc'
        self.instance.destination_ref = test_value
        self.assertEqual(self.instance.destination_ref, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'vozpubczhtjftbqxmshe'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(37.03169398230034)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(99.69318205827365)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(71)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_recorded_at_time_property(self):
        """
        Test recorded_at_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.recorded_at_time = test_value
        self.assertEqual(self.instance.recorded_at_time, test_value)
    
    def test_valid_until_time_property(self):
        """
        Test valid_until_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_until_time = test_value
        self.assertEqual(self.instance.valid_until_time, test_value)
    
    def test_block_ref_property(self):
        """
        Test block_ref property
        """
        test_value = 'xunfrhzkszbhmkufqzzf'
        self.instance.block_ref = test_value
        self.assertEqual(self.instance.block_ref, test_value)
    
    def test_vehicle_journey_ref_property(self):
        """
        Test vehicle_journey_ref property
        """
        test_value = 'utaaxktmxfsiyixvwkda'
        self.instance.vehicle_journey_ref = test_value
        self.assertEqual(self.instance.vehicle_journey_ref, test_value)
    
    def test_origin_aimed_departure_time_property(self):
        """
        Test origin_aimed_departure_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.origin_aimed_departure_time = test_value
        self.assertEqual(self.instance.origin_aimed_departure_time, test_value)
    
    def test_data_frame_ref_property(self):
        """
        Test data_frame_ref property
        """
        test_value = 'fvequvyfwpahnnndeger'
        self.instance.data_frame_ref = test_value
        self.assertEqual(self.instance.data_frame_ref, test_value)
    
    def test_dated_vehicle_journey_ref_property(self):
        """
        Test dated_vehicle_journey_ref property
        """
        test_value = 'mhylokmgrmjzhejrwgsn'
        self.instance.dated_vehicle_journey_ref = test_value
        self.assertEqual(self.instance.dated_vehicle_journey_ref, test_value)
    
    def test_item_identifier_property(self):
        """
        Test item_identifier property
        """
        test_value = 'bqpghbimwxwuehflenwg'
        self.instance.item_identifier = test_value
        self.assertEqual(self.instance.item_identifier, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehiclePosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehiclePosition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

