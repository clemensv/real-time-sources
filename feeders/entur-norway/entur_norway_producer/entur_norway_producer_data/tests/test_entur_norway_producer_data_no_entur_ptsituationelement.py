"""
Test case for PtSituationElement
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.ptsituationelement import PtSituationElement
from test_entur_norway_producer_data_no_entur_validityperiod import Test_ValidityPeriod


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
            situation_number='qfwsjngrdryynlfgbcwc',
            version='zdkehfrqiedvjjgyyjgc',
            creation_time='jdbncfpcwjcsbjtpqmpm',
            source_type='gptzcotymcqlsjqnzbtc',
            source_name='xnndhqbgmyhoatquadiu',
            progress='zzzhjbmknhuopcjzrxcw',
            severity='ynfyptrqqkioiliujaqh',
            keywords='eacmxzwjcatgftpluxjs',
            summary='hlvmfupfvpaoijnnxviu',
            description='bqymypkbrsbyeywyccjb',
            validity_periods=[Test_ValidityPeriod.create_instance(), Test_ValidityPeriod.create_instance(), Test_ValidityPeriod.create_instance()],
            affects_line_refs=['ivxzhmmamsrumxxlfhfu', 'rbmottdapjdnjgffogzu', 'semnorybytelftznvrgg'],
            affects_stop_point_refs=['mzjupjuqpfmxsbpveqdt', 'ondktyazqsebnvurefwt', 'xnqeeqzmxnseqycrzxow', 'htqnnpljhqdqvjitmtwf', 'wtitpowdncglozuddsud']
        )
        return instance

    
    def test_situation_number_property(self):
        """
        Test situation_number property
        """
        test_value = 'qfwsjngrdryynlfgbcwc'
        self.instance.situation_number = test_value
        self.assertEqual(self.instance.situation_number, test_value)
    
    def test_version_property(self):
        """
        Test version property
        """
        test_value = 'zdkehfrqiedvjjgyyjgc'
        self.instance.version = test_value
        self.assertEqual(self.instance.version, test_value)
    
    def test_creation_time_property(self):
        """
        Test creation_time property
        """
        test_value = 'jdbncfpcwjcsbjtpqmpm'
        self.instance.creation_time = test_value
        self.assertEqual(self.instance.creation_time, test_value)
    
    def test_source_type_property(self):
        """
        Test source_type property
        """
        test_value = 'gptzcotymcqlsjqnzbtc'
        self.instance.source_type = test_value
        self.assertEqual(self.instance.source_type, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'xnndhqbgmyhoatquadiu'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_progress_property(self):
        """
        Test progress property
        """
        test_value = 'zzzhjbmknhuopcjzrxcw'
        self.instance.progress = test_value
        self.assertEqual(self.instance.progress, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'ynfyptrqqkioiliujaqh'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_keywords_property(self):
        """
        Test keywords property
        """
        test_value = 'eacmxzwjcatgftpluxjs'
        self.instance.keywords = test_value
        self.assertEqual(self.instance.keywords, test_value)
    
    def test_summary_property(self):
        """
        Test summary property
        """
        test_value = 'hlvmfupfvpaoijnnxviu'
        self.instance.summary = test_value
        self.assertEqual(self.instance.summary, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'bqymypkbrsbyeywyccjb'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_validity_periods_property(self):
        """
        Test validity_periods property
        """
        test_value = [Test_ValidityPeriod.create_instance(), Test_ValidityPeriod.create_instance(), Test_ValidityPeriod.create_instance()]
        self.instance.validity_periods = test_value
        self.assertEqual(self.instance.validity_periods, test_value)
    
    def test_affects_line_refs_property(self):
        """
        Test affects_line_refs property
        """
        test_value = ['ivxzhmmamsrumxxlfhfu', 'rbmottdapjdnjgffogzu', 'semnorybytelftznvrgg']
        self.instance.affects_line_refs = test_value
        self.assertEqual(self.instance.affects_line_refs, test_value)
    
    def test_affects_stop_point_refs_property(self):
        """
        Test affects_stop_point_refs property
        """
        test_value = ['mzjupjuqpfmxsbpveqdt', 'ondktyazqsebnvurefwt', 'xnqeeqzmxnseqycrzxow', 'htqnnpljhqdqvjitmtwf', 'wtitpowdncglozuddsud']
        self.instance.affects_stop_point_refs = test_value
        self.assertEqual(self.instance.affects_stop_point_refs, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PtSituationElement.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
