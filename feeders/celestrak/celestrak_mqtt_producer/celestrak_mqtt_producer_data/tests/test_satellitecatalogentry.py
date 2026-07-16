"""
Test case for SatelliteCatalogEntry
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from celestrak_mqtt_producer_data.org.celestrak.satellitecatalogentry import SatelliteCatalogEntry
from typing import Any
import datetime


class Test_SatelliteCatalogEntry(unittest.TestCase):
    """
    Test case for SatelliteCatalogEntry
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SatelliteCatalogEntry.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SatelliteCatalogEntry for testing
        """
        instance = SatelliteCatalogEntry(
            OBJECT_NAME='qnetfwkofdupeiddijqj',
            OBJECT_ID='oyadhryddycntihwgcxq',
            NORAD_CAT_ID=int(17),
            OBJECT_TYPE=None,
            OPS_STATUS_CODE='dqudjmjghizdfijddurq',
            OWNER='okuhtlvbfeweiiiikdpd',
            LAUNCH_DATE=datetime.date.today(),
            LAUNCH_SITE='etyeqxkilpulhwbznpju',
            DECAY_DATE=datetime.date.today(),
            PERIOD=float(11.850213780091279),
            INCLINATION=float(54.490493762318906),
            APOGEE=int(7),
            PERIGEE=int(75),
            RCS=float(38.38954400009723),
            DATA_STATUS_CODE=None,
            ORBIT_CENTER='hnptmlczdesixiugldil',
            ORBIT_TYPE=None
        )
        return instance

    
    def test_OBJECT_NAME_property(self):
        """
        Test OBJECT_NAME property
        """
        test_value = 'qnetfwkofdupeiddijqj'
        self.instance.OBJECT_NAME = test_value
        self.assertEqual(self.instance.OBJECT_NAME, test_value)
    
    def test_OBJECT_ID_property(self):
        """
        Test OBJECT_ID property
        """
        test_value = 'oyadhryddycntihwgcxq'
        self.instance.OBJECT_ID = test_value
        self.assertEqual(self.instance.OBJECT_ID, test_value)
    
    def test_NORAD_CAT_ID_property(self):
        """
        Test NORAD_CAT_ID property
        """
        test_value = int(17)
        self.instance.NORAD_CAT_ID = test_value
        self.assertEqual(self.instance.NORAD_CAT_ID, test_value)
    
    def test_OBJECT_TYPE_property(self):
        """
        Test OBJECT_TYPE property
        """
        test_value = None
        self.instance.OBJECT_TYPE = test_value
        self.assertEqual(self.instance.OBJECT_TYPE, test_value)
    
    def test_OPS_STATUS_CODE_property(self):
        """
        Test OPS_STATUS_CODE property
        """
        test_value = 'dqudjmjghizdfijddurq'
        self.instance.OPS_STATUS_CODE = test_value
        self.assertEqual(self.instance.OPS_STATUS_CODE, test_value)
    
    def test_OWNER_property(self):
        """
        Test OWNER property
        """
        test_value = 'okuhtlvbfeweiiiikdpd'
        self.instance.OWNER = test_value
        self.assertEqual(self.instance.OWNER, test_value)
    
    def test_LAUNCH_DATE_property(self):
        """
        Test LAUNCH_DATE property
        """
        test_value = datetime.date.today()
        self.instance.LAUNCH_DATE = test_value
        self.assertEqual(self.instance.LAUNCH_DATE, test_value)
    
    def test_LAUNCH_SITE_property(self):
        """
        Test LAUNCH_SITE property
        """
        test_value = 'etyeqxkilpulhwbznpju'
        self.instance.LAUNCH_SITE = test_value
        self.assertEqual(self.instance.LAUNCH_SITE, test_value)
    
    def test_DECAY_DATE_property(self):
        """
        Test DECAY_DATE property
        """
        test_value = datetime.date.today()
        self.instance.DECAY_DATE = test_value
        self.assertEqual(self.instance.DECAY_DATE, test_value)
    
    def test_PERIOD_property(self):
        """
        Test PERIOD property
        """
        test_value = float(11.850213780091279)
        self.instance.PERIOD = test_value
        self.assertEqual(self.instance.PERIOD, test_value)
    
    def test_INCLINATION_property(self):
        """
        Test INCLINATION property
        """
        test_value = float(54.490493762318906)
        self.instance.INCLINATION = test_value
        self.assertEqual(self.instance.INCLINATION, test_value)
    
    def test_APOGEE_property(self):
        """
        Test APOGEE property
        """
        test_value = int(7)
        self.instance.APOGEE = test_value
        self.assertEqual(self.instance.APOGEE, test_value)
    
    def test_PERIGEE_property(self):
        """
        Test PERIGEE property
        """
        test_value = int(75)
        self.instance.PERIGEE = test_value
        self.assertEqual(self.instance.PERIGEE, test_value)
    
    def test_RCS_property(self):
        """
        Test RCS property
        """
        test_value = float(38.38954400009723)
        self.instance.RCS = test_value
        self.assertEqual(self.instance.RCS, test_value)
    
    def test_DATA_STATUS_CODE_property(self):
        """
        Test DATA_STATUS_CODE property
        """
        test_value = None
        self.instance.DATA_STATUS_CODE = test_value
        self.assertEqual(self.instance.DATA_STATUS_CODE, test_value)
    
    def test_ORBIT_CENTER_property(self):
        """
        Test ORBIT_CENTER property
        """
        test_value = 'hnptmlczdesixiugldil'
        self.instance.ORBIT_CENTER = test_value
        self.assertEqual(self.instance.ORBIT_CENTER, test_value)
    
    def test_ORBIT_TYPE_property(self):
        """
        Test ORBIT_TYPE property
        """
        test_value = None
        self.instance.ORBIT_TYPE = test_value
        self.assertEqual(self.instance.ORBIT_TYPE, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SatelliteCatalogEntry.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SatelliteCatalogEntry.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

