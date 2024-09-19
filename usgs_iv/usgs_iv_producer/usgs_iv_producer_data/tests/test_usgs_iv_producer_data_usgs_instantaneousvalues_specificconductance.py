"""
Test case for SpecificConductance
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance


class Test_SpecificConductance(unittest.TestCase):
    """
    Test case for SpecificConductance
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SpecificConductance.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SpecificConductance for testing
        """
        instance = SpecificConductance(
            site_no='doouzignguppbtouffou',
            datetime='xadfnspaaxxbwwbzowjo',
            value=float(59.691412564255245),
            qualifiers=['kqmcmxyfpdcmoszdigrm', 'kmzpmlvukinakheyuhvc', 'hdvhcshrunsdpmvtyxbo', 'rxrcketlfagjgmrphjiz', 'usrpwmnwfetqmujeqaha']
        )
        return instance

    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'doouzignguppbtouffou'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_datetime_property(self):
        """
        Test datetime property
        """
        test_value = 'xadfnspaaxxbwwbzowjo'
        self.instance.datetime = test_value
        self.assertEqual(self.instance.datetime, test_value)
    
    def test_value_property(self):
        """
        Test value property
        """
        test_value = float(59.691412564255245)
        self.instance.value = test_value
        self.assertEqual(self.instance.value, test_value)
    
    def test_qualifiers_property(self):
        """
        Test qualifiers property
        """
        test_value = ['kqmcmxyfpdcmoszdigrm', 'kmzpmlvukinakheyuhvc', 'hdvhcshrunsdpmvtyxbo', 'rxrcketlfagjgmrphjiz', 'usrpwmnwfetqmujeqaha']
        self.instance.qualifiers = test_value
        self.assertEqual(self.instance.qualifiers, test_value)
    
