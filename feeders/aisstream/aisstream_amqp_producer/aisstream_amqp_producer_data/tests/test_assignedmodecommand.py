"""
Test case for AssignedModeCommand
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aisstream_amqp_producer_data.assignedmodecommand import AssignedModeCommand


class Test_AssignedModeCommand(unittest.TestCase):
    """
    Test case for AssignedModeCommand
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_AssignedModeCommand.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of AssignedModeCommand for testing
        """
        instance = AssignedModeCommand(
            MessageID=int(22),
            RepeatIndicator=int(65),
            UserID=int(81),
            Valid=False,
            Spare=int(4),
            Commands={'ggvsxmtgvrmqdmyeeqrj': 'iksvwatluejrfutyvjqv', 'hejaeeemwuoavjguvlqy': 'smnwodaplbmggmeezddo', 'iapttfqwtgdmqrfrkrss': 'lfhojbvlrynyxdtyxbuv', 'tdsoaqiixnepqewtslhb': 'hyvttgqvjtljfyihzkrk', 'jnczoyjphazwaffxxqjq': 'suaooorlmbaursdxsrjf'}
        )
        return instance

    
    def test_MessageID_property(self):
        """
        Test MessageID property
        """
        test_value = int(22)
        self.instance.MessageID = test_value
        self.assertEqual(self.instance.MessageID, test_value)
    
    def test_RepeatIndicator_property(self):
        """
        Test RepeatIndicator property
        """
        test_value = int(65)
        self.instance.RepeatIndicator = test_value
        self.assertEqual(self.instance.RepeatIndicator, test_value)
    
    def test_UserID_property(self):
        """
        Test UserID property
        """
        test_value = int(81)
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
        test_value = int(4)
        self.instance.Spare = test_value
        self.assertEqual(self.instance.Spare, test_value)
    
    def test_Commands_property(self):
        """
        Test Commands property
        """
        test_value = {'ggvsxmtgvrmqdmyeeqrj': 'iksvwatluejrfutyvjqv', 'hejaeeemwuoavjguvlqy': 'smnwodaplbmggmeezddo', 'iapttfqwtgdmqrfrkrss': 'lfhojbvlrynyxdtyxbuv', 'tdsoaqiixnepqewtslhb': 'hyvttgqvjtljfyihzkrk', 'jnczoyjphazwaffxxqjq': 'suaooorlmbaursdxsrjf'}
        self.instance.Commands = test_value
        self.assertEqual(self.instance.Commands, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = AssignedModeCommand.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = AssignedModeCommand.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

