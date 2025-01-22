"""
Test case for ModeSMessages
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from mode_s_producer_data.mode_s.modesmessages import ModeSMessages
from test_mode_s_producer_data_mode_s_modes_adsb_record import Test_ModeS_ADSB_Record


class Test_ModeSMessages(unittest.TestCase):
    """
    Test case for ModeSMessages
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ModeSMessages.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ModeSMessages for testing
        """
        instance = ModeSMessages(
            messages=[Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance()]
        )
        return instance

    
    def test_messages_property(self):
        """
        Test messages property
        """
        test_value = [Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance(), Test_ModeS_ADSB_Record.create_instance()]
        self.instance.messages = test_value
        self.assertEqual(self.instance.messages, test_value)
    
