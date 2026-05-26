"""
Test case for Attraction
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ticketmaster_producer_data.ticketmaster.reference.attraction import Attraction


class Test_Attraction(unittest.TestCase):
    """
    Test case for Attraction
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Attraction.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Attraction for testing
        """
        instance = Attraction(
            entity_id='witmeytquggeydymtzwv',
            name='wbxrlvgpljbeiuqlimvb',
            url='qqsatbczrskvcugleyxs',
            locale='pnapwfcdznmvujbifvlk',
            segment_id='qmkgwsokrqssqphwjmci',
            segment_name='uhwpvjhlqyhljfblzzsj',
            genre_id='jpjbfnrbsazeipemhgjf',
            genre_name='rrlqxgdqcbxshadppxje',
            subgenre_id='igjruchfffppaevkqmrn',
            subgenre_name='gfzlwujduljwdmxcbhez'
        )
        return instance


    def test_entity_id_property(self):
        """
        Test entity_id property
        """
        test_value = 'witmeytquggeydymtzwv'
        self.instance.entity_id = test_value
        self.assertEqual(self.instance.entity_id, test_value)

    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'wbxrlvgpljbeiuqlimvb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)

    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'qqsatbczrskvcugleyxs'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)

    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'pnapwfcdznmvujbifvlk'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)

    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'qmkgwsokrqssqphwjmci'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)

    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'uhwpvjhlqyhljfblzzsj'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)

    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'jpjbfnrbsazeipemhgjf'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)

    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'rrlqxgdqcbxshadppxje'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)

    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'igjruchfffppaevkqmrn'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)

    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'gfzlwujduljwdmxcbhez'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Attraction.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
