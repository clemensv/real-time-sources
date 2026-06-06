"""
Test case for Classification
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ticketmaster_amqp_producer_data.ticketmaster.reference.classification import Classification


class Test_Classification(unittest.TestCase):
    """
    Test case for Classification
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Classification.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Classification for testing
        """
        instance = Classification(
            entity_id='nhhrvnznjzbosyqjwduf',
            name='fiuozhgbhnuwbbxxdrfv',
            type='ajygzjiibicpzsmejqcu',
            primary_genre_id='deqjlwteuctlwgkrbuab',
            primary_genre_name='dboqrphxtjdjvyriacyz',
            primary_subgenre_id='axjeeaovbpqeruqimymd',
            primary_subgenre_name='poepbkbrutukvlhveggu'
        )
        return instance

    
    def test_entity_id_property(self):
        """
        Test entity_id property
        """
        test_value = 'nhhrvnznjzbosyqjwduf'
        self.instance.entity_id = test_value
        self.assertEqual(self.instance.entity_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'fiuozhgbhnuwbbxxdrfv'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'ajygzjiibicpzsmejqcu'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_primary_genre_id_property(self):
        """
        Test primary_genre_id property
        """
        test_value = 'deqjlwteuctlwgkrbuab'
        self.instance.primary_genre_id = test_value
        self.assertEqual(self.instance.primary_genre_id, test_value)
    
    def test_primary_genre_name_property(self):
        """
        Test primary_genre_name property
        """
        test_value = 'dboqrphxtjdjvyriacyz'
        self.instance.primary_genre_name = test_value
        self.assertEqual(self.instance.primary_genre_name, test_value)
    
    def test_primary_subgenre_id_property(self):
        """
        Test primary_subgenre_id property
        """
        test_value = 'axjeeaovbpqeruqimymd'
        self.instance.primary_subgenre_id = test_value
        self.assertEqual(self.instance.primary_subgenre_id, test_value)
    
    def test_primary_subgenre_name_property(self):
        """
        Test primary_subgenre_name property
        """
        test_value = 'poepbkbrutukvlhveggu'
        self.instance.primary_subgenre_name = test_value
        self.assertEqual(self.instance.primary_subgenre_name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Classification.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Classification.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

