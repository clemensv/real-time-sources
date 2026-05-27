"""
Test case for EstimatedCall
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.estimatedcall import EstimatedCall
import datetime


class Test_EstimatedCall(unittest.TestCase):
    """
    Test case for EstimatedCall
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EstimatedCall.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EstimatedCall for testing
        """
        instance = EstimatedCall(
            stop_point_ref='eidbqofjzjgkocpqhtwu',
            order=int(60),
            stop_point_name='wrojnyxhikmufaelvmzx',
            aimed_arrival_time=datetime.datetime.now(datetime.timezone.utc),
            expected_arrival_time=datetime.datetime.now(datetime.timezone.utc),
            aimed_departure_time=datetime.datetime.now(datetime.timezone.utc),
            expected_departure_time=datetime.datetime.now(datetime.timezone.utc),
            arrival_status='upnqndywvnozkdweahfd',
            departure_status='bfegjygblhbeuqqyhlcf',
            departure_platform_name='tdqzggipagdjncriwajj',
            arrival_boarding_activity='pestmffvzvybxmqghuwt',
            departure_boarding_activity='bcfeqctlukietnazgdcj',
            is_cancellation=True,
            is_extra_stop=False
        )
        return instance

    
    def test_stop_point_ref_property(self):
        """
        Test stop_point_ref property
        """
        test_value = 'eidbqofjzjgkocpqhtwu'
        self.instance.stop_point_ref = test_value
        self.assertEqual(self.instance.stop_point_ref, test_value)
    
    def test_order_property(self):
        """
        Test order property
        """
        test_value = int(60)
        self.instance.order = test_value
        self.assertEqual(self.instance.order, test_value)
    
    def test_stop_point_name_property(self):
        """
        Test stop_point_name property
        """
        test_value = 'wrojnyxhikmufaelvmzx'
        self.instance.stop_point_name = test_value
        self.assertEqual(self.instance.stop_point_name, test_value)
    
    def test_aimed_arrival_time_property(self):
        """
        Test aimed_arrival_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.aimed_arrival_time = test_value
        self.assertEqual(self.instance.aimed_arrival_time, test_value)
    
    def test_expected_arrival_time_property(self):
        """
        Test expected_arrival_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expected_arrival_time = test_value
        self.assertEqual(self.instance.expected_arrival_time, test_value)
    
    def test_aimed_departure_time_property(self):
        """
        Test aimed_departure_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.aimed_departure_time = test_value
        self.assertEqual(self.instance.aimed_departure_time, test_value)
    
    def test_expected_departure_time_property(self):
        """
        Test expected_departure_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expected_departure_time = test_value
        self.assertEqual(self.instance.expected_departure_time, test_value)
    
    def test_arrival_status_property(self):
        """
        Test arrival_status property
        """
        test_value = 'upnqndywvnozkdweahfd'
        self.instance.arrival_status = test_value
        self.assertEqual(self.instance.arrival_status, test_value)
    
    def test_departure_status_property(self):
        """
        Test departure_status property
        """
        test_value = 'bfegjygblhbeuqqyhlcf'
        self.instance.departure_status = test_value
        self.assertEqual(self.instance.departure_status, test_value)
    
    def test_departure_platform_name_property(self):
        """
        Test departure_platform_name property
        """
        test_value = 'tdqzggipagdjncriwajj'
        self.instance.departure_platform_name = test_value
        self.assertEqual(self.instance.departure_platform_name, test_value)
    
    def test_arrival_boarding_activity_property(self):
        """
        Test arrival_boarding_activity property
        """
        test_value = 'pestmffvzvybxmqghuwt'
        self.instance.arrival_boarding_activity = test_value
        self.assertEqual(self.instance.arrival_boarding_activity, test_value)
    
    def test_departure_boarding_activity_property(self):
        """
        Test departure_boarding_activity property
        """
        test_value = 'bcfeqctlukietnazgdcj'
        self.instance.departure_boarding_activity = test_value
        self.assertEqual(self.instance.departure_boarding_activity, test_value)
    
    def test_is_cancellation_property(self):
        """
        Test is_cancellation property
        """
        test_value = True
        self.instance.is_cancellation = test_value
        self.assertEqual(self.instance.is_cancellation, test_value)
    
    def test_is_extra_stop_property(self):
        """
        Test is_extra_stop property
        """
        test_value = False
        self.instance.is_extra_stop = test_value
        self.assertEqual(self.instance.is_extra_stop, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EstimatedCall.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EstimatedCall.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EstimatedCall.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

