"""
Test case for VesselLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.vessellocation import VesselLocation


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
            mmsi=int(94),
            time=int(17),
            sog=float(33.203911035339814),
            cog=float(49.70426613118839),
            navStat=int(47),
            rot=int(78),
            posAcc=False,
            raim=True,
            heading=int(34),
            lon=float(33.0404537129625),
            lat=float(56.610378070389864)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(94)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(17)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_sog_property(self):
        """
        Test sog property
        """
        test_value = float(33.203911035339814)
        self.instance.sog = test_value
        self.assertEqual(self.instance.sog, test_value)
    
    def test_cog_property(self):
        """
        Test cog property
        """
        test_value = float(49.70426613118839)
        self.instance.cog = test_value
        self.assertEqual(self.instance.cog, test_value)
    
    def test_navStat_property(self):
        """
        Test navStat property
        """
        test_value = int(47)
        self.instance.navStat = test_value
        self.assertEqual(self.instance.navStat, test_value)
    
    def test_rot_property(self):
        """
        Test rot property
        """
        test_value = int(78)
        self.instance.rot = test_value
        self.assertEqual(self.instance.rot, test_value)
    
    def test_posAcc_property(self):
        """
        Test posAcc property
        """
        test_value = False
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
        test_value = int(34)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(33.0404537129625)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(56.610378070389864)
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

