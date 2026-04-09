"""
Test case for SpotPrice
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energy_charts_producer_data.info.energy_charts.spotprice import SpotPrice
import datetime


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
            country='lfjuuhoxxovvmodlwaez',
            bidding_zone='kpszwolpdgbjniuaxwik',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            unix_seconds=int(56),
            price_eur_per_mwh=float(17.748353935899786),
            unit='lfomkpkypgsibpwcdbvh'
        )
        return instance

    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'lfjuuhoxxovvmodlwaez'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_bidding_zone_property(self):
        """
        Test bidding_zone property
        """
        test_value = 'kpszwolpdgbjniuaxwik'
        self.instance.bidding_zone = test_value
        self.assertEqual(self.instance.bidding_zone, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_unix_seconds_property(self):
        """
        Test unix_seconds property
        """
        test_value = int(56)
        self.instance.unix_seconds = test_value
        self.assertEqual(self.instance.unix_seconds, test_value)
    
    def test_price_eur_per_mwh_property(self):
        """
        Test price_eur_per_mwh property
        """
        test_value = float(17.748353935899786)
        self.instance.price_eur_per_mwh = test_value
        self.assertEqual(self.instance.price_eur_per_mwh, test_value)
    
    def test_unit_property(self):
        """
        Test unit property
        """
        test_value = 'lfomkpkypgsibpwcdbvh'
        self.instance.unit = test_value
        self.assertEqual(self.instance.unit, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SpotPrice.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
