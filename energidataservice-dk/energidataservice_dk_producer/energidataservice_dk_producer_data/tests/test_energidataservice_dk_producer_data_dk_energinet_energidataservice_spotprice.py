"""
Test case for SpotPrice
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energidataservice_dk_producer_data.dk.energinet.energidataservice.spotprice import SpotPrice


class Test_SpotPrice(unittest.TestCase):
    """
    Test case for SpotPrice
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpotPrice.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpotPrice for testing
        """
        instance = SpotPrice(
            hour_utc='unsdloacoltzhjxdgpul',
            hour_dk='prvsejxrbunqknyceeza',
            price_area='auirdnbvwvgokqynbgds',
            spot_price_dkk=float(6.936608448145243),
            spot_price_eur=float(47.34649045557164)
        )
        return instance

    
    def test_hour_utc_property(self):
        """
        Test hour_utc property
        """
        test_value = 'unsdloacoltzhjxdgpul'
        self.instance.hour_utc = test_value
        self.assertEqual(self.instance.hour_utc, test_value)
    
    def test_hour_dk_property(self):
        """
        Test hour_dk property
        """
        test_value = 'prvsejxrbunqknyceeza'
        self.instance.hour_dk = test_value
        self.assertEqual(self.instance.hour_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'auirdnbvwvgokqynbgds'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_spot_price_dkk_property(self):
        """
        Test spot_price_dkk property
        """
        test_value = float(6.936608448145243)
        self.instance.spot_price_dkk = test_value
        self.assertEqual(self.instance.spot_price_dkk, test_value)
    
    def test_spot_price_eur_property(self):
        """
        Test spot_price_eur property
        """
        test_value = float(47.34649045557164)
        self.instance.spot_price_eur = test_value
        self.assertEqual(self.instance.spot_price_eur, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpotPrice.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
