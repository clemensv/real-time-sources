import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nina_bbk_producer_data.msgtypeenum import MsgTypeenum


class Test_MsgTypeenum(unittest.TestCase):
    """
    Test case for MsgTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = MsgTypeenum.Alert

    @staticmethod
    def create_instance():
        """
        Create instance of MsgTypeenum
        """
        return MsgTypeenum.Alert

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(MsgTypeenum.Alert.value, "Alert")
        self.assertEqual(MsgTypeenum.Update.value, "Update")
        self.assertEqual(MsgTypeenum.Cancel.value, "Cancel")
        self.assertEqual(MsgTypeenum.Ack.value, "Ack")
        self.assertEqual(MsgTypeenum.Error.value, "Error")