"""
Test case for AvalancheBulletin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eaws_albina_mqtt_producer_data.avalanchebulletin import AvalancheBulletin
from eaws_albina_mqtt_producer_data.maxdangerratingenum import MaxDangerRatingenum
import datetime


class Test_AvalancheBulletin(unittest.TestCase):
    """
    Test case for AvalancheBulletin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AvalancheBulletin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AvalancheBulletin for testing
        """
        instance = AvalancheBulletin(
            region_id='jydhoyknrkasxsoawxsb',
            region_name='aomizlebyzxoserasdgp',
            bulletin_id='jhsdkvezowkkqqwpyjtb',
            publication_time=datetime.datetime.now(datetime.timezone.utc),
            valid_time_start=datetime.datetime.now(datetime.timezone.utc),
            valid_time_end=datetime.datetime.now(datetime.timezone.utc),
            lang='swvvdbzxrrbwgyimqdah',
            max_danger_rating=MaxDangerRatingenum.low,
            max_danger_rating_value=int(4),
            danger_ratings_json='lvcnjbblurzoujnucmcr',
            avalanche_problems_json='pmhmzlwojrrzecqpseox',
            tendency_type='izlvldrexuufzuyngqqd',
            danger_patterns_json='mbgjqfmxbfayjgvdvzzk',
            avalanche_activity_highlights='pytmagvqpxswnpwbvsvr',
            snowpack_structure_comment='sphbonndkxnzkhwwtffd',
            country='ouxtbdcaksaqtedlddli',
            danger_level='xzoafoxkzawnimgrdhrd'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'jydhoyknrkasxsoawxsb'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'aomizlebyzxoserasdgp'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_bulletin_id_property(self):
        """
        Test bulletin_id property
        """
        test_value = 'jhsdkvezowkkqqwpyjtb'
        self.instance.bulletin_id = test_value
        self.assertEqual(self.instance.bulletin_id, test_value)
    
    def test_publication_time_property(self):
        """
        Test publication_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.publication_time = test_value
        self.assertEqual(self.instance.publication_time, test_value)
    
    def test_valid_time_start_property(self):
        """
        Test valid_time_start property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_start = test_value
        self.assertEqual(self.instance.valid_time_start, test_value)
    
    def test_valid_time_end_property(self):
        """
        Test valid_time_end property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.valid_time_end = test_value
        self.assertEqual(self.instance.valid_time_end, test_value)
    
    def test_lang_property(self):
        """
        Test lang property
        """
        test_value = 'swvvdbzxrrbwgyimqdah'
        self.instance.lang = test_value
        self.assertEqual(self.instance.lang, test_value)
    
    def test_max_danger_rating_property(self):
        """
        Test max_danger_rating property
        """
        test_value = MaxDangerRatingenum.low
        self.instance.max_danger_rating = test_value
        self.assertEqual(self.instance.max_danger_rating, test_value)
    
    def test_max_danger_rating_value_property(self):
        """
        Test max_danger_rating_value property
        """
        test_value = int(4)
        self.instance.max_danger_rating_value = test_value
        self.assertEqual(self.instance.max_danger_rating_value, test_value)
    
    def test_danger_ratings_json_property(self):
        """
        Test danger_ratings_json property
        """
        test_value = 'lvcnjbblurzoujnucmcr'
        self.instance.danger_ratings_json = test_value
        self.assertEqual(self.instance.danger_ratings_json, test_value)
    
    def test_avalanche_problems_json_property(self):
        """
        Test avalanche_problems_json property
        """
        test_value = 'pmhmzlwojrrzecqpseox'
        self.instance.avalanche_problems_json = test_value
        self.assertEqual(self.instance.avalanche_problems_json, test_value)
    
    def test_tendency_type_property(self):
        """
        Test tendency_type property
        """
        test_value = 'izlvldrexuufzuyngqqd'
        self.instance.tendency_type = test_value
        self.assertEqual(self.instance.tendency_type, test_value)
    
    def test_danger_patterns_json_property(self):
        """
        Test danger_patterns_json property
        """
        test_value = 'mbgjqfmxbfayjgvdvzzk'
        self.instance.danger_patterns_json = test_value
        self.assertEqual(self.instance.danger_patterns_json, test_value)
    
    def test_avalanche_activity_highlights_property(self):
        """
        Test avalanche_activity_highlights property
        """
        test_value = 'pytmagvqpxswnpwbvsvr'
        self.instance.avalanche_activity_highlights = test_value
        self.assertEqual(self.instance.avalanche_activity_highlights, test_value)
    
    def test_snowpack_structure_comment_property(self):
        """
        Test snowpack_structure_comment property
        """
        test_value = 'sphbonndkxnzkhwwtffd'
        self.instance.snowpack_structure_comment = test_value
        self.assertEqual(self.instance.snowpack_structure_comment, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'ouxtbdcaksaqtedlddli'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_danger_level_property(self):
        """
        Test danger_level property
        """
        test_value = 'xzoafoxkzawnimgrdhrd'
        self.instance.danger_level = test_value
        self.assertEqual(self.instance.danger_level, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AvalancheBulletin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AvalancheBulletin.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

