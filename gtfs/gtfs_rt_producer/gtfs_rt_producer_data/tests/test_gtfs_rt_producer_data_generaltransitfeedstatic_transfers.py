"""
Test case for Transfers
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.transfers import Transfers


class Test_Transfers(unittest.TestCase):
    """
    Test case for Transfers
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Transfers.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Transfers for testing
        """
        instance = Transfers(
            fromStopId='yialgjxygudadtgfwudq',
            toStopId='rvsscgxtszlpmemfauyr',
            transferType=int(25),
            minTransferTime=int(51)
        )
        return instance

    
    def test_fromStopId_property(self):
        """
        Test fromStopId property
        """
        test_value = 'yialgjxygudadtgfwudq'
        self.instance.fromStopId = test_value
        self.assertEqual(self.instance.fromStopId, test_value)
    
    def test_toStopId_property(self):
        """
        Test toStopId property
        """
        test_value = 'rvsscgxtszlpmemfauyr'
        self.instance.toStopId = test_value
        self.assertEqual(self.instance.toStopId, test_value)
    
    def test_transferType_property(self):
        """
        Test transferType property
        """
        test_value = int(25)
        self.instance.transferType = test_value
        self.assertEqual(self.instance.transferType, test_value)
    
    def test_minTransferTime_property(self):
        """
        Test minTransferTime property
        """
        test_value = int(51)
        self.instance.minTransferTime = test_value
        self.assertEqual(self.instance.minTransferTime, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Transfers.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
