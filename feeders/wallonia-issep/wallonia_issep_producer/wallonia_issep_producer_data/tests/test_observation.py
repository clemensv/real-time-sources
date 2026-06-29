"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wallonia_issep_producer_data.observation import Observation


class Test_Observation(unittest.TestCase):
    """
    Test case for Observation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Observation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Observation for testing
        """
        instance = Observation(
            configuration_id='xakzbrewrkwiptrwrpjn',
            province='jugyuprrgkxkijlpthsn',
            moment='herjcehovylqwxgxhmzg',
            co=int(76),
            no=int(80),
            no2=int(49),
            o3no2=int(72),
            ppbno=float(52.64969667866994),
            ppbno_statut=int(10),
            ppbno2=float(71.51104336430745),
            ppbno2_statut=int(50),
            ppbo3=float(40.455050102339655),
            ppbo3_statut=int(68),
            ugpcmno=float(81.45425151519696),
            ugpcmno_statut=int(69),
            ugpcmno2=float(80.1577849376357),
            ugpcmno2_statut=int(91),
            ugpcmo3=float(91.72987191284605),
            ugpcmo3_statut=int(26),
            bme_t=float(40.983098164816035),
            bme_t_statut=int(69),
            bme_pres=int(35),
            bme_pres_statut=int(100),
            bme_rh=float(98.36196207249188),
            bme_rh_statut=int(38),
            pm1=float(77.7163171438193),
            pm1_statut=int(81),
            pm25=float(67.03957309111462),
            pm25_statut=int(87),
            pm4=float(26.12133601843636),
            pm4_statut=int(62),
            pm10=float(87.12768402939724),
            pm10_statut=int(68),
            vbat=float(86.20818188614055),
            vbat_statut=int(94),
            mwh_bat=float(13.562347610963421),
            mwh_pv=float(76.56206203898574),
            co_rf=float(5.247244104611881),
            no_rf=float(87.0307633772953),
            no2_rf=float(18.851085418508816),
            o3no2_rf=float(86.91146946588508),
            o3_rf=float(21.757460803844587),
            pm10_rf=float(40.57455241865049)
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'xakzbrewrkwiptrwrpjn'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'jugyuprrgkxkijlpthsn'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_moment_property(self):
        """
        Test moment property
        """
        test_value = 'herjcehovylqwxgxhmzg'
        self.instance.moment = test_value
        self.assertEqual(self.instance.moment, test_value)
    
    def test_co_property(self):
        """
        Test co property
        """
        test_value = int(76)
        self.instance.co = test_value
        self.assertEqual(self.instance.co, test_value)
    
    def test_no_property(self):
        """
        Test no property
        """
        test_value = int(80)
        self.instance.no = test_value
        self.assertEqual(self.instance.no, test_value)
    
    def test_no2_property(self):
        """
        Test no2 property
        """
        test_value = int(49)
        self.instance.no2 = test_value
        self.assertEqual(self.instance.no2, test_value)
    
    def test_o3no2_property(self):
        """
        Test o3no2 property
        """
        test_value = int(72)
        self.instance.o3no2 = test_value
        self.assertEqual(self.instance.o3no2, test_value)
    
    def test_ppbno_property(self):
        """
        Test ppbno property
        """
        test_value = float(52.64969667866994)
        self.instance.ppbno = test_value
        self.assertEqual(self.instance.ppbno, test_value)
    
    def test_ppbno_statut_property(self):
        """
        Test ppbno_statut property
        """
        test_value = int(10)
        self.instance.ppbno_statut = test_value
        self.assertEqual(self.instance.ppbno_statut, test_value)
    
    def test_ppbno2_property(self):
        """
        Test ppbno2 property
        """
        test_value = float(71.51104336430745)
        self.instance.ppbno2 = test_value
        self.assertEqual(self.instance.ppbno2, test_value)
    
    def test_ppbno2_statut_property(self):
        """
        Test ppbno2_statut property
        """
        test_value = int(50)
        self.instance.ppbno2_statut = test_value
        self.assertEqual(self.instance.ppbno2_statut, test_value)
    
    def test_ppbo3_property(self):
        """
        Test ppbo3 property
        """
        test_value = float(40.455050102339655)
        self.instance.ppbo3 = test_value
        self.assertEqual(self.instance.ppbo3, test_value)
    
    def test_ppbo3_statut_property(self):
        """
        Test ppbo3_statut property
        """
        test_value = int(68)
        self.instance.ppbo3_statut = test_value
        self.assertEqual(self.instance.ppbo3_statut, test_value)
    
    def test_ugpcmno_property(self):
        """
        Test ugpcmno property
        """
        test_value = float(81.45425151519696)
        self.instance.ugpcmno = test_value
        self.assertEqual(self.instance.ugpcmno, test_value)
    
    def test_ugpcmno_statut_property(self):
        """
        Test ugpcmno_statut property
        """
        test_value = int(69)
        self.instance.ugpcmno_statut = test_value
        self.assertEqual(self.instance.ugpcmno_statut, test_value)
    
    def test_ugpcmno2_property(self):
        """
        Test ugpcmno2 property
        """
        test_value = float(80.1577849376357)
        self.instance.ugpcmno2 = test_value
        self.assertEqual(self.instance.ugpcmno2, test_value)
    
    def test_ugpcmno2_statut_property(self):
        """
        Test ugpcmno2_statut property
        """
        test_value = int(91)
        self.instance.ugpcmno2_statut = test_value
        self.assertEqual(self.instance.ugpcmno2_statut, test_value)
    
    def test_ugpcmo3_property(self):
        """
        Test ugpcmo3 property
        """
        test_value = float(91.72987191284605)
        self.instance.ugpcmo3 = test_value
        self.assertEqual(self.instance.ugpcmo3, test_value)
    
    def test_ugpcmo3_statut_property(self):
        """
        Test ugpcmo3_statut property
        """
        test_value = int(26)
        self.instance.ugpcmo3_statut = test_value
        self.assertEqual(self.instance.ugpcmo3_statut, test_value)
    
    def test_bme_t_property(self):
        """
        Test bme_t property
        """
        test_value = float(40.983098164816035)
        self.instance.bme_t = test_value
        self.assertEqual(self.instance.bme_t, test_value)
    
    def test_bme_t_statut_property(self):
        """
        Test bme_t_statut property
        """
        test_value = int(69)
        self.instance.bme_t_statut = test_value
        self.assertEqual(self.instance.bme_t_statut, test_value)
    
    def test_bme_pres_property(self):
        """
        Test bme_pres property
        """
        test_value = int(35)
        self.instance.bme_pres = test_value
        self.assertEqual(self.instance.bme_pres, test_value)
    
    def test_bme_pres_statut_property(self):
        """
        Test bme_pres_statut property
        """
        test_value = int(100)
        self.instance.bme_pres_statut = test_value
        self.assertEqual(self.instance.bme_pres_statut, test_value)
    
    def test_bme_rh_property(self):
        """
        Test bme_rh property
        """
        test_value = float(98.36196207249188)
        self.instance.bme_rh = test_value
        self.assertEqual(self.instance.bme_rh, test_value)
    
    def test_bme_rh_statut_property(self):
        """
        Test bme_rh_statut property
        """
        test_value = int(38)
        self.instance.bme_rh_statut = test_value
        self.assertEqual(self.instance.bme_rh_statut, test_value)
    
    def test_pm1_property(self):
        """
        Test pm1 property
        """
        test_value = float(77.7163171438193)
        self.instance.pm1 = test_value
        self.assertEqual(self.instance.pm1, test_value)
    
    def test_pm1_statut_property(self):
        """
        Test pm1_statut property
        """
        test_value = int(81)
        self.instance.pm1_statut = test_value
        self.assertEqual(self.instance.pm1_statut, test_value)
    
    def test_pm25_property(self):
        """
        Test pm25 property
        """
        test_value = float(67.03957309111462)
        self.instance.pm25 = test_value
        self.assertEqual(self.instance.pm25, test_value)
    
    def test_pm25_statut_property(self):
        """
        Test pm25_statut property
        """
        test_value = int(87)
        self.instance.pm25_statut = test_value
        self.assertEqual(self.instance.pm25_statut, test_value)
    
    def test_pm4_property(self):
        """
        Test pm4 property
        """
        test_value = float(26.12133601843636)
        self.instance.pm4 = test_value
        self.assertEqual(self.instance.pm4, test_value)
    
    def test_pm4_statut_property(self):
        """
        Test pm4_statut property
        """
        test_value = int(62)
        self.instance.pm4_statut = test_value
        self.assertEqual(self.instance.pm4_statut, test_value)
    
    def test_pm10_property(self):
        """
        Test pm10 property
        """
        test_value = float(87.12768402939724)
        self.instance.pm10 = test_value
        self.assertEqual(self.instance.pm10, test_value)
    
    def test_pm10_statut_property(self):
        """
        Test pm10_statut property
        """
        test_value = int(68)
        self.instance.pm10_statut = test_value
        self.assertEqual(self.instance.pm10_statut, test_value)
    
    def test_vbat_property(self):
        """
        Test vbat property
        """
        test_value = float(86.20818188614055)
        self.instance.vbat = test_value
        self.assertEqual(self.instance.vbat, test_value)
    
    def test_vbat_statut_property(self):
        """
        Test vbat_statut property
        """
        test_value = int(94)
        self.instance.vbat_statut = test_value
        self.assertEqual(self.instance.vbat_statut, test_value)
    
    def test_mwh_bat_property(self):
        """
        Test mwh_bat property
        """
        test_value = float(13.562347610963421)
        self.instance.mwh_bat = test_value
        self.assertEqual(self.instance.mwh_bat, test_value)
    
    def test_mwh_pv_property(self):
        """
        Test mwh_pv property
        """
        test_value = float(76.56206203898574)
        self.instance.mwh_pv = test_value
        self.assertEqual(self.instance.mwh_pv, test_value)
    
    def test_co_rf_property(self):
        """
        Test co_rf property
        """
        test_value = float(5.247244104611881)
        self.instance.co_rf = test_value
        self.assertEqual(self.instance.co_rf, test_value)
    
    def test_no_rf_property(self):
        """
        Test no_rf property
        """
        test_value = float(87.0307633772953)
        self.instance.no_rf = test_value
        self.assertEqual(self.instance.no_rf, test_value)
    
    def test_no2_rf_property(self):
        """
        Test no2_rf property
        """
        test_value = float(18.851085418508816)
        self.instance.no2_rf = test_value
        self.assertEqual(self.instance.no2_rf, test_value)
    
    def test_o3no2_rf_property(self):
        """
        Test o3no2_rf property
        """
        test_value = float(86.91146946588508)
        self.instance.o3no2_rf = test_value
        self.assertEqual(self.instance.o3no2_rf, test_value)
    
    def test_o3_rf_property(self):
        """
        Test o3_rf property
        """
        test_value = float(21.757460803844587)
        self.instance.o3_rf = test_value
        self.assertEqual(self.instance.o3_rf, test_value)
    
    def test_pm10_rf_property(self):
        """
        Test pm10_rf property
        """
        test_value = float(40.57455241865049)
        self.instance.pm10_rf = test_value
        self.assertEqual(self.instance.pm10_rf, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Observation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Observation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

