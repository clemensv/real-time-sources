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
            site_no='wlomklgzausjnizwizfk',
            datetime='ufrkxiolfafthffeimlt',
            status='mfdpekxgalnbrgdgmuio',
            parameter_cd='micsyqdwafmuyiqitghf',
            timeseries_cd='nzmuyexnsvvkukjbimpy'
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'wlomklgzausjnizwizfk'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'ufrkxiolfafthffeimlt'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'mfdpekxgalnbrgdgmuio'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_parameter_cd_property(self):
        """
        Test parameter_cd property
        """
        test_value = 'micsyqdwafmuyiqitghf'
        self.instance.parameter_cd = test_value
        self.assertEqual(self.instance.parameter_cd, test_value)
    
    def test_timeseries_cd_property(self):
        """
        Test timeseries_cd property
        """
        test_value = 'nzmuyexnsvvkukjbimpy'
        self.instance.timeseries_cd = test_value
        self.assertEqual(self.instance.timeseries_cd, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EquipmentStatus.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EquipmentStatus.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

