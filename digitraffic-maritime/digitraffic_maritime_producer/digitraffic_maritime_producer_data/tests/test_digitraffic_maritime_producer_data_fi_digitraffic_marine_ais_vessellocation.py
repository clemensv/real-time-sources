"""
Test case for VesselLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_producer_data.fi.digitraffic.marine.ais.vessellocation import VesselLocation


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
            mmsi=int(99),
            time=int(42),
            sog=float(86.51702431110199),
            cog=float(62.20543206976588),
            navStat=int(68),
            rot=int(24),
            posAcc=False,
            raim=False,
            heading=int(55),
            lon=float(95.20060655973259),
            lat=float(69.67812284275401)
        )
        return instance

    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(99)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_time_property(self):
        """
        Test time property
        """
        test_value = int(42)
        self.instance.time = test_value
        self.assertEqual(self.instance.time, test_value)
    
    def test_sog_property(self):
        """
        Test sog property
        """
        test_value = float(86.51702431110199)
        self.instance.sog = test_value
        self.assertEqual(self.instance.sog, test_value)
    
    def test_cog_property(self):
        """
        Test cog property
        """
        test_value = float(62.20543206976588)
        self.instance.cog = test_value
        self.assertEqual(self.instance.cog, test_value)
    
    def test_navStat_property(self):
        """
        Test navStat property
        """
        test_value = int(68)
        self.instance.navStat = test_value
        self.assertEqual(self.instance.navStat, test_value)
    
    def test_rot_property(self):
        """
        Test rot property
        """
        test_value = int(24)
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
        test_value = False
        self.instance.raim = test_value
        self.assertEqual(self.instance.raim, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(55)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(95.20060655973259)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(69.67812284275401)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
