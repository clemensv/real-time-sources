"""
Test case for VehiclePosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from uk_bods_siri_producer_data.vehicleposition import VehiclePosition
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
            operator_ref='dmorscbgprftmfvjmtla',
            vehicle_ref='febxvdawyrcqvbbmvlzl',
            line_ref='tvggmdycugjnxyhlqhud',
            direction_ref='agprdjgabienyqzyksbg',
            published_line_name='pxhghzswjloxtkkszqec',
            origin_ref='eujhxzkzbfzjyqnxrvmm',
            origin_name='lzzazotgbwfurajooizq',
            destination_ref='fhxmoxyjdtakscwvczdv',
            destination_name='uudyofpkhijhtbnqauqr',
            longitude=float(88.01654611038879),
            latitude=float(85.8723180725231),
            bearing=int(65),
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            valid_until_time=datetime.datetime.now(datetime.timezone.utc),
            block_ref='uruxfigdfcotaxxlgjst',
            vehicle_journey_ref='wnoxulcwmwblutjradmg',
            origin_aimed_departure_time=datetime.datetime.now(datetime.timezone.utc),
            data_frame_ref='kibxtjxqdozxnovjqejt',
            dated_vehicle_journey_ref='kvswgpqpkjcllzgyjwsq',
            item_identifier='gginlawpryfitpxapmea'
        )
        return instance

    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'dmorscbgprftmfvjmtla'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_vehicle_ref_property(self):
        """
        Test vehicle_ref property
        """
        test_value = 'febxvdawyrcqvbbmvlzl'
        self.instance.vehicle_ref = test_value
        self.assertEqual(self.instance.vehicle_ref, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'tvggmdycugjnxyhlqhud'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'agprdjgabienyqzyksbg'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'pxhghzswjloxtkkszqec'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_origin_ref_property(self):
        """
        Test origin_ref property
        """
        test_value = 'eujhxzkzbfzjyqnxrvmm'
        self.instance.origin_ref = test_value
        self.assertEqual(self.instance.origin_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'lzzazotgbwfurajooizq'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_ref_property(self):
        """
        Test destination_ref property
        """
        test_value = 'fhxmoxyjdtakscwvczdv'
        self.instance.destination_ref = test_value
        self.assertEqual(self.instance.destination_ref, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'uudyofpkhijhtbnqauqr'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(88.01654611038879)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(85.8723180725231)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(65)
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
        test_value = 'uruxfigdfcotaxxlgjst'
        self.instance.block_ref = test_value
        self.assertEqual(self.instance.block_ref, test_value)
    
    def test_vehicle_journey_ref_property(self):
        """
        Test vehicle_journey_ref property
        """
        test_value = 'wnoxulcwmwblutjradmg'
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
        test_value = 'kibxtjxqdozxnovjqejt'
        self.instance.data_frame_ref = test_value
        self.assertEqual(self.instance.data_frame_ref, test_value)
    
    def test_dated_vehicle_journey_ref_property(self):
        """
        Test dated_vehicle_journey_ref property
        """
        test_value = 'kvswgpqpkjcllzgyjwsq'
        self.instance.dated_vehicle_journey_ref = test_value
        self.assertEqual(self.instance.dated_vehicle_journey_ref, test_value)
    
    def test_item_identifier_property(self):
        """
        Test item_identifier property
        """
        test_value = 'gginlawpryfitpxapmea'
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

