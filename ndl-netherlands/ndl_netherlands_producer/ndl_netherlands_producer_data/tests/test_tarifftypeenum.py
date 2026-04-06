import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ndl_netherlands_producer_data.tarifftypeenum import TariffTypeenum


class Test_TariffTypeenum(unittest.TestCase):
    """
    Test case for TariffTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = TariffTypeenum.AD_HOC_PAYMENT

    @staticmethod
    def create_instance():
        """
        Create instance of TariffTypeenum
        """
        return TariffTypeenum.AD_HOC_PAYMENT

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(TariffTypeenum.AD_HOC_PAYMENT.value, "AD_HOC_PAYMENT")
        self.assertEqual(TariffTypeenum.PROFILE_CHEAP.value, "PROFILE_CHEAP")
        self.assertEqual(TariffTypeenum.PROFILE_FAST.value, "PROFILE_FAST")
        self.assertEqual(TariffTypeenum.PROFILE_GREEN.value, "PROFILE_GREEN")
        self.assertEqual(TariffTypeenum.REGULAR.value, "REGULAR")
        self.assertEqual(TariffTypeenum.None.value, "None")