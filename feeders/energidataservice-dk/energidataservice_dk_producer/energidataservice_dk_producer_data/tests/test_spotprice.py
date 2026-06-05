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
            hour_utc='rbpbgehbdjcnafyqbynv',
            hour_dk='boaummgkuvtyltqorrcj',
            price_area='mfupwrdacegmscrobnxm',
            spot_price_dkk=float(34.58868710123683),
            spot_price_eur=float(42.17784524623504)
        )
        return instance

    
    def test_hour_utc_property(self):
        """
        Test hour_utc property
        """
        test_value = 'rbpbgehbdjcnafyqbynv'
        self.instance.hour_utc = test_value
        self.assertEqual(self.instance.hour_utc, test_value)
    
    def test_hour_dk_property(self):
        """
        Test hour_dk property
        """
        test_value = 'boaummgkuvtyltqorrcj'
        self.instance.hour_dk = test_value
        self.assertEqual(self.instance.hour_dk, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'mfupwrdacegmscrobnxm'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_spot_price_dkk_property(self):
        """
        Test spot_price_dkk property
        """
        test_value = float(34.58868710123683)
        self.instance.spot_price_dkk = test_value
        self.assertEqual(self.instance.spot_price_dkk, test_value)
    
    def test_spot_price_eur_property(self):
        """
        Test spot_price_eur property
        """
        test_value = float(42.17784524623504)
        self.instance.spot_price_eur = test_value
        self.assertEqual(self.instance.spot_price_eur, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpotPrice.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SpotPrice.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

