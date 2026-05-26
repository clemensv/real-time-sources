import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_producer_data.generaltransitfeedstatic.exceptiontype import ExceptionType


class Test_ExceptionType(unittest.TestCase):
    """
    Test case for ExceptionType
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ExceptionType.SERVICE_ADDED

    @staticmethod
    def create_instance():
        """
        Create instance of ExceptionType
        """
        return ExceptionType.SERVICE_ADDED

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ExceptionType.SERVICE_ADDED.value, 'SERVICE_ADDED')
        self.assertEqual(ExceptionType.SERVICE_REMOVED.value, 'SERVICE_REMOVED')