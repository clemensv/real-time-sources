import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_quake_amqp_producer_data.bulletintypeenum import BulletinTypeenum


class Test_BulletinTypeenum(unittest.TestCase):
    """
    Test case for BulletinTypeenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = BulletinTypeenum.VXSE51

    @staticmethod
    def create_instance():
        """
        Create instance of BulletinTypeenum
        """
        return BulletinTypeenum.VXSE51

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BulletinTypeenum.VXSE51.value, 'VXSE51')
        self.assertEqual(BulletinTypeenum.VXSE52.value, 'VXSE52')
        self.assertEqual(BulletinTypeenum.VXSE53.value, 'VXSE53')
        self.assertEqual(BulletinTypeenum.VXSE5k.value, 'VXSE5k')
        self.assertEqual(BulletinTypeenum.VXSE61.value, 'VXSE61')
        self.assertEqual(BulletinTypeenum.VYSE52.value, 'VYSE52')