"""
Test case for Species
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from laqn_london_producer_data.uk.kcl.laqn.species import Species


class Test_Species(unittest.TestCase):
    """
    Test case for Species
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Species.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Species for testing
        """
        instance = Species(
            species_code='cvvcmuzqjpejopkqgbnw',
            species_name='eogfrocxsbizhjvfqlhu',
            description='hjpbokzscbmjnyopfzoy',
            health_effect='jgzafjttglxldbjkerpy',
            link='sabgrvlctluajfnzvaxh'
        )
        return instance

    
    def test_species_code_property(self):
        """
        Test species_code property
        """
        test_value = 'cvvcmuzqjpejopkqgbnw'
        self.instance.species_code = test_value
        self.assertEqual(self.instance.species_code, test_value)
    
    def test_species_name_property(self):
        """
        Test species_name property
        """
        test_value = 'eogfrocxsbizhjvfqlhu'
        self.instance.species_name = test_value
        self.assertEqual(self.instance.species_name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'hjpbokzscbmjnyopfzoy'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_health_effect_property(self):
        """
        Test health_effect property
        """
        test_value = 'jgzafjttglxldbjkerpy'
        self.instance.health_effect = test_value
        self.assertEqual(self.instance.health_effect, test_value)
    
    def test_link_property(self):
        """
        Test link property
        """
        test_value = 'sabgrvlctluajfnzvaxh'
        self.instance.link = test_value
        self.assertEqual(self.instance.link, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Species.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
