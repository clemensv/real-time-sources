"""
Test case for SiteTimeseries
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.sites.sitetimeseries import SiteTimeseries


class Test_SiteTimeseries(unittest.TestCase):
    """
    Test case for SiteTimeseries
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SiteTimeseries.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SiteTimeseries for testing
        """
        instance = SiteTimeseries(
            agency_cd='eixdlektgkqxchztigff',
            site_no='jzeelnpcpcbiilquvilb',
            parameter_cd='uasoflkhkjqemiwtulfb',
            timeseries_cd='ywiwrnuwtdymuslslbxe',
            description='qsgydxrcuhngokvluvvb'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'eixdlektgkqxchztigff'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'jzeelnpcpcbiilquvilb'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'uasoflkhkjqemiwtulfb'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ywiwrnuwtdymuslslbxe'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'qsgydxrcuhngokvluvvb'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SiteTimeseries.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SiteTimeseries.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

