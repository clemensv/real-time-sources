"""
Test case for MonitoringSite
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_nwis_wq_amqp_producer_data.monitoringsite import MonitoringSite


class Test_MonitoringSite(unittest.TestCase):
    """
    Test case for MonitoringSite
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MonitoringSite.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MonitoringSite for testing
        """
        instance = MonitoringSite(
            site_number='cvyxbpgqjkwqruzoqlmd',
            site_name='zbkjreyqrujsyvjetctt',
            agency_code='wkbjhfdxfqnrqxoxdrls',
            latitude=float(1.9952963028393111),
            longitude=float(43.913745604631984),
            site_type='hnqhzuvnfpptyveylizd',
            state_code='byunqeadlffitqtlkpyz',
            county_code='eteykljltemkqvowxjkf',
            huc_code='bbmwgwxfnjmpptpthdms',
            state='pyjpcyhmpubtnxacuxmi',
            parameter_code='fesxvkntszivrpdqrcal'
        )
        return instance

    
    def test_site_number_property(self):
        """
        Test site_number property
        """
        test_value = 'cvyxbpgqjkwqruzoqlmd'
        self.instance.site_number = test_value
        self.assertEqual(self.instance.site_number, test_value)
    
    def test_site_name_property(self):
        """
        Test site_name property
        """
        test_value = 'zbkjreyqrujsyvjetctt'
        self.instance.site_name = test_value
        self.assertEqual(self.instance.site_name, test_value)
    
    def test_agency_code_property(self):
        """
        Test agency_code property
        """
        test_value = 'wkbjhfdxfqnrqxoxdrls'
        self.instance.agency_code = test_value
        self.assertEqual(self.instance.agency_code, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(1.9952963028393111)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(43.913745604631984)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = 'hnqhzuvnfpptyveylizd'
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'byunqeadlffitqtlkpyz'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_county_code_property(self):
        """
        Test county_code property
        """
        test_value = 'eteykljltemkqvowxjkf'
        self.instance.county_code = test_value
        self.assertEqual(self.instance.county_code, test_value)
    
    def test_huc_code_property(self):
        """
        Test huc_code property
        """
        test_value = 'bbmwgwxfnjmpptpthdms'
        self.instance.huc_code = test_value
        self.assertEqual(self.instance.huc_code, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'pyjpcyhmpubtnxacuxmi'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_parameter_code_property(self):
        """
        Test parameter_code property
        """
        test_value = 'fesxvkntszivrpdqrcal'
        self.instance.parameter_code = test_value
        self.assertEqual(self.instance.parameter_code, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MonitoringSite.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MonitoringSite.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

