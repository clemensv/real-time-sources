import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gdacs_producer_data.alertcolorenum import AlertColorenum


class Test_AlertColorenum(unittest.TestCase):
    """
    Test case for AlertColorenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = AlertColorenum.green

    @staticmethod
    def create_instance():
        """
        Create instance of AlertColorenum
        """
        return AlertColorenum.green

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(AlertColorenum.green.value, 'green')
        self.assertEqual(AlertColorenum.orange.value, 'orange')
        self.assertEqual(AlertColorenum.red.value, 'red')