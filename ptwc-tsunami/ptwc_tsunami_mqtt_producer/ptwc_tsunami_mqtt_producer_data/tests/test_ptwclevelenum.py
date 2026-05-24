import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ptwc_tsunami_mqtt_producer_data.ptwclevelenum import PtwcLevelenum


class Test_PtwcLevelenum(unittest.TestCase):
    """
    Test case for PtwcLevelenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = PtwcLevelenum.warning

    @staticmethod
    def create_instance():
        """
        Create instance of PtwcLevelenum
        """
        return PtwcLevelenum.warning

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(PtwcLevelenum.warning.value, 'warning')
        self.assertEqual(PtwcLevelenum.advisory.value, 'advisory')
        self.assertEqual(PtwcLevelenum.watch.value, 'watch')
        self.assertEqual(PtwcLevelenum.information.value, 'information')
        self.assertEqual(PtwcLevelenum.unknown.value, 'unknown')