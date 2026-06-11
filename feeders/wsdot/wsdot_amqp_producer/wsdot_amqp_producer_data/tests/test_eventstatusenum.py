import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.alerts.eventstatusenum import EventStatusenum


class Test_EventStatusenum(unittest.TestCase):
    """
    Test case for EventStatusenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = EventStatusenum.Open

    @staticmethod
    def create_instance():
        """
        Create instance of EventStatusenum
        """
        return EventStatusenum.Open

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(EventStatusenum.Open.value, 'Open')
        self.assertEqual(EventStatusenum.Closed.value, 'Closed')