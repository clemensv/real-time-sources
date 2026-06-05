import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.effect import Effect


class Test_Effect(unittest.TestCase):
    """
    Test case for Effect
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = Effect.NO_SERVICE

    @staticmethod
    def create_instance():
        """
        Create instance of Effect
        """
        return Effect.NO_SERVICE

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(Effect.NO_SERVICE.value, 'NO_SERVICE')
        self.assertEqual(Effect.REDUCED_SERVICE.value, 'REDUCED_SERVICE')
        self.assertEqual(Effect.SIGNIFICANT_DELAYS.value, 'SIGNIFICANT_DELAYS')
        self.assertEqual(Effect.DETOUR.value, 'DETOUR')
        self.assertEqual(Effect.ADDITIONAL_SERVICE.value, 'ADDITIONAL_SERVICE')
        self.assertEqual(Effect.MODIFIED_SERVICE.value, 'MODIFIED_SERVICE')
        self.assertEqual(Effect.OTHER_EFFECT.value, 'OTHER_EFFECT')
        self.assertEqual(Effect.UNKNOWN_EFFECT.value, 'UNKNOWN_EFFECT')
        self.assertEqual(Effect.STOP_MOVED.value, 'STOP_MOVED')