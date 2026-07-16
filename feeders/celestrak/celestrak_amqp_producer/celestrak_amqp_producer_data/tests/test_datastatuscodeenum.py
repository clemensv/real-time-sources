import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_amqp_producer_data.org.celestrak.datastatuscodeenum import DataStatusCodeEnum


class Test_DataStatusCodeEnum(unittest.TestCase):
    """
    Test case for DataStatusCodeEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = DataStatusCodeEnum.NCE

    @staticmethod
    def create_instance():
        """
        Create instance of DataStatusCodeEnum
        """
        return DataStatusCodeEnum.NCE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(DataStatusCodeEnum.NCE.value, 'NCE')
        self.assertEqual(DataStatusCodeEnum.NIE.value, 'NIE')
        self.assertEqual(DataStatusCodeEnum.NEA.value, 'NEA')