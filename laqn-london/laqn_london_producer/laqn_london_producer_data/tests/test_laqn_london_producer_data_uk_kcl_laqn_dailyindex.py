"""
Test case for DailyIndex
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_producer_data.uk.kcl.laqn.dailyindex import DailyIndex


class Test_DailyIndex(unittest.TestCase):
    """
    Test case for DailyIndex
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DailyIndex.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DailyIndex for testing
        """
        instance = DailyIndex(
            site_code='xtptnlzzfaoclffdvpvl',
            bulletin_date='kvxwfpbksybvkwvvtluq',
            species_code='jsrwzjpnwwicqiysehlk',
            air_quality_index=int(22),
            air_quality_band='sjprljtlqrjidwxdjxvj',
            index_source='tobkkdnqwcydjvidemjm'
        )
        return instance

    
    def test_site_code_property(self):
        """
        Test site_code property
        """
        test_value = 'xtptnlzzfaoclffdvpvl'
        self.instance.site_code = test_value
        self.assertEqual(self.instance.site_code, test_value)
    
    def test_bulletin_date_property(self):
        """
        Test bulletin_date property
        """
        test_value = 'kvxwfpbksybvkwvvtluq'
        self.instance.bulletin_date = test_value
        self.assertEqual(self.instance.bulletin_date, test_value)
    
    def test_species_code_property(self):
        """
        Test species_code property
        """
        test_value = 'jsrwzjpnwwicqiysehlk'
        self.instance.species_code = test_value
        self.assertEqual(self.instance.species_code, test_value)
    
    def test_air_quality_index_property(self):
        """
        Test air_quality_index property
        """
        test_value = int(22)
        self.instance.air_quality_index = test_value
        self.assertEqual(self.instance.air_quality_index, test_value)
    
    def test_air_quality_band_property(self):
        """
        Test air_quality_band property
        """
        test_value = 'sjprljtlqrjidwxdjxvj'
        self.instance.air_quality_band = test_value
        self.assertEqual(self.instance.air_quality_band, test_value)
    
    def test_index_source_property(self):
        """
        Test index_source property
        """
        test_value = 'tobkkdnqwcydjvidemjm'
        self.instance.index_source = test_value
        self.assertEqual(self.instance.index_source, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DailyIndex.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
