"""
Test case for BinaryAcknowledge
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_producer_data.binaryacknowledge import BinaryAcknowledge


class Test_BinaryAcknowledge(unittest.TestCase):
    """
    Test case for BinaryAcknowledge
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BinaryAcknowledge.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BinaryAcknowledge for testing
        """
        instance = BinaryAcknowledge(
            MessageID=int(5),
            RepeatIndicator=int(86),
            UserID=int(26),
            Valid=True,
            Spare=int(0),
            Destinations={'gfnvffiutjwbowvdmmgw': 'kwzsvggbamoxynodminr', 'sjjickqfxtrhnbqutkew': 'pppeihfpkgztkixmdlhq', 'whhrglrlqsczaiideoov': 'ypelqmnyikjkpnimzhrx'}
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(5)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(86)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(26)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = True
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(0)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Destinations_property(self):
        """
        Test Destinations property
        """
        test_value = {'gfnvffiutjwbowvdmmgw': 'kwzsvggbamoxynodminr', 'sjjickqfxtrhnbqutkew': 'pppeihfpkgztkixmdlhq', 'whhrglrlqsczaiideoov': 'ypelqmnyikjkpnimzhrx'}
        self.instance.Destinations = test_value
        self.assertEqual(self.instance.Destinations, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BinaryAcknowledge.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BinaryAcknowledge.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

