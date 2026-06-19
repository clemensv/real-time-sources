import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from kystverket_ais_amqp_producer_data.msgtypeenum import MsgTypeenum


class Test_MsgTypeenum(unittest.TestCase):
    """
    Test case for MsgTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = MsgTypeenum.position_MINUSreport

    @staticmethod
    def create_instance():
        """
        Create instance of MsgTypeenum
        """
        return MsgTypeenum.position_MINUSreport

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(MsgTypeenum.position_MINUSreport.value, 'position-report')
        self.assertEqual(MsgTypeenum.static.value, 'static')
        self.assertEqual(MsgTypeenum.aid_MINUSto_MINUSnavigation.value, 'aid-to-navigation')