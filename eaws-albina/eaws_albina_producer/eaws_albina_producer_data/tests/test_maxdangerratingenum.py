import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from eaws_albina_producer_data.maxdangerratingenum import MaxDangerRatingenum


class Test_MaxDangerRatingenum(unittest.TestCase):
    """
    Test case for MaxDangerRatingenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = MaxDangerRatingenum.low

    @staticmethod
    def create_instance():
        """
        Create instance of MaxDangerRatingenum
        """
        return MaxDangerRatingenum.low

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(MaxDangerRatingenum.low.value, "low")
        self.assertEqual(MaxDangerRatingenum.moderate.value, "moderate")
        self.assertEqual(MaxDangerRatingenum.considerable.value, "considerable")
        self.assertEqual(MaxDangerRatingenum.high.value, "high")
        self.assertEqual(MaxDangerRatingenum.very_high.value, "very_high")