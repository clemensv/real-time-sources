"""
Test case for ParameterMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_producer_data.usgs.waterdata.parametermetadata import ParameterMetadata
from usgs_waterdata_producer_data.usgs.waterdata.point import Point


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
            id='xrpvpjtfexwcfjvwuqet',
            parameter_name='ofbqpurrutrszggylwsf',
            unit_of_measure='rkoruvqjabkpgpbvoxpx',
            parameter_group_code='xqexkujluxlnfxxutree',
            parameter_description='qixlertishztajprbhlm',
            medium='pigectcxrdtwcrgfjbse',
            statistical_basis='tfdymldtyinejdpjmwdl',
            time_basis='nifesffyveapilliiand',
            weight_basis='ubzddpzrgwdhjinxnntg',
            particle_size_basis='rrcnjqmusbflepxbtodh',
            sample_fraction='apdhsyclwrlbstjmcakv',
            temperature_basis='ocssikysdgfyovyuynom',
            epa_equivalence='lowcfqjtqkzkzcnbuhmj',
            geometry=None
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'xrpvpjtfexwcfjvwuqet'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_parameter_name_property(self):
        """
        Test parameter_name property
        """
        test_value = 'ofbqpurrutrszggylwsf'
        self.instance.parameter_name = test_value
        self.assertEqual(self.instance.parameter_name, test_value)
    
    def test_unit_of_measure_property(self):
        """
        Test unit_of_measure property
        """
        test_value = 'rkoruvqjabkpgpbvoxpx'
        self.instance.unit_of_measure = test_value
        self.assertEqual(self.instance.unit_of_measure, test_value)
    
    def test_parameter_group_code_property(self):
        """
        Test parameter_group_code property
        """
        test_value = 'xqexkujluxlnfxxutree'
        self.instance.parameter_group_code = test_value
        self.assertEqual(self.instance.parameter_group_code, test_value)
    
    def test_parameter_description_property(self):
        """
        Test parameter_description property
        """
        test_value = 'qixlertishztajprbhlm'
        self.instance.parameter_description = test_value
        self.assertEqual(self.instance.parameter_description, test_value)
    
    def test_medium_property(self):
        """
        Test medium property
        """
        test_value = 'pigectcxrdtwcrgfjbse'
        self.instance.medium = test_value
        self.assertEqual(self.instance.medium, test_value)
    
    def test_statistical_basis_property(self):
        """
        Test statistical_basis property
        """
        test_value = 'tfdymldtyinejdpjmwdl'
        self.instance.statistical_basis = test_value
        self.assertEqual(self.instance.statistical_basis, test_value)
    
    def test_time_basis_property(self):
        """
        Test time_basis property
        """
        test_value = 'nifesffyveapilliiand'
        self.instance.time_basis = test_value
        self.assertEqual(self.instance.time_basis, test_value)
    
    def test_weight_basis_property(self):
        """
        Test weight_basis property
        """
        test_value = 'ubzddpzrgwdhjinxnntg'
        self.instance.weight_basis = test_value
        self.assertEqual(self.instance.weight_basis, test_value)
    
    def test_particle_size_basis_property(self):
        """
        Test particle_size_basis property
        """
        test_value = 'rrcnjqmusbflepxbtodh'
        self.instance.particle_size_basis = test_value
        self.assertEqual(self.instance.particle_size_basis, test_value)
    
    def test_sample_fraction_property(self):
        """
        Test sample_fraction property
        """
        test_value = 'apdhsyclwrlbstjmcakv'
        self.instance.sample_fraction = test_value
        self.assertEqual(self.instance.sample_fraction, test_value)
    
    def test_temperature_basis_property(self):
        """
        Test temperature_basis property
        """
        test_value = 'ocssikysdgfyovyuynom'
        self.instance.temperature_basis = test_value
        self.assertEqual(self.instance.temperature_basis, test_value)
    
    def test_epa_equivalence_property(self):
        """
        Test epa_equivalence property
        """
        test_value = 'lowcfqjtqkzkzcnbuhmj'
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

