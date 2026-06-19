"""
Test case for ReservoirFillingInformation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entsoe_mqtt_producer_data.eu.entsoe.transparency.reservoirfillinginformation import ReservoirFillingInformation


class Test_ReservoirFillingInformation(unittest.TestCase):
    """
    Test case for ReservoirFillingInformation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ReservoirFillingInformation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ReservoirFillingInformation for testing
        """
        instance = ReservoirFillingInformation(
            inDomain='lnssqwbahoorsekabctk',
            quantity=float(86.94351349938393),
            resolution='wpjdvpgsrtepjceuxbak',
            documentType='uvzyeqilyfvzehfkchaw',
            unitName='dzxnvkdnudfwzvawjeas'
        )
        return instance

    
    def test_inDomain_property(self):
        """
        Test inDomain property
        """
        test_value = 'lnssqwbahoorsekabctk'
        self.instance.inDomain = test_value
        self.assertEqual(self.instance.inDomain, test_value)
    
    def test_quantity_property(self):
        """
        Test quantity property
        """
        test_value = float(86.94351349938393)
        self.instance.quantity = test_value
        self.assertEqual(self.instance.quantity, test_value)
    
    def test_resolution_property(self):
        """
        Test resolution property
        """
        test_value = 'wpjdvpgsrtepjceuxbak'
        self.instance.resolution = test_value
        self.assertEqual(self.instance.resolution, test_value)
    
    def test_documentType_property(self):
        """
        Test documentType property
        """
        test_value = 'uvzyeqilyfvzehfkchaw'
        self.instance.documentType = test_value
        self.assertEqual(self.instance.documentType, test_value)
    
    def test_unitName_property(self):
        """
        Test unitName property
        """
        test_value = 'dzxnvkdnudfwzvawjeas'
        self.instance.unitName = test_value
        self.assertEqual(self.instance.unitName, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ReservoirFillingInformation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ReservoirFillingInformation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

