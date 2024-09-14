"""
Test case for Stops
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from gtfs_rt_producer_data.generaltransitfeedstatic.stops import Stops
from test_gtfs_rt_producer_data_generaltransitfeedstatic_locationtype import Test_LocationType
from test_gtfs_rt_producer_data_generaltransitfeedstatic_wheelchairboarding import Test_WheelchairBoarding

class Test_Stops(unittest.TestCase):
    """
    Test case for Stops
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Stops.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Stops for testing
        """
        instance = Stops(
            stopId='urvhgscohlswhejemusi',
            stopCode='hownwovtnpbxouyogrnt',
            stopName='zresdmaczdwlfzvgqesh',
            ttsStopName='tqedegotzmsvyzhsagdb',
            stopDesc='qvaredmuefvbfiiyzslf',
            stopLat=float(25.391731895978133),
            stopLon=float(52.26672896963057),
            zoneId='lgjqabhgpxhqwvrcqplb',
            stopUrl='cizzmosnhzzttzfczsbz',
            locationType=Test_LocationType.create_instance(),
            parentStation='optzetqtutcwfsxiumgb',
            stopTimezone='emagyztnnehaphggqqlh',
            wheelchairBoarding=Test_WheelchairBoarding.create_instance(),
            levelId='wwhsijmcdrbkzzjnncpw',
            platformCode='oiimfksfftuxwddslqny'
        )
        return instance

    
    def test_stopId_property(self):
        """
        Test stopId property
        """
        test_value = 'urvhgscohlswhejemusi'
        self.instance.stopId = test_value
        self.assertEqual(self.instance.stopId, test_value)
    
    def test_stopCode_property(self):
        """
        Test stopCode property
        """
        test_value = 'hownwovtnpbxouyogrnt'
        self.instance.stopCode = test_value
        self.assertEqual(self.instance.stopCode, test_value)
    
    def test_stopName_property(self):
        """
        Test stopName property
        """
        test_value = 'zresdmaczdwlfzvgqesh'
        self.instance.stopName = test_value
        self.assertEqual(self.instance.stopName, test_value)
    
    def test_ttsStopName_property(self):
        """
        Test ttsStopName property
        """
        test_value = 'tqedegotzmsvyzhsagdb'
        self.instance.ttsStopName = test_value
        self.assertEqual(self.instance.ttsStopName, test_value)
    
    def test_stopDesc_property(self):
        """
        Test stopDesc property
        """
        test_value = 'qvaredmuefvbfiiyzslf'
        self.instance.stopDesc = test_value
        self.assertEqual(self.instance.stopDesc, test_value)
    
    def test_stopLat_property(self):
        """
        Test stopLat property
        """
        test_value = float(25.391731895978133)
        self.instance.stopLat = test_value
        self.assertEqual(self.instance.stopLat, test_value)
    
    def test_stopLon_property(self):
        """
        Test stopLon property
        """
        test_value = float(52.26672896963057)
        self.instance.stopLon = test_value
        self.assertEqual(self.instance.stopLon, test_value)
    
    def test_zoneId_property(self):
        """
        Test zoneId property
        """
        test_value = 'lgjqabhgpxhqwvrcqplb'
        self.instance.zoneId = test_value
        self.assertEqual(self.instance.zoneId, test_value)
    
    def test_stopUrl_property(self):
        """
        Test stopUrl property
        """
        test_value = 'cizzmosnhzzttzfczsbz'
        self.instance.stopUrl = test_value
        self.assertEqual(self.instance.stopUrl, test_value)
    
    def test_locationType_property(self):
        """
        Test locationType property
        """
        test_value = Test_LocationType.create_instance()
        self.instance.locationType = test_value
        self.assertEqual(self.instance.locationType, test_value)
    
    def test_parentStation_property(self):
        """
        Test parentStation property
        """
        test_value = 'optzetqtutcwfsxiumgb'
        self.instance.parentStation = test_value
        self.assertEqual(self.instance.parentStation, test_value)
    
    def test_stopTimezone_property(self):
        """
        Test stopTimezone property
        """
        test_value = 'emagyztnnehaphggqqlh'
        self.instance.stopTimezone = test_value
        self.assertEqual(self.instance.stopTimezone, test_value)
    
    def test_wheelchairBoarding_property(self):
        """
        Test wheelchairBoarding property
        """
        test_value = Test_WheelchairBoarding.create_instance()
        self.instance.wheelchairBoarding = test_value
        self.assertEqual(self.instance.wheelchairBoarding, test_value)
    
    def test_levelId_property(self):
        """
        Test levelId property
        """
        test_value = 'wwhsijmcdrbkzzjnncpw'
        self.instance.levelId = test_value
        self.assertEqual(self.instance.levelId, test_value)
    
    def test_platformCode_property(self):
        """
        Test platformCode property
        """
        test_value = 'oiimfksfftuxwddslqny'
        self.instance.platformCode = test_value
        self.assertEqual(self.instance.platformCode, test_value)
    
