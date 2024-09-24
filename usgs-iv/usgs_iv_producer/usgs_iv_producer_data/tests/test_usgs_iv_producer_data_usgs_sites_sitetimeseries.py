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
            agency_cd='kfviuuzrekespsuzcjbk',
            site_no='rmacdnthnodnnckygxig',
            parameter_cd='anxdpdnmhdnchdrqoguo',
            timeseries_cd='ccsviysypkyqwenxpkoj',
            description='jxdrebgsuxtqcbgctmtu'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'kfviuuzrekespsuzcjbk'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rmacdnthnodnnckygxig'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'anxdpdnmhdnchdrqoguo'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'ccsviysypkyqwenxpkoj'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'jxdrebgsuxtqcbgctmtu'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
