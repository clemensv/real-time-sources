"""
Test case for WindSolarForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_producer_data.eu.entsoe.transparency.windsolarforecast import WindSolarForecast


class Test_WindSolarForecast(unittest.TestCase):
    """
    Test case for WindSolarForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WindSolarForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WindSolarForecast for testing
        """
        instance = WindSolarForecast(
            inDomain='hjcnxetydslwexwbqduy',
            psrType='dxryhumxsjomclivpjyk',
            quantity=float(44.580736690815655),
            resolution='cqdxwzvubebisbcsadne',
            businessType='stkjpyrevooouvxszssx',
            documentType='vgayvoyvcxzetltvyppr',
            unitName='zxzkoflnsyrpfgzzzjxd'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'hjcnxetydslwexwbqduy'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_psrType_property(self):
        """
        Test psrType property
        """
        test_value = 'dxryhumxsjomclivpjyk'
        self.instance.psrType = test_value
        self.assertEqual(self.instance.psrType, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(44.580736690815655)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'cqdxwzvubebisbcsadne'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_businessType_property(self):
        """
        Test businessType property
        """
        test_value = 'stkjpyrevooouvxszssx'
        self.instance.businessType = test_value
        self.assertEqual(self.instance.businessType, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'vgayvoyvcxzetltvyppr'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'zxzkoflnsyrpfgzzzjxd'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WindSolarForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
