"""
Test case for DataLinkManagementMessage
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_mqtt_producer_data.datalinkmanagementmessage import DataLinkManagementMessage


class Test_DataLinkManagementMessage(unittest.TestCase):
    """
    Test case for DataLinkManagementMessage
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DataLinkManagementMessage.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DataLinkManagementMessage for testing
        """
        instance = DataLinkManagementMessage(
            MessageID=int(99),
            RepeatIndicator=int(86),
            UserID=int(21),
            Valid=False,
            Spare=int(65),
            Data={'ukdbztbnpmmphonnlnwk': 'zoddmuyntivlqqwsrshk', 'qttoiuoqwipsmvxjwogv': 'usamxlmojdmayyhrquav', 'ehckfvjgkfhrhmykkeri': 'xrcrdhyyvctgotbuywpi', 'jbhgqmdlhhezowgelcam': 'kxhfckqrcfamxcypcgep', 'fctjecyudeynjsgyplmi': 'jpnwmagyihxsvmkyttmb'}
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(99)
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
        test_value = int(21)
        self.instance.UserID = test_value
        self.assertEqual(self.instance.UserID, test_value)
    
    def test_Valid_property(self):
        """
        Test Valid property
        """
        test_value = False
        self.instance.Valid = test_value
        self.assertEqual(self.instance.Valid, test_value)
    
    def test_Spare_property(self):
        """
        Test Spare property
        """
        test_value = int(65)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Data_property(self):
        """
        Test Data property
        """
        test_value = {'ukdbztbnpmmphonnlnwk': 'zoddmuyntivlqqwsrshk', 'qttoiuoqwipsmvxjwogv': 'usamxlmojdmayyhrquav', 'ehckfvjgkfhrhmykkeri': 'xrcrdhyyvctgotbuywpi', 'jbhgqmdlhhezowgelcam': 'kxhfckqrcfamxcypcgep', 'fctjecyudeynjsgyplmi': 'jpnwmagyihxsvmkyttmb'}
        self.instance.Data = test_value
        self.assertEqual(self.instance.Data, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DataLinkManagementMessage.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DataLinkManagementMessage.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

