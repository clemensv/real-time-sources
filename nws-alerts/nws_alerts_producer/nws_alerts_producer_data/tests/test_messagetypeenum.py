import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nws_alerts_producer_data.messagetypeenum import MessageTypeenum


class Test_MessageTypeenum(unittest.TestCase):
    """
    Test case for MessageTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = MessageTypeenum.Alert

    @staticmethod
    def create_instance():
        """
        Create instance of MessageTypeenum
        """
        return MessageTypeenum.Alert

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(MessageTypeenum.Alert.value, "Alert")
        self.assertEqual(MessageTypeenum.Update.value, "Update")
        self.assertEqual(MessageTypeenum.Cancel.value, "Cancel")
        self.assertEqual(MessageTypeenum.Ack.value, "Ack")
        self.assertEqual(MessageTypeenum.Error.value, "Error")