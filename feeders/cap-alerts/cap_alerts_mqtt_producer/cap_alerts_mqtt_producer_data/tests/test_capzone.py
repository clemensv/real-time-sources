"""
Test case for CapZone
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_mqtt_producer_data.org.oasis.cap.alerts.capzone import CapZone


class Test_CapZone(unittest.TestCase):
    """
    Test case for CapZone
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CapZone.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CapZone for testing
        """
        instance = CapZone(
            cap_source_id='aowhurbmayjkhsuxxqhv',
            zone_id='kwvfiyngppggoptwenei',
            name='awecsecayevrkuwjqgxf',
            zone_type='eacoxkzuwqjtalyykysc',
            state='vewkfeupnjvlelrkxuzh',
            forecast_office='wueufxtlivhsaqaqlrrr',
            time_zones=['hhxsoqnmnafdipdumcmd'],
            geometry='tntplgcpsfaazxzctwsy',
            provider_url='acuigfwtekevjqmnznra'
        )
        return instance

    
    def test_cap_source_id_property(self):
        """
        Test cap_source_id property
        """
        test_value = 'aowhurbmayjkhsuxxqhv'
        self.instance.cap_source_id = test_value
        self.assertEqual(self.instance.cap_source_id, test_value)
    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'kwvfiyngppggoptwenei'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'awecsecayevrkuwjqgxf'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_zone_type_property(self):
        """
        Test zone_type property
        """
        test_value = 'eacoxkzuwqjtalyykysc'
        self.instance.zone_type = test_value
        self.assertEqual(self.instance.zone_type, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'vewkfeupnjvlelrkxuzh'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_forecast_office_property(self):
        """
        Test forecast_office property
        """
        test_value = 'wueufxtlivhsaqaqlrrr'
        self.instance.forecast_office = test_value
        self.assertEqual(self.instance.forecast_office, test_value)
    
    def test_time_zones_property(self):
        """
        Test time_zones property
        """
        test_value = ['hhxsoqnmnafdipdumcmd']
        self.instance.time_zones = test_value
        self.assertEqual(self.instance.time_zones, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = 'tntplgcpsfaazxzctwsy'
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_provider_url_property(self):
        """
        Test provider_url property
        """
        test_value = 'acuigfwtekevjqmnznra'
        self.instance.provider_url = test_value
        self.assertEqual(self.instance.provider_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CapZone.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CapZone.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

