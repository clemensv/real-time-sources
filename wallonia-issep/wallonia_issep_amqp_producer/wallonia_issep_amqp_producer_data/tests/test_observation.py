"""
Test case for Observation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wallonia_issep_amqp_producer_data.observation import Observation


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
            configuration_id='jboyrjgibvhpcucrbxiv',
            province='xfzzycuoqqgsxytnsffy',
            moment='uearmmbdpkgggausyboq',
            co=int(88),
            no=int(96),
            no2=int(19),
            o3no2=int(27),
            ppbno=float(68.11015627270524),
            ppbno_statut=int(13),
            ppbno2=float(82.4966132691062),
            ppbno2_statut=int(42),
            ppbo3=float(42.22119405879292),
            ppbo3_statut=int(18),
            ugpcmno=float(13.607060329117882),
            ugpcmno_statut=int(50),
            ugpcmno2=float(64.52378591370444),
            ugpcmno2_statut=int(18),
            ugpcmo3=float(4.573586040465772),
            ugpcmo3_statut=int(51),
            bme_t=float(7.21525987558751),
            bme_t_statut=int(58),
            bme_pres=int(18),
            bme_pres_statut=int(99),
            bme_rh=float(85.75691312888698),
            bme_rh_statut=int(26),
            pm1=float(10.94591833136077),
            pm1_statut=int(19),
            pm25=float(34.32853700010811),
            pm25_statut=int(39),
            pm4=float(88.08043400126623),
            pm4_statut=int(6),
            pm10=float(28.8352166071537),
            pm10_statut=int(54),
            vbat=float(39.1216843503582),
            vbat_statut=int(38),
            mwh_bat=float(12.897421188182367),
            mwh_pv=float(30.45573382103386),
            co_rf=float(22.67085114333639),
            no_rf=float(63.308672072244455),
            no2_rf=float(84.19195954592692),
            o3no2_rf=float(62.665319439540845),
            o3_rf=float(83.28246118314038),
            pm10_rf=float(86.58180753101328)
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'jboyrjgibvhpcucrbxiv'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'xfzzycuoqqgsxytnsffy'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_moment_property(self):
        """
        Test moment property
        """
        test_value = 'uearmmbdpkgggausyboq'
        self.instance.moment = test_value
        self.assertEqual(self.instance.moment, test_value)
    
    def test_co_property(self):
        """
        Test co property
        """
        test_value = int(88)
        self.instance.co = test_value
        self.assertEqual(self.instance.co, test_value)
    
    def test_no_property(self):
        """
        Test no property
        """
        test_value = int(96)
        self.instance.no = test_value
        self.assertEqual(self.instance.no, test_value)
    
    def test_no2_property(self):
        """
        Test no2 property
        """
        test_value = int(19)
        self.instance.no2 = test_value
        self.assertEqual(self.instance.no2, test_value)
    
    def test_o3no2_property(self):
        """
        Test o3no2 property
        """
        test_value = int(27)
        self.instance.o3no2 = test_value
        self.assertEqual(self.instance.o3no2, test_value)
    
    def test_ppbno_property(self):
        """
        Test ppbno property
        """
        test_value = float(68.11015627270524)
        self.instance.ppbno = test_value
        self.assertEqual(self.instance.ppbno, test_value)
    
    def test_ppbno_statut_property(self):
        """
        Test ppbno_statut property
        """
        test_value = int(13)
        self.instance.ppbno_statut = test_value
        self.assertEqual(self.instance.ppbno_statut, test_value)
    
    def test_ppbno2_property(self):
        """
        Test ppbno2 property
        """
        test_value = float(82.4966132691062)
        self.instance.ppbno2 = test_value
        self.assertEqual(self.instance.ppbno2, test_value)
    
    def test_ppbno2_statut_property(self):
        """
        Test ppbno2_statut property
        """
        test_value = int(42)
        self.instance.ppbno2_statut = test_value
        self.assertEqual(self.instance.ppbno2_statut, test_value)
    
    def test_ppbo3_property(self):
        """
        Test ppbo3 property
        """
        test_value = float(42.22119405879292)
        self.instance.ppbo3 = test_value
        self.assertEqual(self.instance.ppbo3, test_value)
    
    def test_ppbo3_statut_property(self):
        """
        Test ppbo3_statut property
        """
        test_value = int(18)
        self.instance.ppbo3_statut = test_value
        self.assertEqual(self.instance.ppbo3_statut, test_value)
    
    def test_ugpcmno_property(self):
        """
        Test ugpcmno property
        """
        test_value = float(13.607060329117882)
        self.instance.ugpcmno = test_value
        self.assertEqual(self.instance.ugpcmno, test_value)
    
    def test_ugpcmno_statut_property(self):
        """
        Test ugpcmno_statut property
        """
        test_value = int(50)
        self.instance.ugpcmno_statut = test_value
        self.assertEqual(self.instance.ugpcmno_statut, test_value)
    
    def test_ugpcmno2_property(self):
        """
        Test ugpcmno2 property
        """
        test_value = float(64.52378591370444)
        self.instance.ugpcmno2 = test_value
        self.assertEqual(self.instance.ugpcmno2, test_value)
    
    def test_ugpcmno2_statut_property(self):
        """
        Test ugpcmno2_statut property
        """
        test_value = int(18)
        self.instance.ugpcmno2_statut = test_value
        self.assertEqual(self.instance.ugpcmno2_statut, test_value)
    
    def test_ugpcmo3_property(self):
        """
        Test ugpcmo3 property
        """
        test_value = float(4.573586040465772)
        self.instance.ugpcmo3 = test_value
        self.assertEqual(self.instance.ugpcmo3, test_value)
    
    def test_ugpcmo3_statut_property(self):
        """
        Test ugpcmo3_statut property
        """
        test_value = int(51)
        self.instance.ugpcmo3_statut = test_value
        self.assertEqual(self.instance.ugpcmo3_statut, test_value)
    
    def test_bme_t_property(self):
        """
        Test bme_t property
        """
        test_value = float(7.21525987558751)
        self.instance.bme_t = test_value
        self.assertEqual(self.instance.bme_t, test_value)
    
    def test_bme_t_statut_property(self):
        """
        Test bme_t_statut property
        """
        test_value = int(58)
        self.instance.bme_t_statut = test_value
        self.assertEqual(self.instance.bme_t_statut, test_value)
    
    def test_bme_pres_property(self):
        """
        Test bme_pres property
        """
        test_value = int(18)
        self.instance.bme_pres = test_value
        self.assertEqual(self.instance.bme_pres, test_value)
    
    def test_bme_pres_statut_property(self):
        """
        Test bme_pres_statut property
        """
        test_value = int(99)
        self.instance.bme_pres_statut = test_value
        self.assertEqual(self.instance.bme_pres_statut, test_value)
    
    def test_bme_rh_property(self):
        """
        Test bme_rh property
        """
        test_value = float(85.75691312888698)
        self.instance.bme_rh = test_value
        self.assertEqual(self.instance.bme_rh, test_value)
    
    def test_bme_rh_statut_property(self):
        """
        Test bme_rh_statut property
        """
        test_value = int(26)
        self.instance.bme_rh_statut = test_value
        self.assertEqual(self.instance.bme_rh_statut, test_value)
    
    def test_pm1_property(self):
        """
        Test pm1 property
        """
        test_value = float(10.94591833136077)
        self.instance.pm1 = test_value
        self.assertEqual(self.instance.pm1, test_value)
    
    def test_pm1_statut_property(self):
        """
        Test pm1_statut property
        """
        test_value = int(19)
        self.instance.pm1_statut = test_value
        self.assertEqual(self.instance.pm1_statut, test_value)
    
    def test_pm25_property(self):
        """
        Test pm25 property
        """
        test_value = float(34.32853700010811)
        self.instance.pm25 = test_value
        self.assertEqual(self.instance.pm25, test_value)
    
    def test_pm25_statut_property(self):
        """
        Test pm25_statut property
        """
        test_value = int(39)
        self.instance.pm25_statut = test_value
        self.assertEqual(self.instance.pm25_statut, test_value)
    
    def test_pm4_property(self):
        """
        Test pm4 property
        """
        test_value = float(88.08043400126623)
        self.instance.pm4 = test_value
        self.assertEqual(self.instance.pm4, test_value)
    
    def test_pm4_statut_property(self):
        """
        Test pm4_statut property
        """
        test_value = int(6)
        self.instance.pm4_statut = test_value
        self.assertEqual(self.instance.pm4_statut, test_value)
    
    def test_pm10_property(self):
        """
        Test pm10 property
        """
        test_value = float(28.8352166071537)
        self.instance.pm10 = test_value
        self.assertEqual(self.instance.pm10, test_value)
    
    def test_pm10_statut_property(self):
        """
        Test pm10_statut property
        """
        test_value = int(54)
        self.instance.pm10_statut = test_value
        self.assertEqual(self.instance.pm10_statut, test_value)
    
    def test_vbat_property(self):
        """
        Test vbat property
        """
        test_value = float(39.1216843503582)
        self.instance.vbat = test_value
        self.assertEqual(self.instance.vbat, test_value)
    
    def test_vbat_statut_property(self):
        """
        Test vbat_statut property
        """
        test_value = int(38)
        self.instance.vbat_statut = test_value
        self.assertEqual(self.instance.vbat_statut, test_value)
    
    def test_mwh_bat_property(self):
        """
        Test mwh_bat property
        """
        test_value = float(12.897421188182367)
        self.instance.mwh_bat = test_value
        self.assertEqual(self.instance.mwh_bat, test_value)
    
    def test_mwh_pv_property(self):
        """
        Test mwh_pv property
        """
        test_value = float(30.45573382103386)
        self.instance.mwh_pv = test_value
        self.assertEqual(self.instance.mwh_pv, test_value)
    
    def test_co_rf_property(self):
        """
        Test co_rf property
        """
        test_value = float(22.67085114333639)
        self.instance.co_rf = test_value
        self.assertEqual(self.instance.co_rf, test_value)
    
    def test_no_rf_property(self):
        """
        Test no_rf property
        """
        test_value = float(63.308672072244455)
        self.instance.no_rf = test_value
        self.assertEqual(self.instance.no_rf, test_value)
    
    def test_no2_rf_property(self):
        """
        Test no2_rf property
        """
        test_value = float(84.19195954592692)
        self.instance.no2_rf = test_value
        self.assertEqual(self.instance.no2_rf, test_value)
    
    def test_o3no2_rf_property(self):
        """
        Test o3no2_rf property
        """
        test_value = float(62.665319439540845)
        self.instance.o3no2_rf = test_value
        self.assertEqual(self.instance.o3no2_rf, test_value)
    
    def test_o3_rf_property(self):
        """
        Test o3_rf property
        """
        test_value = float(83.28246118314038)
        self.instance.o3_rf = test_value
        self.assertEqual(self.instance.o3_rf, test_value)
    
    def test_pm10_rf_property(self):
        """
        Test pm10_rf property
        """
        test_value = float(86.58180753101328)
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

