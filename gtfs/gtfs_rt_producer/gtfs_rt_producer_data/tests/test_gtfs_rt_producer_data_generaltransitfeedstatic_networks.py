"""
Test case for Networks
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.networks import Networks


class Test_Networks(unittest.TestCase):
    """
    Test case for Networks
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Networks.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Networks for testing
        """
        instance = Networks(
            networkId='veikseoaoxpovbdxsimj',
            networkName='mmwznvmrswmnevmaijrd',
            networkDesc='aawsvkpkvuyytwximukt',
            networkUrl='lrsafplqzskbjxtcyisi'
        )
        return instance

    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'veikseoaoxpovbdxsimj'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
    def test_networkName_property(self):
        """
        Test networkName property
        """
        test_value = 'mmwznvmrswmnevmaijrd'
        self.instance.networkName = test_value
        self.assertEqual(self.instance.networkName, test_value)
    
    def test_networkDesc_property(self):
        """
        Test networkDesc property
        """
        test_value = 'aawsvkpkvuyytwximukt'
        self.instance.networkDesc = test_value
        self.assertEqual(self.instance.networkDesc, test_value)
    
    def test_networkUrl_property(self):
        """
        Test networkUrl property
        """
        test_value = 'lrsafplqzskbjxtcyisi'
        self.instance.networkUrl = test_value
        self.assertEqual(self.instance.networkUrl, test_value)
    
