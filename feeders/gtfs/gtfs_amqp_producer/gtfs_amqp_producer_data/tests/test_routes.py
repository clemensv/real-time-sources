"""
Test case for Routes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_amqp_producer_data.generaltransitfeedstatic.routes import Routes
from typing import Any


class Test_Routes(unittest.TestCase):
    """
    Test case for Routes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Routes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Routes for testing
        """
        instance = Routes(
            routeId='wzdmnthwuzpkowsptfjs',
            agencyId='avaadxgrgockdujmcefl',
            routeShortName='hbxlbwwsivjwthpllerv',
            routeLongName='wljahpazubbimubwkiqh',
            routeDesc='urxcgaruehputtbpehur',
            routeType=None,
            routeUrl='rfdpoodjrfgvjpworweg',
            routeColor='lakbezgvpwrzkdthedzz',
            routeTextColor='aqjuibuiuuhpjjoyoegz',
            routeSortOrder=int(73),
            continuousPickup=None,
            continuousDropOff=None,
            networkId='qwhbywqovjwgtnawmwol'
        )
        return instance

    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'wzdmnthwuzpkowsptfjs'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'avaadxgrgockdujmcefl'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_routeShortName_property(self):
        """
        Test routeShortName property
        """
        test_value = 'hbxlbwwsivjwthpllerv'
        self.instance.routeShortName = test_value
        self.assertEqual(self.instance.routeShortName, test_value)
    
    def test_routeLongName_property(self):
        """
        Test routeLongName property
        """
        test_value = 'wljahpazubbimubwkiqh'
        self.instance.routeLongName = test_value
        self.assertEqual(self.instance.routeLongName, test_value)
    
    def test_routeDesc_property(self):
        """
        Test routeDesc property
        """
        test_value = 'urxcgaruehputtbpehur'
        self.instance.routeDesc = test_value
        self.assertEqual(self.instance.routeDesc, test_value)
    
    def test_routeType_property(self):
        """
        Test routeType property
        """
        test_value = None
        self.instance.routeType = test_value
        self.assertEqual(self.instance.routeType, test_value)
    
    def test_routeUrl_property(self):
        """
        Test routeUrl property
        """
        test_value = 'rfdpoodjrfgvjpworweg'
        self.instance.routeUrl = test_value
        self.assertEqual(self.instance.routeUrl, test_value)
    
    def test_routeColor_property(self):
        """
        Test routeColor property
        """
        test_value = 'lakbezgvpwrzkdthedzz'
        self.instance.routeColor = test_value
        self.assertEqual(self.instance.routeColor, test_value)
    
    def test_routeTextColor_property(self):
        """
        Test routeTextColor property
        """
        test_value = 'aqjuibuiuuhpjjoyoegz'
        self.instance.routeTextColor = test_value
        self.assertEqual(self.instance.routeTextColor, test_value)
    
    def test_routeSortOrder_property(self):
        """
        Test routeSortOrder property
        """
        test_value = int(73)
        self.instance.routeSortOrder = test_value
        self.assertEqual(self.instance.routeSortOrder, test_value)
    
    def test_continuousPickup_property(self):
        """
        Test continuousPickup property
        """
        test_value = None
        self.instance.continuousPickup = test_value
        self.assertEqual(self.instance.continuousPickup, test_value)
    
    def test_continuousDropOff_property(self):
        """
        Test continuousDropOff property
        """
        test_value = None
        self.instance.continuousDropOff = test_value
        self.assertEqual(self.instance.continuousDropOff, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'qwhbywqovjwgtnawmwol'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Routes.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Routes.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

