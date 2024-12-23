"""
Test case for Areas
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.areas import Areas


class Test_Areas(unittest.TestCase):
    """
    Test case for Areas
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Areas.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Areas for testing
        """
        instance = Areas(
            areaId='zdzhzidahcnfdtslsxbf',
            areaName='rliktqqovpmfcyramnpf',
            areaDesc='kdahbwamqgjlhfkpchpq',
            areaUrl='vjgothvpkbshpovdsmgs'
        )
        return instance

    
    def test_areaId_property(self):
        """
        Test areaId property
        """
        test_value = 'zdzhzidahcnfdtslsxbf'
        self.instance.areaId = test_value
        self.assertEqual(self.instance.areaId, test_value)
    
    def test_areaName_property(self):
        """
        Test areaName property
        """
        test_value = 'rliktqqovpmfcyramnpf'
        self.instance.areaName = test_value
        self.assertEqual(self.instance.areaName, test_value)
    
    def test_areaDesc_property(self):
        """
        Test areaDesc property
        """
        test_value = 'kdahbwamqgjlhfkpchpq'
        self.instance.areaDesc = test_value
        self.assertEqual(self.instance.areaDesc, test_value)
    
    def test_areaUrl_property(self):
        """
        Test areaUrl property
        """
        test_value = 'vjgothvpkbshpovdsmgs'
        self.instance.areaUrl = test_value
        self.assertEqual(self.instance.areaUrl, test_value)
    
