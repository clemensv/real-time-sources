"""
Test case for Water
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from pegelonline_producer_data.de.wsv.pegelonline.water import Water


class Test_Water(unittest.TestCase):
    """
    Test case for Water
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Water.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Water for testing
        """
        instance = Water(
            shortname='ztdyqulfatlrjmldqdom',
            longname='hrmhgcgjscsnqlfrqdoq'
        )
        return instance

    
    def test_shortname_property(self):
        """
        Test shortname property
        """
        test_value = 'ztdyqulfatlrjmldqdom'
        self.instance.shortname = test_value
        self.assertEqual(self.instance.shortname, test_value)
    
    def test_longname_property(self):
        """
        Test longname property
        """
        test_value = 'hrmhgcgjscsnqlfrqdoq'
        self.instance.longname = test_value
        self.assertEqual(self.instance.longname, test_value)
    
