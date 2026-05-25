import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.biomeenum import BiomeEnum


class Test_BiomeEnum(unittest.TestCase):
    """
    Test case for BiomeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = BiomeEnum.amazon

    @staticmethod
    def create_instance():
        """
        Create instance of BiomeEnum
        """
        return BiomeEnum.amazon

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(BiomeEnum.amazon.value, 'amazon')
        self.assertEqual(BiomeEnum.cerrado.value, 'cerrado')