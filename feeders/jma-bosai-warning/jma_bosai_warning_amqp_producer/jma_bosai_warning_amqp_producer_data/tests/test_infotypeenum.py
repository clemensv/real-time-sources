import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_warning_amqp_producer_data.infotypeenum import InfoTypeenum


class Test_InfoTypeenum(unittest.TestCase):
    """
    Test case for InfoTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = InfoTypeenum.ISSUED

    @staticmethod
    def create_instance():
        """
        Create instance of InfoTypeenum
        """
        return InfoTypeenum.ISSUED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(InfoTypeenum.ISSUED.value, 'ISSUED')
        self.assertEqual(InfoTypeenum.CORRECTED.value, 'CORRECTED')
        self.assertEqual(InfoTypeenum.CANCELLED.value, 'CANCELLED')