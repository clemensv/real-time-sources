"""
Test case for PtSituationElement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.ptsituationelement import PtSituationElement
from entur_norway_producer_data.no.entur.validityperiod import ValidityPeriod
import datetime


class Test_PtSituationElement(unittest.TestCase):
    """
    Test case for PtSituationElement
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PtSituationElement.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PtSituationElement for testing
        """
        instance = PtSituationElement(
            situation_number='wysmzfvbvnxzzpltuoqm',
            version='jssltfnzxzwfijjhhhkg',
            creation_time=datetime.datetime.now(datetime.timezone.utc),
            source_type='kwohqjjyhtjibuenirwi',
            source_name='clsjuvcqggnrmnfxdbsz',
            progress='pryrhyvnfyomvdtpbfzn',
            severity='axdzeycdndejbkahngaz',
            keywords='dgnzdciwtnknoncgfxop',
            summary='lfbztrwqebaklwdfxmsf',
            description='glvptjvbnlyvxmhmpsgo',
            affects_line_refs=['cmwgtrzzhwqdivqfpcta'],
            affects_stop_point_refs=['vqhwbrihpdavvsiwrovq'],
            validity_periods=[None]
        )
        return instance

    
    def test_situation_number_property(self):
        """
        Test situation_number property
        """
        test_value = 'wysmzfvbvnxzzpltuoqm'
        self.instance.situation_number = test_value
        self.assertEqual(self.instance.situation_number, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'jssltfnzxzwfijjhhhkg'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_creation_time_property(self):
        """
        Test creation_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.creation_time = test_value
        self.assertEqual(self.instance.creation_time, test_value)
    
    def test_source_type_property(self):
        """
        Test source_type property
        """
        test_value = 'kwohqjjyhtjibuenirwi'
        self.instance.source_type = test_value
        self.assertEqual(self.instance.source_type, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'clsjuvcqggnrmnfxdbsz'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_progress_property(self):
        """
        Test progress property
        """
        test_value = 'pryrhyvnfyomvdtpbfzn'
        self.instance.progress = test_value
        self.assertEqual(self.instance.progress, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'axdzeycdndejbkahngaz'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_keywords_property(self):
        """
        Test keywords property
        """
        test_value = 'dgnzdciwtnknoncgfxop'
        self.instance.keywords = test_value
        self.assertEqual(self.instance.keywords, test_value)
    
    def test_summary_property(self):
        """
        Test summary property
        """
        test_value = 'lfbztrwqebaklwdfxmsf'
        self.instance.summary = test_value
        self.assertEqual(self.instance.summary, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'glvptjvbnlyvxmhmpsgo'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_affects_line_refs_property(self):
        """
        Test affects_line_refs property
        """
        test_value = ['cmwgtrzzhwqdivqfpcta']
        self.instance.affects_line_refs = test_value
        self.assertEqual(self.instance.affects_line_refs, test_value)
    
    def test_affects_stop_point_refs_property(self):
        """
        Test affects_stop_point_refs property
        """
        test_value = ['vqhwbrihpdavvsiwrovq']
        self.instance.affects_stop_point_refs = test_value
        self.assertEqual(self.instance.affects_stop_point_refs, test_value)
    
    def test_validity_periods_property(self):
        """
        Test validity_periods property
        """
        test_value = [None]
        self.instance.validity_periods = test_value
        self.assertEqual(self.instance.validity_periods, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PtSituationElement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PtSituationElement.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

