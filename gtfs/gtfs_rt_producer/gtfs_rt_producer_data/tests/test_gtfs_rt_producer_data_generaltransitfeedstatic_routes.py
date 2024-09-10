"""
Test case for Routes
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.routes import Routes
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuousdropoff import Test_ContinuousDropOff
from test_gtfs_rt_producer_data_generaltransitfeedstatic_continuouspickup import Test_ContinuousPickup
from test_gtfs_rt_producer_data_generaltransitfeedstatic_routetype import Test_RouteType

class Test_Routes(unittest.TestCase):
    """
    Test case for Routes
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Routes.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Routes for testing
        """
        instance = Routes(
            routeId='nmexuyweqcyhxkiocrgb',
            agencyId='ggubruoifpmfwnktssaf',
            routeShortName='ekpfqklremsejpufwbej',
            routeLongName='wpqlupnrwsqsgsnxwnxd',
            routeDesc='pazbgjnfuskjcklkbeck',
            routeType=Test_RouteType.create_instance(),
            routeUrl='xzgvbvkumdarklznlqas',
            routeColor='uvawnnfglutxhchuulvl',
            routeTextColor='lbuokhpuahwzxhtrggzg',
            routeSortOrder=int(35),
            continuousPickup=Test_ContinuousPickup.create_instance(),
            continuousDropOff=Test_ContinuousDropOff.create_instance(),
            networkId='oyhofcemjtyiavxwrvbf'
        )
        return instance

    
    def test_routeId_property(self):
        """
        Test routeId property
        """
        test_value = 'nmexuyweqcyhxkiocrgb'
        self.instance.routeId = test_value
        self.assertEqual(self.instance.routeId, test_value)
    
    def test_agencyId_property(self):
        """
        Test agencyId property
        """
        test_value = 'ggubruoifpmfwnktssaf'
        self.instance.agencyId = test_value
        self.assertEqual(self.instance.agencyId, test_value)
    
    def test_routeShortName_property(self):
        """
        Test routeShortName property
        """
        test_value = 'ekpfqklremsejpufwbej'
        self.instance.routeShortName = test_value
        self.assertEqual(self.instance.routeShortName, test_value)
    
    def test_routeLongName_property(self):
        """
        Test routeLongName property
        """
        test_value = 'wpqlupnrwsqsgsnxwnxd'
        self.instance.routeLongName = test_value
        self.assertEqual(self.instance.routeLongName, test_value)
    
    def test_routeDesc_property(self):
        """
        Test routeDesc property
        """
        test_value = 'pazbgjnfuskjcklkbeck'
        self.instance.routeDesc = test_value
        self.assertEqual(self.instance.routeDesc, test_value)
    
    def test_routeType_property(self):
        """
        Test routeType property
        """
        test_value = Test_RouteType.create_instance()
        self.instance.routeType = test_value
        self.assertEqual(self.instance.routeType, test_value)
    
    def test_routeUrl_property(self):
        """
        Test routeUrl property
        """
        test_value = 'xzgvbvkumdarklznlqas'
        self.instance.routeUrl = test_value
        self.assertEqual(self.instance.routeUrl, test_value)
    
    def test_routeColor_property(self):
        """
        Test routeColor property
        """
        test_value = 'uvawnnfglutxhchuulvl'
        self.instance.routeColor = test_value
        self.assertEqual(self.instance.routeColor, test_value)
    
    def test_routeTextColor_property(self):
        """
        Test routeTextColor property
        """
        test_value = 'lbuokhpuahwzxhtrggzg'
        self.instance.routeTextColor = test_value
        self.assertEqual(self.instance.routeTextColor, test_value)
    
    def test_routeSortOrder_property(self):
        """
        Test routeSortOrder property
        """
        test_value = int(35)
        self.instance.routeSortOrder = test_value
        self.assertEqual(self.instance.routeSortOrder, test_value)
    
    def test_continuousPickup_property(self):
        """
        Test continuousPickup property
        """
        test_value = Test_ContinuousPickup.create_instance()
        self.instance.continuousPickup = test_value
        self.assertEqual(self.instance.continuousPickup, test_value)
    
    def test_continuousDropOff_property(self):
        """
        Test continuousDropOff property
        """
        test_value = Test_ContinuousDropOff.create_instance()
        self.instance.continuousDropOff = test_value
        self.assertEqual(self.instance.continuousDropOff, test_value)
    
    def test_networkId_property(self):
        """
        Test networkId property
        """
        test_value = 'oyhofcemjtyiavxwrvbf'
        self.instance.networkId = test_value
        self.assertEqual(self.instance.networkId, test_value)
    
