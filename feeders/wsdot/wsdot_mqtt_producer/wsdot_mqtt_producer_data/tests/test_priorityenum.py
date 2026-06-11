import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.alerts.priorityenum import PriorityEnum


class Test_PriorityEnum(unittest.TestCase):
    """
    Test case for PriorityEnum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = PriorityEnum.Highest

    @staticmethod
    def create_instance():
        """
        Create instance of PriorityEnum
        """
        return PriorityEnum.Highest

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(PriorityEnum.Highest.value, 'Highest')
        self.assertEqual(PriorityEnum.High.value, 'High')
        self.assertEqual(PriorityEnum.Medium.value, 'Medium')
        self.assertEqual(PriorityEnum.Low.value, 'Low')
        self.assertEqual(PriorityEnum.Lowest.value, 'Lowest')