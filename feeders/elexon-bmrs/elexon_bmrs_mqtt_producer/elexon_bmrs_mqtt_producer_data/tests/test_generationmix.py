"""
Test case for GenerationMix
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from elexon_bmrs_mqtt_producer_data.generationmix import GenerationMix
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
            settlement_period=int(29),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(39.323114349883014),
            ccgt_mw=float(73.82105934731635),
            coal_mw=float(8.379424031332562),
            nuclear_mw=float(71.64444842387762),
            wind_mw=float(20.869682566139957),
            ocgt_mw=float(80.82278293016873),
            oil_mw=float(90.45844921308355),
            npshyd_mw=float(43.87894105291284),
            ps_mw=float(69.4800742186866),
            intfr_mw=float(25.853750249316132),
            intned_mw=float(83.30232005558003),
            intnem_mw=float(73.47032538173353),
            intelec_mw=float(16.98088883755312),
            intifa2_mw=float(43.397670879235896),
            intnsl_mw=float(44.88655016782918),
            intvkl_mw=float(3.410861814598243),
            other_mw=float(42.84483942524877)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(29)
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
        test_value = float(39.323114349883014)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_ccgt_mw_property(self):
        """
        Test ccgt_mw property
        """
        test_value = float(73.82105934731635)
        self.instance.ccgt_mw = test_value
        self.assertEqual(self.instance.ccgt_mw, test_value)
    
    def test_coal_mw_property(self):
        """
        Test coal_mw property
        """
        test_value = float(8.379424031332562)
        self.instance.coal_mw = test_value
        self.assertEqual(self.instance.coal_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(71.64444842387762)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_wind_mw_property(self):
        """
        Test wind_mw property
        """
        test_value = float(20.869682566139957)
        self.instance.wind_mw = test_value
        self.assertEqual(self.instance.wind_mw, test_value)
    
    def test_ocgt_mw_property(self):
        """
        Test ocgt_mw property
        """
        test_value = float(80.82278293016873)
        self.instance.ocgt_mw = test_value
        self.assertEqual(self.instance.ocgt_mw, test_value)
    
    def test_oil_mw_property(self):
        """
        Test oil_mw property
        """
        test_value = float(90.45844921308355)
        self.instance.oil_mw = test_value
        self.assertEqual(self.instance.oil_mw, test_value)
    
    def test_npshyd_mw_property(self):
        """
        Test npshyd_mw property
        """
        test_value = float(43.87894105291284)
        self.instance.npshyd_mw = test_value
        self.assertEqual(self.instance.npshyd_mw, test_value)
    
    def test_ps_mw_property(self):
        """
        Test ps_mw property
        """
        test_value = float(69.4800742186866)
        self.instance.ps_mw = test_value
        self.assertEqual(self.instance.ps_mw, test_value)
    
    def test_intfr_mw_property(self):
        """
        Test intfr_mw property
        """
        test_value = float(25.853750249316132)
        self.instance.intfr_mw = test_value
        self.assertEqual(self.instance.intfr_mw, test_value)
    
    def test_intned_mw_property(self):
        """
        Test intned_mw property
        """
        test_value = float(83.30232005558003)
        self.instance.intned_mw = test_value
        self.assertEqual(self.instance.intned_mw, test_value)
    
    def test_intnem_mw_property(self):
        """
        Test intnem_mw property
        """
        test_value = float(73.47032538173353)
        self.instance.intnem_mw = test_value
        self.assertEqual(self.instance.intnem_mw, test_value)
    
    def test_intelec_mw_property(self):
        """
        Test intelec_mw property
        """
        test_value = float(16.98088883755312)
        self.instance.intelec_mw = test_value
        self.assertEqual(self.instance.intelec_mw, test_value)
    
    def test_intifa2_mw_property(self):
        """
        Test intifa2_mw property
        """
        test_value = float(43.397670879235896)
        self.instance.intifa2_mw = test_value
        self.assertEqual(self.instance.intifa2_mw, test_value)
    
    def test_intnsl_mw_property(self):
        """
        Test intnsl_mw property
        """
        test_value = float(44.88655016782918)
        self.instance.intnsl_mw = test_value
        self.assertEqual(self.instance.intnsl_mw, test_value)
    
    def test_intvkl_mw_property(self):
        """
        Test intvkl_mw property
        """
        test_value = float(3.410861814598243)
        self.instance.intvkl_mw = test_value
        self.assertEqual(self.instance.intvkl_mw, test_value)
    
    def test_other_mw_property(self):
        """
        Test other_mw property
        """
        test_value = float(42.84483942524877)
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

