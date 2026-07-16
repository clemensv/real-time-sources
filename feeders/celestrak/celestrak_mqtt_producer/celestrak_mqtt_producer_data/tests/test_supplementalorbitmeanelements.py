"""
Test case for SupplementalOrbitMeanElements
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_mqtt_producer_data.org.celestrak.supplementalorbitmeanelements import SupplementalOrbitMeanElements
from typing import Any
import datetime


class Test_SupplementalOrbitMeanElements(unittest.TestCase):
    """
    Test case for SupplementalOrbitMeanElements
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SupplementalOrbitMeanElements.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SupplementalOrbitMeanElements for testing
        """
        instance = SupplementalOrbitMeanElements(
            OBJECT_NAME='bhagkaqqybuycqzhwelz',
            OBJECT_ID='czdldechavmgqpftfncb',
            EPOCH=datetime.datetime.now(datetime.timezone.utc),
            MEAN_MOTION=float(24.010229903580825),
            ECCENTRICITY=float(82.81019970703106),
            INCLINATION=float(97.16779397676319),
            RA_OF_ASC_NODE=float(5.027376585097365),
            ARG_OF_PERICENTER=float(80.08402868568761),
            MEAN_ANOMALY=float(46.467022395085586),
            EPHEMERIS_TYPE=int(23),
            CLASSIFICATION_TYPE=None,
            NORAD_CAT_ID=int(11),
            ELEMENT_SET_NO=int(39),
            REV_AT_EPOCH=int(56),
            BSTAR=float(82.95438756191342),
            MEAN_MOTION_DOT=float(97.33843934188542),
            MEAN_MOTION_DDOT=float(80.93865795635449),
            RMS=float(84.81242564628931),
            DATA_SOURCE='nhhrvyfyhmbpawbjhhps'
        )
        return instance

    
    def test_OBJECT_NAME_property(self):
        """
        Test OBJECT_NAME property
        """
        test_value = 'bhagkaqqybuycqzhwelz'
        self.instance.OBJECT_NAME = test_value
        self.assertEqual(self.instance.OBJECT_NAME, test_value)
    
    def test_OBJECT_ID_property(self):
        """
        Test OBJECT_ID property
        """
        test_value = 'czdldechavmgqpftfncb'
        self.instance.OBJECT_ID = test_value
        self.assertEqual(self.instance.OBJECT_ID, test_value)
    
    def test_EPOCH_property(self):
        """
        Test EPOCH property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.EPOCH = test_value
        self.assertEqual(self.instance.EPOCH, test_value)
    
    def test_MEAN_MOTION_property(self):
        """
        Test MEAN_MOTION property
        """
        test_value = float(24.010229903580825)
        self.instance.MEAN_MOTION = test_value
        self.assertEqual(self.instance.MEAN_MOTION, test_value)
    
    def test_ECCENTRICITY_property(self):
        """
        Test ECCENTRICITY property
        """
        test_value = float(82.81019970703106)
        self.instance.ECCENTRICITY = test_value
        self.assertEqual(self.instance.ECCENTRICITY, test_value)
    
    def test_INCLINATION_property(self):
        """
        Test INCLINATION property
        """
        test_value = float(97.16779397676319)
        self.instance.INCLINATION = test_value
        self.assertEqual(self.instance.INCLINATION, test_value)
    
    def test_RA_OF_ASC_NODE_property(self):
        """
        Test RA_OF_ASC_NODE property
        """
        test_value = float(5.027376585097365)
        self.instance.RA_OF_ASC_NODE = test_value
        self.assertEqual(self.instance.RA_OF_ASC_NODE, test_value)
    
    def test_ARG_OF_PERICENTER_property(self):
        """
        Test ARG_OF_PERICENTER property
        """
        test_value = float(80.08402868568761)
        self.instance.ARG_OF_PERICENTER = test_value
        self.assertEqual(self.instance.ARG_OF_PERICENTER, test_value)
    
    def test_MEAN_ANOMALY_property(self):
        """
        Test MEAN_ANOMALY property
        """
        test_value = float(46.467022395085586)
        self.instance.MEAN_ANOMALY = test_value
        self.assertEqual(self.instance.MEAN_ANOMALY, test_value)
    
    def test_EPHEMERIS_TYPE_property(self):
        """
        Test EPHEMERIS_TYPE property
        """
        test_value = int(23)
        self.instance.EPHEMERIS_TYPE = test_value
        self.assertEqual(self.instance.EPHEMERIS_TYPE, test_value)
    
    def test_CLASSIFICATION_TYPE_property(self):
        """
        Test CLASSIFICATION_TYPE property
        """
        test_value = None
        self.instance.CLASSIFICATION_TYPE = test_value
        self.assertEqual(self.instance.CLASSIFICATION_TYPE, test_value)
    
    def test_NORAD_CAT_ID_property(self):
        """
        Test NORAD_CAT_ID property
        """
        test_value = int(11)
        self.instance.NORAD_CAT_ID = test_value
        self.assertEqual(self.instance.NORAD_CAT_ID, test_value)
    
    def test_ELEMENT_SET_NO_property(self):
        """
        Test ELEMENT_SET_NO property
        """
        test_value = int(39)
        self.instance.ELEMENT_SET_NO = test_value
        self.assertEqual(self.instance.ELEMENT_SET_NO, test_value)
    
    def test_REV_AT_EPOCH_property(self):
        """
        Test REV_AT_EPOCH property
        """
        test_value = int(56)
        self.instance.REV_AT_EPOCH = test_value
        self.assertEqual(self.instance.REV_AT_EPOCH, test_value)
    
    def test_BSTAR_property(self):
        """
        Test BSTAR property
        """
        test_value = float(82.95438756191342)
        self.instance.BSTAR = test_value
        self.assertEqual(self.instance.BSTAR, test_value)
    
    def test_MEAN_MOTION_DOT_property(self):
        """
        Test MEAN_MOTION_DOT property
        """
        test_value = float(97.33843934188542)
        self.instance.MEAN_MOTION_DOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DOT, test_value)
    
    def test_MEAN_MOTION_DDOT_property(self):
        """
        Test MEAN_MOTION_DDOT property
        """
        test_value = float(80.93865795635449)
        self.instance.MEAN_MOTION_DDOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DDOT, test_value)
    
    def test_RMS_property(self):
        """
        Test RMS property
        """
        test_value = float(84.81242564628931)
        self.instance.RMS = test_value
        self.assertEqual(self.instance.RMS, test_value)
    
    def test_DATA_SOURCE_property(self):
        """
        Test DATA_SOURCE property
        """
        test_value = 'nhhrvyfyhmbpawbjhhps'
        self.instance.DATA_SOURCE = test_value
        self.assertEqual(self.instance.DATA_SOURCE, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SupplementalOrbitMeanElements.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SupplementalOrbitMeanElements.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

