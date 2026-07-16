"""
Test case for OrbitMeanElements
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_producer_data.org.celestrak.orbitmeanelements import OrbitMeanElements
from typing import Any
import datetime


class Test_OrbitMeanElements(unittest.TestCase):
    """
    Test case for OrbitMeanElements
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_OrbitMeanElements.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of OrbitMeanElements for testing
        """
        instance = OrbitMeanElements(
            OBJECT_NAME='qhuacctgqghgjbrjcwxf',
            OBJECT_ID='yliyuyeofhcjiyybrbhf',
            EPOCH=datetime.datetime.now(datetime.timezone.utc),
            MEAN_MOTION=float(26.96864869486564),
            ECCENTRICITY=float(2.313001381367008),
            INCLINATION=float(89.29084961293945),
            RA_OF_ASC_NODE=float(51.51351570850379),
            ARG_OF_PERICENTER=float(5.1183797858268765),
            MEAN_ANOMALY=float(39.05093008067099),
            EPHEMERIS_TYPE=int(15),
            CLASSIFICATION_TYPE=None,
            NORAD_CAT_ID=int(8),
            ELEMENT_SET_NO=int(7),
            REV_AT_EPOCH=int(76),
            BSTAR=float(36.89584112788773),
            MEAN_MOTION_DOT=float(0.17025166103343814),
            MEAN_MOTION_DDOT=float(19.29611145988509)
        )
        return instance

    
    def test_OBJECT_NAME_property(self):
        """
        Test OBJECT_NAME property
        """
        test_value = 'qhuacctgqghgjbrjcwxf'
        self.instance.OBJECT_NAME = test_value
        self.assertEqual(self.instance.OBJECT_NAME, test_value)
    
    def test_OBJECT_ID_property(self):
        """
        Test OBJECT_ID property
        """
        test_value = 'yliyuyeofhcjiyybrbhf'
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
        test_value = float(26.96864869486564)
        self.instance.MEAN_MOTION = test_value
        self.assertEqual(self.instance.MEAN_MOTION, test_value)
    
    def test_ECCENTRICITY_property(self):
        """
        Test ECCENTRICITY property
        """
        test_value = float(2.313001381367008)
        self.instance.ECCENTRICITY = test_value
        self.assertEqual(self.instance.ECCENTRICITY, test_value)
    
    def test_INCLINATION_property(self):
        """
        Test INCLINATION property
        """
        test_value = float(89.29084961293945)
        self.instance.INCLINATION = test_value
        self.assertEqual(self.instance.INCLINATION, test_value)
    
    def test_RA_OF_ASC_NODE_property(self):
        """
        Test RA_OF_ASC_NODE property
        """
        test_value = float(51.51351570850379)
        self.instance.RA_OF_ASC_NODE = test_value
        self.assertEqual(self.instance.RA_OF_ASC_NODE, test_value)
    
    def test_ARG_OF_PERICENTER_property(self):
        """
        Test ARG_OF_PERICENTER property
        """
        test_value = float(5.1183797858268765)
        self.instance.ARG_OF_PERICENTER = test_value
        self.assertEqual(self.instance.ARG_OF_PERICENTER, test_value)
    
    def test_MEAN_ANOMALY_property(self):
        """
        Test MEAN_ANOMALY property
        """
        test_value = float(39.05093008067099)
        self.instance.MEAN_ANOMALY = test_value
        self.assertEqual(self.instance.MEAN_ANOMALY, test_value)
    
    def test_EPHEMERIS_TYPE_property(self):
        """
        Test EPHEMERIS_TYPE property
        """
        test_value = int(15)
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
        test_value = int(8)
        self.instance.NORAD_CAT_ID = test_value
        self.assertEqual(self.instance.NORAD_CAT_ID, test_value)
    
    def test_ELEMENT_SET_NO_property(self):
        """
        Test ELEMENT_SET_NO property
        """
        test_value = int(7)
        self.instance.ELEMENT_SET_NO = test_value
        self.assertEqual(self.instance.ELEMENT_SET_NO, test_value)
    
    def test_REV_AT_EPOCH_property(self):
        """
        Test REV_AT_EPOCH property
        """
        test_value = int(76)
        self.instance.REV_AT_EPOCH = test_value
        self.assertEqual(self.instance.REV_AT_EPOCH, test_value)
    
    def test_BSTAR_property(self):
        """
        Test BSTAR property
        """
        test_value = float(36.89584112788773)
        self.instance.BSTAR = test_value
        self.assertEqual(self.instance.BSTAR, test_value)
    
    def test_MEAN_MOTION_DOT_property(self):
        """
        Test MEAN_MOTION_DOT property
        """
        test_value = float(0.17025166103343814)
        self.instance.MEAN_MOTION_DOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DOT, test_value)
    
    def test_MEAN_MOTION_DDOT_property(self):
        """
        Test MEAN_MOTION_DDOT property
        """
        test_value = float(19.29611145988509)
        self.instance.MEAN_MOTION_DDOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DDOT, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = OrbitMeanElements.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = OrbitMeanElements.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

