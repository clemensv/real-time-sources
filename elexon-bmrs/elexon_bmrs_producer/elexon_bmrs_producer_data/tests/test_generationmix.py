"""
Test case for GenerationMix
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from elexon_bmrs_producer_data.generationmix import GenerationMix
import datetime


class Test_GenerationMix(unittest.TestCase):
    """
    Test case for GenerationMix
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_GenerationMix.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of GenerationMix for testing
        """
        instance = GenerationMix(
            settlement_period=int(31),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(79.43561814234602),
            ccgt_mw=float(1.4818704234155655),
            coal_mw=float(59.975912391983556),
            nuclear_mw=float(30.076990053515395),
            wind_mw=float(81.21237837669578),
            ocgt_mw=float(8.79855711318972),
            oil_mw=float(65.10373679706905),
            npshyd_mw=float(44.962907729510235),
            ps_mw=float(38.36207582912965),
            intfr_mw=float(24.821551260137408),
            intned_mw=float(82.10448056215003),
            intnem_mw=float(92.25802257163124),
            intelec_mw=float(70.51250959966026),
            intifa2_mw=float(52.49877958605427),
            intnsl_mw=float(98.43737759485803),
            intvkl_mw=float(92.4311606785384),
            other_mw=float(1.7401134392235673)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(31)
        self.instance.settlement_period = test_value
        self.assertEqual(self.instance.settlement_period, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_biomass_mw_property(self):
        """
        Test biomass_mw property
        """
        test_value = float(79.43561814234602)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_ccgt_mw_property(self):
        """
        Test ccgt_mw property
        """
        test_value = float(1.4818704234155655)
        self.instance.ccgt_mw = test_value
        self.assertEqual(self.instance.ccgt_mw, test_value)
    
    def test_coal_mw_property(self):
        """
        Test coal_mw property
        """
        test_value = float(59.975912391983556)
        self.instance.coal_mw = test_value
        self.assertEqual(self.instance.coal_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(30.076990053515395)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_wind_mw_property(self):
        """
        Test wind_mw property
        """
        test_value = float(81.21237837669578)
        self.instance.wind_mw = test_value
        self.assertEqual(self.instance.wind_mw, test_value)
    
    def test_ocgt_mw_property(self):
        """
        Test ocgt_mw property
        """
        test_value = float(8.79855711318972)
        self.instance.ocgt_mw = test_value
        self.assertEqual(self.instance.ocgt_mw, test_value)
    
    def test_oil_mw_property(self):
        """
        Test oil_mw property
        """
        test_value = float(65.10373679706905)
        self.instance.oil_mw = test_value
        self.assertEqual(self.instance.oil_mw, test_value)
    
    def test_npshyd_mw_property(self):
        """
        Test npshyd_mw property
        """
        test_value = float(44.962907729510235)
        self.instance.npshyd_mw = test_value
        self.assertEqual(self.instance.npshyd_mw, test_value)
    
    def test_ps_mw_property(self):
        """
        Test ps_mw property
        """
        test_value = float(38.36207582912965)
        self.instance.ps_mw = test_value
        self.assertEqual(self.instance.ps_mw, test_value)
    
    def test_intfr_mw_property(self):
        """
        Test intfr_mw property
        """
        test_value = float(24.821551260137408)
        self.instance.intfr_mw = test_value
        self.assertEqual(self.instance.intfr_mw, test_value)
    
    def test_intned_mw_property(self):
        """
        Test intned_mw property
        """
        test_value = float(82.10448056215003)
        self.instance.intned_mw = test_value
        self.assertEqual(self.instance.intned_mw, test_value)
    
    def test_intnem_mw_property(self):
        """
        Test intnem_mw property
        """
        test_value = float(92.25802257163124)
        self.instance.intnem_mw = test_value
        self.assertEqual(self.instance.intnem_mw, test_value)
    
    def test_intelec_mw_property(self):
        """
        Test intelec_mw property
        """
        test_value = float(70.51250959966026)
        self.instance.intelec_mw = test_value
        self.assertEqual(self.instance.intelec_mw, test_value)
    
    def test_intifa2_mw_property(self):
        """
        Test intifa2_mw property
        """
        test_value = float(52.49877958605427)
        self.instance.intifa2_mw = test_value
        self.assertEqual(self.instance.intifa2_mw, test_value)
    
    def test_intnsl_mw_property(self):
        """
        Test intnsl_mw property
        """
        test_value = float(98.43737759485803)
        self.instance.intnsl_mw = test_value
        self.assertEqual(self.instance.intnsl_mw, test_value)
    
    def test_intvkl_mw_property(self):
        """
        Test intvkl_mw property
        """
        test_value = float(92.4311606785384)
        self.instance.intvkl_mw = test_value
        self.assertEqual(self.instance.intvkl_mw, test_value)
    
    def test_other_mw_property(self):
        """
        Test other_mw property
        """
        test_value = float(1.7401134392235673)
        self.instance.other_mw = test_value
        self.assertEqual(self.instance.other_mw, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = GenerationMix.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = GenerationMix.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

