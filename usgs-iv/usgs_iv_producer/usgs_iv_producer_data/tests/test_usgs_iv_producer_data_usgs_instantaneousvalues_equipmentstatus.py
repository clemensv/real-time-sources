"""
Test case for EquipmentStatus
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.equipmentstatus import EquipmentStatus


class Test_EquipmentStatus(unittest.TestCase):
    """
    Test case for EquipmentStatus
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EquipmentStatus.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EquipmentStatus for testing
        """
        instance = EquipmentStatus(
            site_no='xovbwbguxtncfhvnouhb',
            datetime='anxeqxugmshuhemgkkdt',
            status='sjmtyrddtitrhqezhgjh',
            parameter_cd='bicrzrsopcnxexeyxokg',
            timeseries_cd='npxxusuybammqwvhhbat'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'xovbwbguxtncfhvnouhb'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'anxeqxugmshuhemgkkdt'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'sjmtyrddtitrhqezhgjh'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'bicrzrsopcnxexeyxokg'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'npxxusuybammqwvhhbat'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
