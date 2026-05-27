"""
Test case for EstimatedCall
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.estimatedcall import EstimatedCall


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
            stop_point_ref='uawungjueqdnhargzira',
            order=int(15),
            stop_point_name='gbbqkjnzatctamcqqvoa',
            aimed_arrival_time='btoiwasuplcpmqsjwyju',
            expected_arrival_time='maoxdqplbacytffmmjkq',
            aimed_departure_time='ebztikrwtyodjpjptihx',
            expected_departure_time='lqlyyxltzrzthnnspmxw',
            arrival_status='xjyruywaadbufnjplioa',
            departure_status='xsajynbmcvwfgmozypva',
            departure_platform_name='ksdyqltmqfzhfbuotttp',
            arrival_boarding_activity='iohaxqfmtiuimlsanbbs',
            departure_boarding_activity='ujprfqxtoaxowuollsyo',
            is_cancellation=True,
            is_extra_stop=False
        )
        return instance

    
    def test_stop_point_ref_property(self):
        """
        Test stop_point_ref property
        """
        test_value = 'uawungjueqdnhargzira'
        self.instance.stop_point_ref = test_value
        self.assertEqual(self.instance.stop_point_ref, test_value)
    
    def test_order_property(self):
        """
        Test order property
        """
        test_value = int(15)
        self.instance.order = test_value
        self.assertEqual(self.instance.order, test_value)
    
    def test_stop_point_name_property(self):
        """
        Test stop_point_name property
        """
        test_value = 'gbbqkjnzatctamcqqvoa'
        self.instance.stop_point_name = test_value
        self.assertEqual(self.instance.stop_point_name, test_value)
    
    def test_aimed_arrival_time_property(self):
        """
        Test aimed_arrival_time property
        """
        test_value = 'btoiwasuplcpmqsjwyju'
        self.instance.aimed_arrival_time = test_value
        self.assertEqual(self.instance.aimed_arrival_time, test_value)
    
    def test_expected_arrival_time_property(self):
        """
        Test expected_arrival_time property
        """
        test_value = 'maoxdqplbacytffmmjkq'
        self.instance.expected_arrival_time = test_value
        self.assertEqual(self.instance.expected_arrival_time, test_value)
    
    def test_aimed_departure_time_property(self):
        """
        Test aimed_departure_time property
        """
        test_value = 'ebztikrwtyodjpjptihx'
        self.instance.aimed_departure_time = test_value
        self.assertEqual(self.instance.aimed_departure_time, test_value)
    
    def test_expected_departure_time_property(self):
        """
        Test expected_departure_time property
        """
        test_value = 'lqlyyxltzrzthnnspmxw'
        self.instance.expected_departure_time = test_value
        self.assertEqual(self.instance.expected_departure_time, test_value)
    
    def test_arrival_status_property(self):
        """
        Test arrival_status property
        """
        test_value = 'xjyruywaadbufnjplioa'
        self.instance.arrival_status = test_value
        self.assertEqual(self.instance.arrival_status, test_value)
    
    def test_departure_status_property(self):
        """
        Test departure_status property
        """
        test_value = 'xsajynbmcvwfgmozypva'
        self.instance.departure_status = test_value
        self.assertEqual(self.instance.departure_status, test_value)
    
    def test_departure_platform_name_property(self):
        """
        Test departure_platform_name property
        """
        test_value = 'ksdyqltmqfzhfbuotttp'
        self.instance.departure_platform_name = test_value
        self.assertEqual(self.instance.departure_platform_name, test_value)
    
    def test_arrival_boarding_activity_property(self):
        """
        Test arrival_boarding_activity property
        """
        test_value = 'iohaxqfmtiuimlsanbbs'
        self.instance.arrival_boarding_activity = test_value
        self.assertEqual(self.instance.arrival_boarding_activity, test_value)
    
    def test_departure_boarding_activity_property(self):
        """
        Test departure_boarding_activity property
        """
        test_value = 'ujprfqxtoaxowuollsyo'
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
