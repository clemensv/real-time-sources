import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gdacs_producer_data.eventtypeenum import EventTypeenum


class Test_EventTypeenum(unittest.TestCase):
    """
    Test case for EventTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EventTypeenum.EQ

    @staticmethod
    def create_instance():
        """
        Create instance of EventTypeenum
        """
        return EventTypeenum.EQ

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EventTypeenum.EQ.value, "EQ")
        self.assertEqual(EventTypeenum.TC.value, "TC")
        self.assertEqual(EventTypeenum.FL.value, "FL")
        self.assertEqual(EventTypeenum.VO.value, "VO")
        self.assertEqual(EventTypeenum.FF.value, "FF")
        self.assertEqual(EventTypeenum.DR.value, "DR")