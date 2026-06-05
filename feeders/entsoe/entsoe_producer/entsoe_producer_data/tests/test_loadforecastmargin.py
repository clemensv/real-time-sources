"""
Test case for LoadForecastMargin
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin


class Test_LoadForecastMargin(unittest.TestCase):
    """
    Test case for LoadForecastMargin
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LoadForecastMargin.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LoadForecastMargin for testing
        """
        instance = LoadForecastMargin(
            inDomain='ejyktcpqbmcfbpyfvlbs',
            quantity=float(0.3980349750637546),
            resolution='wyytzfrcdoylkhgyxzkf',
            documentType='yyraohlflkeaijntijxg',
            unitName='oenhfvctbmgozsrfxfuq'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'ejyktcpqbmcfbpyfvlbs'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(0.3980349750637546)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'wyytzfrcdoylkhgyxzkf'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'yyraohlflkeaijntijxg'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'oenhfvctbmgozsrfxfuq'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LoadForecastMargin.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LoadForecastMargin.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

