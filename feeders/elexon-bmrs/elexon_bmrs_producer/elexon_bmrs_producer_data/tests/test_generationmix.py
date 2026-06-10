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
            settlement_period=int(49),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(59.127534797584104),
            ccgt_mw=float(1.1985649100643148),
            coal_mw=float(69.66885434958019),
            nuclear_mw=float(6.119718802434326),
            wind_mw=float(19.983574410973304),
            ocgt_mw=float(47.09048335151893),
            oil_mw=float(21.857587162140803),
            npshyd_mw=float(4.027252957163007),
            ps_mw=float(99.52529157253322),
            intfr_mw=float(75.46613140437722),
            intned_mw=float(58.421134011382506),
            intnem_mw=float(35.90789977929013),
            intelec_mw=float(11.793727067384319),
            intifa2_mw=float(76.59303521466249),
            intnsl_mw=float(38.752115637348105),
            intvkl_mw=float(39.6217484982043),
            other_mw=float(39.11572056435364)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(49)
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
        test_value = float(59.127534797584104)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_ccgt_mw_property(self):
        """
        Test ccgt_mw property
        """
        test_value = float(1.1985649100643148)
        self.instance.ccgt_mw = test_value
        self.assertEqual(self.instance.ccgt_mw, test_value)
    
    def test_coal_mw_property(self):
        """
        Test coal_mw property
        """
        test_value = float(69.66885434958019)
        self.instance.coal_mw = test_value
        self.assertEqual(self.instance.coal_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(6.119718802434326)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_wind_mw_property(self):
        """
        Test wind_mw property
        """
        test_value = float(19.983574410973304)
        self.instance.wind_mw = test_value
        self.assertEqual(self.instance.wind_mw, test_value)
    
    def test_ocgt_mw_property(self):
        """
        Test ocgt_mw property
        """
        test_value = float(47.09048335151893)
        self.instance.ocgt_mw = test_value
        self.assertEqual(self.instance.ocgt_mw, test_value)
    
    def test_oil_mw_property(self):
        """
        Test oil_mw property
        """
        test_value = float(21.857587162140803)
        self.instance.oil_mw = test_value
        self.assertEqual(self.instance.oil_mw, test_value)
    
    def test_npshyd_mw_property(self):
        """
        Test npshyd_mw property
        """
        test_value = float(4.027252957163007)
        self.instance.npshyd_mw = test_value
        self.assertEqual(self.instance.npshyd_mw, test_value)
    
    def test_ps_mw_property(self):
        """
        Test ps_mw property
        """
        test_value = float(99.52529157253322)
        self.instance.ps_mw = test_value
        self.assertEqual(self.instance.ps_mw, test_value)
    
    def test_intfr_mw_property(self):
        """
        Test intfr_mw property
        """
        test_value = float(75.46613140437722)
        self.instance.intfr_mw = test_value
        self.assertEqual(self.instance.intfr_mw, test_value)
    
    def test_intned_mw_property(self):
        """
        Test intned_mw property
        """
        test_value = float(58.421134011382506)
        self.instance.intned_mw = test_value
        self.assertEqual(self.instance.intned_mw, test_value)
    
    def test_intnem_mw_property(self):
        """
        Test intnem_mw property
        """
        test_value = float(35.90789977929013)
        self.instance.intnem_mw = test_value
        self.assertEqual(self.instance.intnem_mw, test_value)
    
    def test_intelec_mw_property(self):
        """
        Test intelec_mw property
        """
        test_value = float(11.793727067384319)
        self.instance.intelec_mw = test_value
        self.assertEqual(self.instance.intelec_mw, test_value)
    
    def test_intifa2_mw_property(self):
        """
        Test intifa2_mw property
        """
        test_value = float(76.59303521466249)
        self.instance.intifa2_mw = test_value
        self.assertEqual(self.instance.intifa2_mw, test_value)
    
    def test_intnsl_mw_property(self):
        """
        Test intnsl_mw property
        """
        test_value = float(38.752115637348105)
        self.instance.intnsl_mw = test_value
        self.assertEqual(self.instance.intnsl_mw, test_value)
    
    def test_intvkl_mw_property(self):
        """
        Test intvkl_mw property
        """
        test_value = float(39.6217484982043)
        self.instance.intvkl_mw = test_value
        self.assertEqual(self.instance.intvkl_mw, test_value)
    
    def test_other_mw_property(self):
        """
        Test other_mw property
        """
        test_value = float(39.11572056435364)
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

