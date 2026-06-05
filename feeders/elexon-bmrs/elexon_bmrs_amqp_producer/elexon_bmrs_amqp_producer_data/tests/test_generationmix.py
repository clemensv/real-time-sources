"""
Test case for GenerationMix
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from elexon_bmrs_amqp_producer_data.generationmix import GenerationMix
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
            settlement_period=int(13),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(25.430720655304363),
            ccgt_mw=float(12.122777775949011),
            coal_mw=float(25.253046729587346),
            nuclear_mw=float(87.95554810479271),
            wind_mw=float(10.556266702993689),
            ocgt_mw=float(46.42045265140909),
            oil_mw=float(24.880621349153408),
            npshyd_mw=float(29.946773262444292),
            ps_mw=float(48.89798198962871),
            intfr_mw=float(0.9422842417877275),
            intned_mw=float(17.049345444063157),
            intnem_mw=float(2.3533545653587895),
            intelec_mw=float(46.282894428228886),
            intifa2_mw=float(43.263098475554465),
            intnsl_mw=float(97.39571915118049),
            intvkl_mw=float(4.846599312006427),
            other_mw=float(15.479370137353888)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(13)
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
        test_value = float(25.430720655304363)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_ccgt_mw_property(self):
        """
        Test ccgt_mw property
        """
        test_value = float(12.122777775949011)
        self.instance.ccgt_mw = test_value
        self.assertEqual(self.instance.ccgt_mw, test_value)
    
    def test_coal_mw_property(self):
        """
        Test coal_mw property
        """
        test_value = float(25.253046729587346)
        self.instance.coal_mw = test_value
        self.assertEqual(self.instance.coal_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(87.95554810479271)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_wind_mw_property(self):
        """
        Test wind_mw property
        """
        test_value = float(10.556266702993689)
        self.instance.wind_mw = test_value
        self.assertEqual(self.instance.wind_mw, test_value)
    
    def test_ocgt_mw_property(self):
        """
        Test ocgt_mw property
        """
        test_value = float(46.42045265140909)
        self.instance.ocgt_mw = test_value
        self.assertEqual(self.instance.ocgt_mw, test_value)
    
    def test_oil_mw_property(self):
        """
        Test oil_mw property
        """
        test_value = float(24.880621349153408)
        self.instance.oil_mw = test_value
        self.assertEqual(self.instance.oil_mw, test_value)
    
    def test_npshyd_mw_property(self):
        """
        Test npshyd_mw property
        """
        test_value = float(29.946773262444292)
        self.instance.npshyd_mw = test_value
        self.assertEqual(self.instance.npshyd_mw, test_value)
    
    def test_ps_mw_property(self):
        """
        Test ps_mw property
        """
        test_value = float(48.89798198962871)
        self.instance.ps_mw = test_value
        self.assertEqual(self.instance.ps_mw, test_value)
    
    def test_intfr_mw_property(self):
        """
        Test intfr_mw property
        """
        test_value = float(0.9422842417877275)
        self.instance.intfr_mw = test_value
        self.assertEqual(self.instance.intfr_mw, test_value)
    
    def test_intned_mw_property(self):
        """
        Test intned_mw property
        """
        test_value = float(17.049345444063157)
        self.instance.intned_mw = test_value
        self.assertEqual(self.instance.intned_mw, test_value)
    
    def test_intnem_mw_property(self):
        """
        Test intnem_mw property
        """
        test_value = float(2.3533545653587895)
        self.instance.intnem_mw = test_value
        self.assertEqual(self.instance.intnem_mw, test_value)
    
    def test_intelec_mw_property(self):
        """
        Test intelec_mw property
        """
        test_value = float(46.282894428228886)
        self.instance.intelec_mw = test_value
        self.assertEqual(self.instance.intelec_mw, test_value)
    
    def test_intifa2_mw_property(self):
        """
        Test intifa2_mw property
        """
        test_value = float(43.263098475554465)
        self.instance.intifa2_mw = test_value
        self.assertEqual(self.instance.intifa2_mw, test_value)
    
    def test_intnsl_mw_property(self):
        """
        Test intnsl_mw property
        """
        test_value = float(97.39571915118049)
        self.instance.intnsl_mw = test_value
        self.assertEqual(self.instance.intnsl_mw, test_value)
    
    def test_intvkl_mw_property(self):
        """
        Test intvkl_mw property
        """
        test_value = float(4.846599312006427)
        self.instance.intvkl_mw = test_value
        self.assertEqual(self.instance.intvkl_mw, test_value)
    
    def test_other_mw_property(self):
        """
        Test other_mw property
        """
        test_value = float(15.479370137353888)
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

