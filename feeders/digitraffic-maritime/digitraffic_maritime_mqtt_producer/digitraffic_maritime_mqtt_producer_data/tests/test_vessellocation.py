"""
Test case for VesselLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_mqtt_producer_data.vessellocation import VesselLocation


class Test_VesselLocation(unittest.TestCase):
    """
    Test case for VesselLocation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselLocation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselLocation for testing
        """
        instance = VesselLocation(
            mmsi=int(90),
            time=int(23),
            sog=float(66.87290089364814),
            cog=float(86.69470391216919),
            navStat=int(90),
            rot=int(9),
            posAcc=True,
            raim=True,
            heading=int(29),
            lon=float(79.44816604657474),
            lat=float(61.79448121586003)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(90)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(23)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_sog_property(self):
        """
        Test sog property
        """
        test_value = float(66.87290089364814)
        self.instance.sog = test_value
        self.assertEqual(self.instance.sog, test_value)
    
    def test_cog_property(self):
        """
        Test cog property
        """
        test_value = float(86.69470391216919)
        self.instance.cog = test_value
        self.assertEqual(self.instance.cog, test_value)
    
    def test_navStat_property(self):
        """
        Test navStat property
        """
        test_value = int(90)
        self.instance.navStat = test_value
        self.assertEqual(self.instance.navStat, test_value)
    
    def test_rot_property(self):
        """
        Test rot property
        """
        test_value = int(9)
        self.instance.rot = test_value
        self.assertEqual(self.instance.rot, test_value)
    
    def test_posAcc_property(self):
        """
        Test posAcc property
        """
        test_value = True
        self.instance.posAcc = test_value
        self.assertEqual(self.instance.posAcc, test_value)
    
    def test_raim_property(self):
        """
        Test raim property
        """
        test_value = True
        self.instance.raim = test_value
        self.assertEqual(self.instance.raim, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(29)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(79.44816604657474)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(61.79448121586003)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselLocation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

