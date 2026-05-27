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
            entity_id='bizithbjyzkjramqjkim',
            name='gedknazfxeoufdelbmpj',
            url='jappuxqpwnrtdsquzkni',
            locale='yjiiunlxljebshcomwtn',
            segment_id='acvivxyqvfeowstwexvz',
            segment_name='ffaoczdncvbuauwmqwvg',
            genre_id='xjymyaggglhzdmyvdqjz',
            genre_name='lssedowltcwpikqtdxah',
            subgenre_id='ruzokcfzakefqcdgaora',
            subgenre_name='sbpknparzotdlinqwggb'
        )
        return instance


    def test_entity_id_property(self):
        """
        Test entity_id property
        """
        test_value = 'bizithbjyzkjramqjkim'
        self.instance.entity_id = test_value
        self.assertEqual(self.instance.entity_id, test_value)

    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'gedknazfxeoufdelbmpj'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)

    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'jappuxqpwnrtdsquzkni'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)

    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'yjiiunlxljebshcomwtn'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)

    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'acvivxyqvfeowstwexvz'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)

    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'ffaoczdncvbuauwmqwvg'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)

    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'xjymyaggglhzdmyvdqjz'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)

    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'lssedowltcwpikqtdxah'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)

    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'ruzokcfzakefqcdgaora'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)

    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'sbpknparzotdlinqwggb'
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
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Attraction.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Attraction.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

