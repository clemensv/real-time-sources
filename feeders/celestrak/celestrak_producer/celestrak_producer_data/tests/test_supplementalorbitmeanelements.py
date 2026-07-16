"""
Test case for SupplementalOrbitMeanElements
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_producer_data.org.celestrak.supplementalorbitmeanelements import SupplementalOrbitMeanElements
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
            OBJECT_NAME='iztopezdliwufrthhicy',
            OBJECT_ID='izdfllkmkmzaxpylkrln',
            EPOCH=datetime.datetime.now(datetime.timezone.utc),
            MEAN_MOTION=float(45.87431797448922),
            ECCENTRICITY=float(42.424937332362155),
            INCLINATION=float(4.459021434217869),
            RA_OF_ASC_NODE=float(46.73012520934141),
            ARG_OF_PERICENTER=float(66.74019837708191),
            MEAN_ANOMALY=float(46.90928435468504),
            EPHEMERIS_TYPE=int(86),
            CLASSIFICATION_TYPE=None,
            NORAD_CAT_ID=int(9),
            ELEMENT_SET_NO=int(46),
            REV_AT_EPOCH=int(86),
            BSTAR=float(86.24822603079373),
            MEAN_MOTION_DOT=float(96.37163530402654),
            MEAN_MOTION_DDOT=float(24.030478139744016),
            RMS=float(75.99814642954313),
            DATA_SOURCE='bnmbmhtpwdaukvxaazsd'
        )
        return instance

    
    def test_OBJECT_NAME_property(self):
        """
        Test OBJECT_NAME property
        """
        test_value = 'iztopezdliwufrthhicy'
        self.instance.OBJECT_NAME = test_value
        self.assertEqual(self.instance.OBJECT_NAME, test_value)
    
    def test_OBJECT_ID_property(self):
        """
        Test OBJECT_ID property
        """
        test_value = 'izdfllkmkmzaxpylkrln'
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
        test_value = float(45.87431797448922)
        self.instance.MEAN_MOTION = test_value
        self.assertEqual(self.instance.MEAN_MOTION, test_value)
    
    def test_ECCENTRICITY_property(self):
        """
        Test ECCENTRICITY property
        """
        test_value = float(42.424937332362155)
        self.instance.ECCENTRICITY = test_value
        self.assertEqual(self.instance.ECCENTRICITY, test_value)
    
    def test_INCLINATION_property(self):
        """
        Test INCLINATION property
        """
        test_value = float(4.459021434217869)
        self.instance.INCLINATION = test_value
        self.assertEqual(self.instance.INCLINATION, test_value)
    
    def test_RA_OF_ASC_NODE_property(self):
        """
        Test RA_OF_ASC_NODE property
        """
        test_value = float(46.73012520934141)
        self.instance.RA_OF_ASC_NODE = test_value
        self.assertEqual(self.instance.RA_OF_ASC_NODE, test_value)
    
    def test_ARG_OF_PERICENTER_property(self):
        """
        Test ARG_OF_PERICENTER property
        """
        test_value = float(66.74019837708191)
        self.instance.ARG_OF_PERICENTER = test_value
        self.assertEqual(self.instance.ARG_OF_PERICENTER, test_value)
    
    def test_MEAN_ANOMALY_property(self):
        """
        Test MEAN_ANOMALY property
        """
        test_value = float(46.90928435468504)
        self.instance.MEAN_ANOMALY = test_value
        self.assertEqual(self.instance.MEAN_ANOMALY, test_value)
    
    def test_EPHEMERIS_TYPE_property(self):
        """
        Test EPHEMERIS_TYPE property
        """
        test_value = int(86)
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
        test_value = int(9)
        self.instance.NORAD_CAT_ID = test_value
        self.assertEqual(self.instance.NORAD_CAT_ID, test_value)
    
    def test_ELEMENT_SET_NO_property(self):
        """
        Test ELEMENT_SET_NO property
        """
        test_value = int(46)
        self.instance.ELEMENT_SET_NO = test_value
        self.assertEqual(self.instance.ELEMENT_SET_NO, test_value)
    
    def test_REV_AT_EPOCH_property(self):
        """
        Test REV_AT_EPOCH property
        """
        test_value = int(86)
        self.instance.REV_AT_EPOCH = test_value
        self.assertEqual(self.instance.REV_AT_EPOCH, test_value)
    
    def test_BSTAR_property(self):
        """
        Test BSTAR property
        """
        test_value = float(86.24822603079373)
        self.instance.BSTAR = test_value
        self.assertEqual(self.instance.BSTAR, test_value)
    
    def test_MEAN_MOTION_DOT_property(self):
        """
        Test MEAN_MOTION_DOT property
        """
        test_value = float(96.37163530402654)
        self.instance.MEAN_MOTION_DOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DOT, test_value)
    
    def test_MEAN_MOTION_DDOT_property(self):
        """
        Test MEAN_MOTION_DDOT property
        """
        test_value = float(24.030478139744016)
        self.instance.MEAN_MOTION_DDOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DDOT, test_value)
    
    def test_RMS_property(self):
        """
        Test RMS property
        """
        test_value = float(75.99814642954313)
        self.instance.RMS = test_value
        self.assertEqual(self.instance.RMS, test_value)
    
    def test_DATA_SOURCE_property(self):
        """
        Test DATA_SOURCE property
        """
        test_value = 'bnmbmhtpwdaukvxaazsd'
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

