import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_mqtt_producer_data.org.oasis.cap.alerts.responsetypelistenum import ResponseTypelistenum


class Test_ResponseTypelistenum(unittest.TestCase):
    """
    Test case for ResponseTypelistenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ResponseTypelistenum.Shelter

    @staticmethod
    def create_instance():
        """
        Create instance of ResponseTypelistenum
        """
        return ResponseTypelistenum.Shelter

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ResponseTypelistenum.Shelter.value, 'Shelter')
        self.assertEqual(ResponseTypelistenum.Evacuate.value, 'Evacuate')
        self.assertEqual(ResponseTypelistenum.Prepare.value, 'Prepare')
        self.assertEqual(ResponseTypelistenum.Execute.value, 'Execute')
        self.assertEqual(ResponseTypelistenum.Avoid.value, 'Avoid')
        self.assertEqual(ResponseTypelistenum.Monitor.value, 'Monitor')
        self.assertEqual(ResponseTypelistenum.Assess.value, 'Assess')
        self.assertEqual(ResponseTypelistenum.AllClear.value, 'AllClear')
        self.assertEqual(ResponseTypelistenum.None_.value, 'None')