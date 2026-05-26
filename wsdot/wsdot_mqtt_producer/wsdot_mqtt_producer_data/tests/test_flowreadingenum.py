import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.traffic.flowreadingenum import FlowReadingenum


class Test_FlowReadingenum(unittest.TestCase):
    """
    Test case for FlowReadingenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = FlowReadingenum.Unknown

    @staticmethod
    def create_instance():
        """
        Create instance of FlowReadingenum
        """
        return FlowReadingenum.Unknown

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(FlowReadingenum.Unknown.value, 'Unknown')
        self.assertEqual(FlowReadingenum.WideOpen.value, 'WideOpen')
        self.assertEqual(FlowReadingenum.Moderate.value, 'Moderate')
        self.assertEqual(FlowReadingenum.Heavy.value, 'Heavy')
        self.assertEqual(FlowReadingenum.StopAndGo.value, 'StopAndGo')
        self.assertEqual(FlowReadingenum.NoData.value, 'NoData')