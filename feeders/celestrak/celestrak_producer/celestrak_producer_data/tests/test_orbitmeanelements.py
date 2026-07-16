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
            OBJECT_NAME='ysekfloensklnfrrzvnf',
            OBJECT_ID='cqhusbmpoxvaarhhtnsc',
            EPOCH=datetime.datetime.now(datetime.timezone.utc),
            MEAN_MOTION=float(8.861867796441548),
            ECCENTRICITY=float(27.001100646776788),
            INCLINATION=float(82.98841678299522),
            RA_OF_ASC_NODE=float(28.325000715454017),
            ARG_OF_PERICENTER=float(49.28176131408062),
            MEAN_ANOMALY=float(52.09625037555345),
            EPHEMERIS_TYPE=int(68),
            CLASSIFICATION_TYPE=None,
            NORAD_CAT_ID=int(92),
            ELEMENT_SET_NO=int(71),
            REV_AT_EPOCH=int(46),
            BSTAR=float(97.86467056460266),
            MEAN_MOTION_DOT=float(75.44233186397533),
            MEAN_MOTION_DDOT=float(38.06682311108385)
        )
        return instance

    
    def test_OBJECT_NAME_property(self):
        """
        Test OBJECT_NAME property
        """
        test_value = 'ysekfloensklnfrrzvnf'
        self.instance.OBJECT_NAME = test_value
        self.assertEqual(self.instance.OBJECT_NAME, test_value)
    
    def test_OBJECT_ID_property(self):
        """
        Test OBJECT_ID property
        """
        test_value = 'cqhusbmpoxvaarhhtnsc'
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
        test_value = float(8.861867796441548)
        self.instance.MEAN_MOTION = test_value
        self.assertEqual(self.instance.MEAN_MOTION, test_value)
    
    def test_ECCENTRICITY_property(self):
        """
        Test ECCENTRICITY property
        """
        test_value = float(27.001100646776788)
        self.instance.ECCENTRICITY = test_value
        self.assertEqual(self.instance.ECCENTRICITY, test_value)
    
    def test_INCLINATION_property(self):
        """
        Test INCLINATION property
        """
        test_value = float(82.98841678299522)
        self.instance.INCLINATION = test_value
        self.assertEqual(self.instance.INCLINATION, test_value)
    
    def test_RA_OF_ASC_NODE_property(self):
        """
        Test RA_OF_ASC_NODE property
        """
        test_value = float(28.325000715454017)
        self.instance.RA_OF_ASC_NODE = test_value
        self.assertEqual(self.instance.RA_OF_ASC_NODE, test_value)
    
    def test_ARG_OF_PERICENTER_property(self):
        """
        Test ARG_OF_PERICENTER property
        """
        test_value = float(49.28176131408062)
        self.instance.ARG_OF_PERICENTER = test_value
        self.assertEqual(self.instance.ARG_OF_PERICENTER, test_value)
    
    def test_MEAN_ANOMALY_property(self):
        """
        Test MEAN_ANOMALY property
        """
        test_value = float(52.09625037555345)
        self.instance.MEAN_ANOMALY = test_value
        self.assertEqual(self.instance.MEAN_ANOMALY, test_value)
    
    def test_EPHEMERIS_TYPE_property(self):
        """
        Test EPHEMERIS_TYPE property
        """
        test_value = int(68)
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
        test_value = int(92)
        self.instance.NORAD_CAT_ID = test_value
        self.assertEqual(self.instance.NORAD_CAT_ID, test_value)
    
    def test_ELEMENT_SET_NO_property(self):
        """
        Test ELEMENT_SET_NO property
        """
        test_value = int(71)
        self.instance.ELEMENT_SET_NO = test_value
        self.assertEqual(self.instance.ELEMENT_SET_NO, test_value)
    
    def test_REV_AT_EPOCH_property(self):
        """
        Test REV_AT_EPOCH property
        """
        test_value = int(46)
        self.instance.REV_AT_EPOCH = test_value
        self.assertEqual(self.instance.REV_AT_EPOCH, test_value)
    
    def test_BSTAR_property(self):
        """
        Test BSTAR property
        """
        test_value = float(97.86467056460266)
        self.instance.BSTAR = test_value
        self.assertEqual(self.instance.BSTAR, test_value)
    
    def test_MEAN_MOTION_DOT_property(self):
        """
        Test MEAN_MOTION_DOT property
        """
        test_value = float(75.44233186397533)
        self.instance.MEAN_MOTION_DOT = test_value
        self.assertEqual(self.instance.MEAN_MOTION_DOT, test_value)
    
    def test_MEAN_MOTION_DDOT_property(self):
        """
        Test MEAN_MOTION_DDOT property
        """
        test_value = float(38.06682311108385)
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

