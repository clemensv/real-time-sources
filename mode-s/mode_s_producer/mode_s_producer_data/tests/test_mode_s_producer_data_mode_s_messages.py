"""
Test case for Messages
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from mode_s_producer_data.mode_s.messages import Messages
from test_mode_s_producer_data_mode_s_modes_adsb_record import Test_ModeS_ADSB_Record


class Test_Messages(unittest.TestCase):
    """
    Test case for Messages
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Messages.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Messages for testing
        """
        instance = Messages(
            messages=[Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance()]
        )
        return instance

    
    def test_messages_property(self):
        """
        Test messages property
        """
        test_value = [Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance()]
        self.instance.messages = test_value
        self.assertEqual(self.instance.messages, test_value)
    
