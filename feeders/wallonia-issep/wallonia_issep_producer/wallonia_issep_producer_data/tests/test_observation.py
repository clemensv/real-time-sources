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
            configuration_id='yddqvdtitosopvqsmemf',
            province='jwxulooymsqghoymyroo',
            moment='dchibusvrcgtqanlphoa',
            co=int(40),
            no=int(34),
            no2=int(12),
            o3no2=int(16),
            ppbno=float(44.734614817138116),
            ppbno_statut=int(44),
            ppbno2=float(7.232074913561581),
            ppbno2_statut=int(93),
            ppbo3=float(74.51127606616244),
            ppbo3_statut=int(21),
            ugpcmno=float(84.44686506945736),
            ugpcmno_statut=int(81),
            ugpcmno2=float(72.99132450163421),
            ugpcmno2_statut=int(42),
            ugpcmo3=float(85.32440589530457),
            ugpcmo3_statut=int(49),
            bme_t=float(0.36475030340782366),
            bme_t_statut=int(28),
            bme_pres=int(43),
            bme_pres_statut=int(41),
            bme_rh=float(30.380847360451966),
            bme_rh_statut=int(72),
            pm1=float(47.97138726130357),
            pm1_statut=int(35),
            pm25=float(17.80467110854662),
            pm25_statut=int(68),
            pm4=float(47.735387559005204),
            pm4_statut=int(18),
            pm10=float(59.854711330113794),
            pm10_statut=int(71),
            vbat=float(94.27714869301175),
            vbat_statut=int(78),
            mwh_bat=float(2.431951899230411),
            mwh_pv=float(62.67861435867768),
            co_rf=float(6.5313160107893005),
            no_rf=float(7.214222679055993),
            no2_rf=float(88.51154031804238),
            o3no2_rf=float(74.84603810215708),
            o3_rf=float(84.35992724972756),
            pm10_rf=float(26.56897316788802)
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'yddqvdtitosopvqsmemf'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'jwxulooymsqghoymyroo'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_moment_property(self):
        """
        Test moment property
        """
        test_value = 'dchibusvrcgtqanlphoa'
        self.instance.moment = test_value
        self.assertEqual(self.instance.moment, test_value)
    
    def test_co_property(self):
        """
        Test co property
        """
        test_value = int(40)
        self.instance.co = test_value
        self.assertEqual(self.instance.co, test_value)
    
    def test_no_property(self):
        """
        Test no property
        """
        test_value = int(34)
        self.instance.no = test_value
        self.assertEqual(self.instance.no, test_value)
    
    def test_no2_property(self):
        """
        Test no2 property
        """
        test_value = int(12)
        self.instance.no2 = test_value
        self.assertEqual(self.instance.no2, test_value)
    
    def test_o3no2_property(self):
        """
        Test o3no2 property
        """
        test_value = int(16)
        self.instance.o3no2 = test_value
        self.assertEqual(self.instance.o3no2, test_value)
    
    def test_ppbno_property(self):
        """
        Test ppbno property
        """
        test_value = float(44.734614817138116)
        self.instance.ppbno = test_value
        self.assertEqual(self.instance.ppbno, test_value)
    
    def test_ppbno_statut_property(self):
        """
        Test ppbno_statut property
        """
        test_value = int(44)
        self.instance.ppbno_statut = test_value
        self.assertEqual(self.instance.ppbno_statut, test_value)
    
    def test_ppbno2_property(self):
        """
        Test ppbno2 property
        """
        test_value = float(7.232074913561581)
        self.instance.ppbno2 = test_value
        self.assertEqual(self.instance.ppbno2, test_value)
    
    def test_ppbno2_statut_property(self):
        """
        Test ppbno2_statut property
        """
        test_value = int(93)
        self.instance.ppbno2_statut = test_value
        self.assertEqual(self.instance.ppbno2_statut, test_value)
    
    def test_ppbo3_property(self):
        """
        Test ppbo3 property
        """
        test_value = float(74.51127606616244)
        self.instance.ppbo3 = test_value
        self.assertEqual(self.instance.ppbo3, test_value)
    
    def test_ppbo3_statut_property(self):
        """
        Test ppbo3_statut property
        """
        test_value = int(21)
        self.instance.ppbo3_statut = test_value
        self.assertEqual(self.instance.ppbo3_statut, test_value)
    
    def test_ugpcmno_property(self):
        """
        Test ugpcmno property
        """
        test_value = float(84.44686506945736)
        self.instance.ugpcmno = test_value
        self.assertEqual(self.instance.ugpcmno, test_value)
    
    def test_ugpcmno_statut_property(self):
        """
        Test ugpcmno_statut property
        """
        test_value = int(81)
        self.instance.ugpcmno_statut = test_value
        self.assertEqual(self.instance.ugpcmno_statut, test_value)
    
    def test_ugpcmno2_property(self):
        """
        Test ugpcmno2 property
        """
        test_value = float(72.99132450163421)
        self.instance.ugpcmno2 = test_value
        self.assertEqual(self.instance.ugpcmno2, test_value)
    
    def test_ugpcmno2_statut_property(self):
        """
        Test ugpcmno2_statut property
        """
        test_value = int(42)
        self.instance.ugpcmno2_statut = test_value
        self.assertEqual(self.instance.ugpcmno2_statut, test_value)
    
    def test_ugpcmo3_property(self):
        """
        Test ugpcmo3 property
        """
        test_value = float(85.32440589530457)
        self.instance.ugpcmo3 = test_value
        self.assertEqual(self.instance.ugpcmo3, test_value)
    
    def test_ugpcmo3_statut_property(self):
        """
        Test ugpcmo3_statut property
        """
        test_value = int(49)
        self.instance.ugpcmo3_statut = test_value
        self.assertEqual(self.instance.ugpcmo3_statut, test_value)
    
    def test_bme_t_property(self):
        """
        Test bme_t property
        """
        test_value = float(0.36475030340782366)
        self.instance.bme_t = test_value
        self.assertEqual(self.instance.bme_t, test_value)
    
    def test_bme_t_statut_property(self):
        """
        Test bme_t_statut property
        """
        test_value = int(28)
        self.instance.bme_t_statut = test_value
        self.assertEqual(self.instance.bme_t_statut, test_value)
    
    def test_bme_pres_property(self):
        """
        Test bme_pres property
        """
        test_value = int(43)
        self.instance.bme_pres = test_value
        self.assertEqual(self.instance.bme_pres, test_value)
    
    def test_bme_pres_statut_property(self):
        """
        Test bme_pres_statut property
        """
        test_value = int(41)
        self.instance.bme_pres_statut = test_value
        self.assertEqual(self.instance.bme_pres_statut, test_value)
    
    def test_bme_rh_property(self):
        """
        Test bme_rh property
        """
        test_value = float(30.380847360451966)
        self.instance.bme_rh = test_value
        self.assertEqual(self.instance.bme_rh, test_value)
    
    def test_bme_rh_statut_property(self):
        """
        Test bme_rh_statut property
        """
        test_value = int(72)
        self.instance.bme_rh_statut = test_value
        self.assertEqual(self.instance.bme_rh_statut, test_value)
    
    def test_pm1_property(self):
        """
        Test pm1 property
        """
        test_value = float(47.97138726130357)
        self.instance.pm1 = test_value
        self.assertEqual(self.instance.pm1, test_value)
    
    def test_pm1_statut_property(self):
        """
        Test pm1_statut property
        """
        test_value = int(35)
        self.instance.pm1_statut = test_value
        self.assertEqual(self.instance.pm1_statut, test_value)
    
    def test_pm25_property(self):
        """
        Test pm25 property
        """
        test_value = float(17.80467110854662)
        self.instance.pm25 = test_value
        self.assertEqual(self.instance.pm25, test_value)
    
    def test_pm25_statut_property(self):
        """
        Test pm25_statut property
        """
        test_value = int(68)
        self.instance.pm25_statut = test_value
        self.assertEqual(self.instance.pm25_statut, test_value)
    
    def test_pm4_property(self):
        """
        Test pm4 property
        """
        test_value = float(47.735387559005204)
        self.instance.pm4 = test_value
        self.assertEqual(self.instance.pm4, test_value)
    
    def test_pm4_statut_property(self):
        """
        Test pm4_statut property
        """
        test_value = int(18)
        self.instance.pm4_statut = test_value
        self.assertEqual(self.instance.pm4_statut, test_value)
    
    def test_pm10_property(self):
        """
        Test pm10 property
        """
        test_value = float(59.854711330113794)
        self.instance.pm10 = test_value
        self.assertEqual(self.instance.pm10, test_value)
    
    def test_pm10_statut_property(self):
        """
        Test pm10_statut property
        """
        test_value = int(71)
        self.instance.pm10_statut = test_value
        self.assertEqual(self.instance.pm10_statut, test_value)
    
    def test_vbat_property(self):
        """
        Test vbat property
        """
        test_value = float(94.27714869301175)
        self.instance.vbat = test_value
        self.assertEqual(self.instance.vbat, test_value)
    
    def test_vbat_statut_property(self):
        """
        Test vbat_statut property
        """
        test_value = int(78)
        self.instance.vbat_statut = test_value
        self.assertEqual(self.instance.vbat_statut, test_value)
    
    def test_mwh_bat_property(self):
        """
        Test mwh_bat property
        """
        test_value = float(2.431951899230411)
        self.instance.mwh_bat = test_value
        self.assertEqual(self.instance.mwh_bat, test_value)
    
    def test_mwh_pv_property(self):
        """
        Test mwh_pv property
        """
        test_value = float(62.67861435867768)
        self.instance.mwh_pv = test_value
        self.assertEqual(self.instance.mwh_pv, test_value)
    
    def test_co_rf_property(self):
        """
        Test co_rf property
        """
        test_value = float(6.5313160107893005)
        self.instance.co_rf = test_value
        self.assertEqual(self.instance.co_rf, test_value)
    
    def test_no_rf_property(self):
        """
        Test no_rf property
        """
        test_value = float(7.214222679055993)
        self.instance.no_rf = test_value
        self.assertEqual(self.instance.no_rf, test_value)
    
    def test_no2_rf_property(self):
        """
        Test no2_rf property
        """
        test_value = float(88.51154031804238)
        self.instance.no2_rf = test_value
        self.assertEqual(self.instance.no2_rf, test_value)
    
    def test_o3no2_rf_property(self):
        """
        Test o3no2_rf property
        """
        test_value = float(74.84603810215708)
        self.instance.o3no2_rf = test_value
        self.assertEqual(self.instance.o3no2_rf, test_value)
    
    def test_o3_rf_property(self):
        """
        Test o3_rf property
        """
        test_value = float(84.35992724972756)
        self.instance.o3_rf = test_value
        self.assertEqual(self.instance.o3_rf, test_value)
    
    def test_pm10_rf_property(self):
        """
        Test pm10_rf property
        """
        test_value = float(26.56897316788802)
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

