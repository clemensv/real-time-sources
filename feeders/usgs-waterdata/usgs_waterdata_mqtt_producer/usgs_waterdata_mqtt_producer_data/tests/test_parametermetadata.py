"""
Test case for ParameterMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_mqtt_producer_data.usgs.waterdata.parametermetadata import ParameterMetadata
from usgs_waterdata_mqtt_producer_data.usgs.waterdata.point import Point


class Test_ParameterMetadata(unittest.TestCase):
    """
    Test case for ParameterMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ParameterMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ParameterMetadata for testing
        """
        instance = ParameterMetadata(
            id='vekzuqoyngixhucvntak',
            parameter_name='jmmgymygipfhyeffskzh',
            unit_of_measure='agbcflaidffnztznfxpp',
            parameter_group_code='xfninyvrzyraiopokajr',
            parameter_description='zcrwzxktrlmwigmjjtkj',
            medium='eiolubelegtvgnjzpobt',
            statistical_basis='djtjzjhvuzfedmeufhfd',
            time_basis='wtzmozmmnpaybngtcecg',
            weight_basis='eexgruxsziqfppixqalq',
            particle_size_basis='qcsepzltljomauxivjrw',
            sample_fraction='vhjkfzdfcnrfmiqfqcpv',
            temperature_basis='axedaoibpcbwtekizzpk',
            epa_equivalence='vjllhghwaveqbmyswgdw',
            geometry=None
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'vekzuqoyngixhucvntak'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'jmmgymygipfhyeffskzh'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_unit_of_measure_property(self):
        """
        Test unit_of_measure property
        """
        test_value = 'agbcflaidffnztznfxpp'
        self.instance.unit_of_measure = test_value
        self.assertEqual(self.instance.unit_of_measure, test_value)
    
    def test_parameter_group_code_property(self):
        """
        Test parameter_group_code property
        """
        test_value = 'xfninyvrzyraiopokajr'
        self.instance.parameter_group_code = test_value
        self.assertEqual(self.instance.parameter_group_code, test_value)
    
    def test_parameter_description_property(self):
        """
        Test parameter_description property
        """
        test_value = 'zcrwzxktrlmwigmjjtkj'
        self.instance.parameter_description = test_value
        self.assertEqual(self.instance.parameter_description, test_value)
    
    def test_medium_property(self):
        """
        Test medium property
        """
        test_value = 'eiolubelegtvgnjzpobt'
        self.instance.medium = test_value
        self.assertEqual(self.instance.medium, test_value)
    
    def test_statistical_basis_property(self):
        """
        Test statistical_basis property
        """
        test_value = 'djtjzjhvuzfedmeufhfd'
        self.instance.statistical_basis = test_value
        self.assertEqual(self.instance.statistical_basis, test_value)
    
    def test_time_basis_property(self):
        """
        Test time_basis property
        """
        test_value = 'wtzmozmmnpaybngtcecg'
        self.instance.time_basis = test_value
        self.assertEqual(self.instance.time_basis, test_value)
    
    def test_weight_basis_property(self):
        """
        Test weight_basis property
        """
        test_value = 'eexgruxsziqfppixqalq'
        self.instance.weight_basis = test_value
        self.assertEqual(self.instance.weight_basis, test_value)
    
    def test_particle_size_basis_property(self):
        """
        Test particle_size_basis property
        """
        test_value = 'qcsepzltljomauxivjrw'
        self.instance.particle_size_basis = test_value
        self.assertEqual(self.instance.particle_size_basis, test_value)
    
    def test_sample_fraction_property(self):
        """
        Test sample_fraction property
        """
        test_value = 'vhjkfzdfcnrfmiqfqcpv'
        self.instance.sample_fraction = test_value
        self.assertEqual(self.instance.sample_fraction, test_value)
    
    def test_temperature_basis_property(self):
        """
        Test temperature_basis property
        """
        test_value = 'axedaoibpcbwtekizzpk'
        self.instance.temperature_basis = test_value
        self.assertEqual(self.instance.temperature_basis, test_value)
    
    def test_epa_equivalence_property(self):
        """
        Test epa_equivalence property
        """
        test_value = 'vjllhghwaveqbmyswgdw'
        self.instance.epa_equivalence = test_value
        self.assertEqual(self.instance.epa_equivalence, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = None
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ParameterMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ParameterMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

