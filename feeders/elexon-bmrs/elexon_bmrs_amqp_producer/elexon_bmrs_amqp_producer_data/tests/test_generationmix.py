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
            settlement_period=int(17),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(27.35495189593201),
            ccgt_mw=float(56.10844023942203),
            coal_mw=float(83.03234363667357),
            nuclear_mw=float(49.205848142750064),
            wind_mw=float(78.73153982842305),
            ocgt_mw=float(96.71288813569883),
            oil_mw=float(42.99886696912003),
            npshyd_mw=float(33.88063058283075),
            ps_mw=float(56.68145644387553),
            intfr_mw=float(59.77032308805031),
            intned_mw=float(85.81946455392868),
            intnem_mw=float(61.9982386221962),
            intelec_mw=float(35.733619853813),
            intifa2_mw=float(12.978185585728653),
            intnsl_mw=float(6.166994010563909),
            intvkl_mw=float(97.83799355106903),
            other_mw=float(2.405436001501704)
        )
        return instance

    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(17)
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
        test_value = float(27.35495189593201)
        self.instance.biomass_mw = test_value
        self.assertEqual(self.instance.biomass_mw, test_value)
    
    def test_ccgt_mw_property(self):
        """
        Test ccgt_mw property
        """
        test_value = float(56.10844023942203)
        self.instance.ccgt_mw = test_value
        self.assertEqual(self.instance.ccgt_mw, test_value)
    
    def test_coal_mw_property(self):
        """
        Test coal_mw property
        """
        test_value = float(83.03234363667357)
        self.instance.coal_mw = test_value
        self.assertEqual(self.instance.coal_mw, test_value)
    
    def test_nuclear_mw_property(self):
        """
        Test nuclear_mw property
        """
        test_value = float(49.205848142750064)
        self.instance.nuclear_mw = test_value
        self.assertEqual(self.instance.nuclear_mw, test_value)
    
    def test_wind_mw_property(self):
        """
        Test wind_mw property
        """
        test_value = float(78.73153982842305)
        self.instance.wind_mw = test_value
        self.assertEqual(self.instance.wind_mw, test_value)
    
    def test_ocgt_mw_property(self):
        """
        Test ocgt_mw property
        """
        test_value = float(96.71288813569883)
        self.instance.ocgt_mw = test_value
        self.assertEqual(self.instance.ocgt_mw, test_value)
    
    def test_oil_mw_property(self):
        """
        Test oil_mw property
        """
        test_value = float(42.99886696912003)
        self.instance.oil_mw = test_value
        self.assertEqual(self.instance.oil_mw, test_value)
    
    def test_npshyd_mw_property(self):
        """
        Test npshyd_mw property
        """
        test_value = float(33.88063058283075)
        self.instance.npshyd_mw = test_value
        self.assertEqual(self.instance.npshyd_mw, test_value)
    
    def test_ps_mw_property(self):
        """
        Test ps_mw property
        """
        test_value = float(56.68145644387553)
        self.instance.ps_mw = test_value
        self.assertEqual(self.instance.ps_mw, test_value)
    
    def test_intfr_mw_property(self):
        """
        Test intfr_mw property
        """
        test_value = float(59.77032308805031)
        self.instance.intfr_mw = test_value
        self.assertEqual(self.instance.intfr_mw, test_value)
    
    def test_intned_mw_property(self):
        """
        Test intned_mw property
        """
        test_value = float(85.81946455392868)
        self.instance.intned_mw = test_value
        self.assertEqual(self.instance.intned_mw, test_value)
    
    def test_intnem_mw_property(self):
        """
        Test intnem_mw property
        """
        test_value = float(61.9982386221962)
        self.instance.intnem_mw = test_value
        self.assertEqual(self.instance.intnem_mw, test_value)
    
    def test_intelec_mw_property(self):
        """
        Test intelec_mw property
        """
        test_value = float(35.733619853813)
        self.instance.intelec_mw = test_value
        self.assertEqual(self.instance.intelec_mw, test_value)
    
    def test_intifa2_mw_property(self):
        """
        Test intifa2_mw property
        """
        test_value = float(12.978185585728653)
        self.instance.intifa2_mw = test_value
        self.assertEqual(self.instance.intifa2_mw, test_value)
    
    def test_intnsl_mw_property(self):
        """
        Test intnsl_mw property
        """
        test_value = float(6.166994010563909)
        self.instance.intnsl_mw = test_value
        self.assertEqual(self.instance.intnsl_mw, test_value)
    
    def test_intvkl_mw_property(self):
        """
        Test intvkl_mw property
        """
        test_value = float(97.83799355106903)
        self.instance.intvkl_mw = test_value
        self.assertEqual(self.instance.intvkl_mw, test_value)
    
    def test_other_mw_property(self):
        """
        Test other_mw property
        """
        test_value = float(2.405436001501704)
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

