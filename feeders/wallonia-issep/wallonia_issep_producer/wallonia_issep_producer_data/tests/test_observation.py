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
            configuration_id='gfulknwbzpfsgwfdytqa',
            province='dmhbsjhpbitfuvekrvpl',
            moment='vldnqtcsfjigoedxjlsm',
            co=int(83),
            no=int(31),
            no2=int(88),
            o3no2=int(60),
            ppbno=float(38.88104499599242),
            ppbno_statut=int(93),
            ppbno2=float(61.155561549765125),
            ppbno2_statut=int(22),
            ppbo3=float(47.29630332223245),
            ppbo3_statut=int(23),
            ugpcmno=float(76.39859427920483),
            ugpcmno_statut=int(63),
            ugpcmno2=float(55.45350484640309),
            ugpcmno2_statut=int(41),
            ugpcmo3=float(74.16400076119484),
            ugpcmo3_statut=int(37),
            bme_t=float(85.53752025452533),
            bme_t_statut=int(7),
            bme_pres=int(28),
            bme_pres_statut=int(61),
            bme_rh=float(77.03445825672055),
            bme_rh_statut=int(57),
            pm1=float(16.129236434611492),
            pm1_statut=int(8),
            pm25=float(43.62485923221633),
            pm25_statut=int(94),
            pm4=float(69.19844505740777),
            pm4_statut=int(84),
            pm10=float(82.15620356870048),
            pm10_statut=int(12),
            vbat=float(66.23211266578703),
            vbat_statut=int(91),
            mwh_bat=float(40.04066080529497),
            mwh_pv=float(95.24381597031412),
            co_rf=float(95.68347655258395),
            no_rf=float(62.38572091990584),
            no2_rf=float(76.05566735261662),
            o3no2_rf=float(69.69889161695323),
            o3_rf=float(78.62969919594475),
            pm10_rf=float(6.339080591731705)
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'gfulknwbzpfsgwfdytqa'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'dmhbsjhpbitfuvekrvpl'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_moment_property(self):
        """
        Test moment property
        """
        test_value = 'vldnqtcsfjigoedxjlsm'
        self.instance.moment = test_value
        self.assertEqual(self.instance.moment, test_value)
    
    def test_co_property(self):
        """
        Test co property
        """
        test_value = int(83)
        self.instance.co = test_value
        self.assertEqual(self.instance.co, test_value)
    
    def test_no_property(self):
        """
        Test no property
        """
        test_value = int(31)
        self.instance.no = test_value
        self.assertEqual(self.instance.no, test_value)
    
    def test_no2_property(self):
        """
        Test no2 property
        """
        test_value = int(88)
        self.instance.no2 = test_value
        self.assertEqual(self.instance.no2, test_value)
    
    def test_o3no2_property(self):
        """
        Test o3no2 property
        """
        test_value = int(60)
        self.instance.o3no2 = test_value
        self.assertEqual(self.instance.o3no2, test_value)
    
    def test_ppbno_property(self):
        """
        Test ppbno property
        """
        test_value = float(38.88104499599242)
        self.instance.ppbno = test_value
        self.assertEqual(self.instance.ppbno, test_value)
    
    def test_ppbno_statut_property(self):
        """
        Test ppbno_statut property
        """
        test_value = int(93)
        self.instance.ppbno_statut = test_value
        self.assertEqual(self.instance.ppbno_statut, test_value)
    
    def test_ppbno2_property(self):
        """
        Test ppbno2 property
        """
        test_value = float(61.155561549765125)
        self.instance.ppbno2 = test_value
        self.assertEqual(self.instance.ppbno2, test_value)
    
    def test_ppbno2_statut_property(self):
        """
        Test ppbno2_statut property
        """
        test_value = int(22)
        self.instance.ppbno2_statut = test_value
        self.assertEqual(self.instance.ppbno2_statut, test_value)
    
    def test_ppbo3_property(self):
        """
        Test ppbo3 property
        """
        test_value = float(47.29630332223245)
        self.instance.ppbo3 = test_value
        self.assertEqual(self.instance.ppbo3, test_value)
    
    def test_ppbo3_statut_property(self):
        """
        Test ppbo3_statut property
        """
        test_value = int(23)
        self.instance.ppbo3_statut = test_value
        self.assertEqual(self.instance.ppbo3_statut, test_value)
    
    def test_ugpcmno_property(self):
        """
        Test ugpcmno property
        """
        test_value = float(76.39859427920483)
        self.instance.ugpcmno = test_value
        self.assertEqual(self.instance.ugpcmno, test_value)
    
    def test_ugpcmno_statut_property(self):
        """
        Test ugpcmno_statut property
        """
        test_value = int(63)
        self.instance.ugpcmno_statut = test_value
        self.assertEqual(self.instance.ugpcmno_statut, test_value)
    
    def test_ugpcmno2_property(self):
        """
        Test ugpcmno2 property
        """
        test_value = float(55.45350484640309)
        self.instance.ugpcmno2 = test_value
        self.assertEqual(self.instance.ugpcmno2, test_value)
    
    def test_ugpcmno2_statut_property(self):
        """
        Test ugpcmno2_statut property
        """
        test_value = int(41)
        self.instance.ugpcmno2_statut = test_value
        self.assertEqual(self.instance.ugpcmno2_statut, test_value)
    
    def test_ugpcmo3_property(self):
        """
        Test ugpcmo3 property
        """
        test_value = float(74.16400076119484)
        self.instance.ugpcmo3 = test_value
        self.assertEqual(self.instance.ugpcmo3, test_value)
    
    def test_ugpcmo3_statut_property(self):
        """
        Test ugpcmo3_statut property
        """
        test_value = int(37)
        self.instance.ugpcmo3_statut = test_value
        self.assertEqual(self.instance.ugpcmo3_statut, test_value)
    
    def test_bme_t_property(self):
        """
        Test bme_t property
        """
        test_value = float(85.53752025452533)
        self.instance.bme_t = test_value
        self.assertEqual(self.instance.bme_t, test_value)
    
    def test_bme_t_statut_property(self):
        """
        Test bme_t_statut property
        """
        test_value = int(7)
        self.instance.bme_t_statut = test_value
        self.assertEqual(self.instance.bme_t_statut, test_value)
    
    def test_bme_pres_property(self):
        """
        Test bme_pres property
        """
        test_value = int(28)
        self.instance.bme_pres = test_value
        self.assertEqual(self.instance.bme_pres, test_value)
    
    def test_bme_pres_statut_property(self):
        """
        Test bme_pres_statut property
        """
        test_value = int(61)
        self.instance.bme_pres_statut = test_value
        self.assertEqual(self.instance.bme_pres_statut, test_value)
    
    def test_bme_rh_property(self):
        """
        Test bme_rh property
        """
        test_value = float(77.03445825672055)
        self.instance.bme_rh = test_value
        self.assertEqual(self.instance.bme_rh, test_value)
    
    def test_bme_rh_statut_property(self):
        """
        Test bme_rh_statut property
        """
        test_value = int(57)
        self.instance.bme_rh_statut = test_value
        self.assertEqual(self.instance.bme_rh_statut, test_value)
    
    def test_pm1_property(self):
        """
        Test pm1 property
        """
        test_value = float(16.129236434611492)
        self.instance.pm1 = test_value
        self.assertEqual(self.instance.pm1, test_value)
    
    def test_pm1_statut_property(self):
        """
        Test pm1_statut property
        """
        test_value = int(8)
        self.instance.pm1_statut = test_value
        self.assertEqual(self.instance.pm1_statut, test_value)
    
    def test_pm25_property(self):
        """
        Test pm25 property
        """
        test_value = float(43.62485923221633)
        self.instance.pm25 = test_value
        self.assertEqual(self.instance.pm25, test_value)
    
    def test_pm25_statut_property(self):
        """
        Test pm25_statut property
        """
        test_value = int(94)
        self.instance.pm25_statut = test_value
        self.assertEqual(self.instance.pm25_statut, test_value)
    
    def test_pm4_property(self):
        """
        Test pm4 property
        """
        test_value = float(69.19844505740777)
        self.instance.pm4 = test_value
        self.assertEqual(self.instance.pm4, test_value)
    
    def test_pm4_statut_property(self):
        """
        Test pm4_statut property
        """
        test_value = int(84)
        self.instance.pm4_statut = test_value
        self.assertEqual(self.instance.pm4_statut, test_value)
    
    def test_pm10_property(self):
        """
        Test pm10 property
        """
        test_value = float(82.15620356870048)
        self.instance.pm10 = test_value
        self.assertEqual(self.instance.pm10, test_value)
    
    def test_pm10_statut_property(self):
        """
        Test pm10_statut property
        """
        test_value = int(12)
        self.instance.pm10_statut = test_value
        self.assertEqual(self.instance.pm10_statut, test_value)
    
    def test_vbat_property(self):
        """
        Test vbat property
        """
        test_value = float(66.23211266578703)
        self.instance.vbat = test_value
        self.assertEqual(self.instance.vbat, test_value)
    
    def test_vbat_statut_property(self):
        """
        Test vbat_statut property
        """
        test_value = int(91)
        self.instance.vbat_statut = test_value
        self.assertEqual(self.instance.vbat_statut, test_value)
    
    def test_mwh_bat_property(self):
        """
        Test mwh_bat property
        """
        test_value = float(40.04066080529497)
        self.instance.mwh_bat = test_value
        self.assertEqual(self.instance.mwh_bat, test_value)
    
    def test_mwh_pv_property(self):
        """
        Test mwh_pv property
        """
        test_value = float(95.24381597031412)
        self.instance.mwh_pv = test_value
        self.assertEqual(self.instance.mwh_pv, test_value)
    
    def test_co_rf_property(self):
        """
        Test co_rf property
        """
        test_value = float(95.68347655258395)
        self.instance.co_rf = test_value
        self.assertEqual(self.instance.co_rf, test_value)
    
    def test_no_rf_property(self):
        """
        Test no_rf property
        """
        test_value = float(62.38572091990584)
        self.instance.no_rf = test_value
        self.assertEqual(self.instance.no_rf, test_value)
    
    def test_no2_rf_property(self):
        """
        Test no2_rf property
        """
        test_value = float(76.05566735261662)
        self.instance.no2_rf = test_value
        self.assertEqual(self.instance.no2_rf, test_value)
    
    def test_o3no2_rf_property(self):
        """
        Test o3no2_rf property
        """
        test_value = float(69.69889161695323)
        self.instance.o3no2_rf = test_value
        self.assertEqual(self.instance.o3no2_rf, test_value)
    
    def test_o3_rf_property(self):
        """
        Test o3_rf property
        """
        test_value = float(78.62969919594475)
        self.instance.o3_rf = test_value
        self.assertEqual(self.instance.o3_rf, test_value)
    
    def test_pm10_rf_property(self):
        """
        Test pm10_rf property
        """
        test_value = float(6.339080591731705)
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

