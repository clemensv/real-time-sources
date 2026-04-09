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
            configuration_id='uixfcaqdjfvvnzvewodu',
            moment='jecyjyjwyqohxnjmogtb',
            co=int(52),
            no=int(5),
            no2=int(65),
            o3no2=int(60),
            ppbno=float(79.956649972886),
            ppbno_statut=int(17),
            ppbno2=float(94.11919558876022),
            ppbno2_statut=int(85),
            ppbo3=float(21.33356605375295),
            ppbo3_statut=int(53),
            ugpcmno=float(74.21210206407693),
            ugpcmno_statut=int(27),
            ugpcmno2=float(88.2004557205468),
            ugpcmno2_statut=int(31),
            ugpcmo3=float(88.63340488577101),
            ugpcmo3_statut=int(97),
            bme_t=float(97.46304059040543),
            bme_t_statut=int(92),
            bme_pres=int(36),
            bme_pres_statut=int(90),
            bme_rh=float(36.52698266088264),
            bme_rh_statut=int(30),
            pm1=float(58.18220156117552),
            pm1_statut=int(93),
            pm25=float(41.0223060292734),
            pm25_statut=int(100),
            pm4=float(58.53989368581607),
            pm4_statut=int(59),
            pm10=float(78.17333809168763),
            pm10_statut=int(10),
            vbat=float(92.70115078855189),
            vbat_statut=int(36),
            mwh_bat=float(81.17658722022883),
            mwh_pv=float(61.01358538438968),
            co_rf=float(21.88846915003254),
            no_rf=float(2.7808634804511345),
            no2_rf=float(6.979188514044099),
            o3no2_rf=float(88.0150221249027),
            o3_rf=float(82.8859582386486),
            pm10_rf=float(80.89091760373559)
        )
        return instance

    
    def test_configuration_id_property(self):
        """
        Test configuration_id property
        """
        test_value = 'uixfcaqdjfvvnzvewodu'
        self.instance.configuration_id = test_value
        self.assertEqual(self.instance.configuration_id, test_value)
    
    def test_moment_property(self):
        """
        Test moment property
        """
        test_value = 'jecyjyjwyqohxnjmogtb'
        self.instance.moment = test_value
        self.assertEqual(self.instance.moment, test_value)
    
    def test_co_property(self):
        """
        Test co property
        """
        test_value = int(52)
        self.instance.co = test_value
        self.assertEqual(self.instance.co, test_value)
    
    def test_no_property(self):
        """
        Test no property
        """
        test_value = int(5)
        self.instance.no = test_value
        self.assertEqual(self.instance.no, test_value)
    
    def test_no2_property(self):
        """
        Test no2 property
        """
        test_value = int(65)
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
        test_value = float(79.956649972886)
        self.instance.ppbno = test_value
        self.assertEqual(self.instance.ppbno, test_value)
    
    def test_ppbno_statut_property(self):
        """
        Test ppbno_statut property
        """
        test_value = int(17)
        self.instance.ppbno_statut = test_value
        self.assertEqual(self.instance.ppbno_statut, test_value)
    
    def test_ppbno2_property(self):
        """
        Test ppbno2 property
        """
        test_value = float(94.11919558876022)
        self.instance.ppbno2 = test_value
        self.assertEqual(self.instance.ppbno2, test_value)
    
    def test_ppbno2_statut_property(self):
        """
        Test ppbno2_statut property
        """
        test_value = int(85)
        self.instance.ppbno2_statut = test_value
        self.assertEqual(self.instance.ppbno2_statut, test_value)
    
    def test_ppbo3_property(self):
        """
        Test ppbo3 property
        """
        test_value = float(21.33356605375295)
        self.instance.ppbo3 = test_value
        self.assertEqual(self.instance.ppbo3, test_value)
    
    def test_ppbo3_statut_property(self):
        """
        Test ppbo3_statut property
        """
        test_value = int(53)
        self.instance.ppbo3_statut = test_value
        self.assertEqual(self.instance.ppbo3_statut, test_value)
    
    def test_ugpcmno_property(self):
        """
        Test ugpcmno property
        """
        test_value = float(74.21210206407693)
        self.instance.ugpcmno = test_value
        self.assertEqual(self.instance.ugpcmno, test_value)
    
    def test_ugpcmno_statut_property(self):
        """
        Test ugpcmno_statut property
        """
        test_value = int(27)
        self.instance.ugpcmno_statut = test_value
        self.assertEqual(self.instance.ugpcmno_statut, test_value)
    
    def test_ugpcmno2_property(self):
        """
        Test ugpcmno2 property
        """
        test_value = float(88.2004557205468)
        self.instance.ugpcmno2 = test_value
        self.assertEqual(self.instance.ugpcmno2, test_value)
    
    def test_ugpcmno2_statut_property(self):
        """
        Test ugpcmno2_statut property
        """
        test_value = int(31)
        self.instance.ugpcmno2_statut = test_value
        self.assertEqual(self.instance.ugpcmno2_statut, test_value)
    
    def test_ugpcmo3_property(self):
        """
        Test ugpcmo3 property
        """
        test_value = float(88.63340488577101)
        self.instance.ugpcmo3 = test_value
        self.assertEqual(self.instance.ugpcmo3, test_value)
    
    def test_ugpcmo3_statut_property(self):
        """
        Test ugpcmo3_statut property
        """
        test_value = int(97)
        self.instance.ugpcmo3_statut = test_value
        self.assertEqual(self.instance.ugpcmo3_statut, test_value)
    
    def test_bme_t_property(self):
        """
        Test bme_t property
        """
        test_value = float(97.46304059040543)
        self.instance.bme_t = test_value
        self.assertEqual(self.instance.bme_t, test_value)
    
    def test_bme_t_statut_property(self):
        """
        Test bme_t_statut property
        """
        test_value = int(92)
        self.instance.bme_t_statut = test_value
        self.assertEqual(self.instance.bme_t_statut, test_value)
    
    def test_bme_pres_property(self):
        """
        Test bme_pres property
        """
        test_value = int(36)
        self.instance.bme_pres = test_value
        self.assertEqual(self.instance.bme_pres, test_value)
    
    def test_bme_pres_statut_property(self):
        """
        Test bme_pres_statut property
        """
        test_value = int(90)
        self.instance.bme_pres_statut = test_value
        self.assertEqual(self.instance.bme_pres_statut, test_value)
    
    def test_bme_rh_property(self):
        """
        Test bme_rh property
        """
        test_value = float(36.52698266088264)
        self.instance.bme_rh = test_value
        self.assertEqual(self.instance.bme_rh, test_value)
    
    def test_bme_rh_statut_property(self):
        """
        Test bme_rh_statut property
        """
        test_value = int(30)
        self.instance.bme_rh_statut = test_value
        self.assertEqual(self.instance.bme_rh_statut, test_value)
    
    def test_pm1_property(self):
        """
        Test pm1 property
        """
        test_value = float(58.18220156117552)
        self.instance.pm1 = test_value
        self.assertEqual(self.instance.pm1, test_value)
    
    def test_pm1_statut_property(self):
        """
        Test pm1_statut property
        """
        test_value = int(93)
        self.instance.pm1_statut = test_value
        self.assertEqual(self.instance.pm1_statut, test_value)
    
    def test_pm25_property(self):
        """
        Test pm25 property
        """
        test_value = float(41.0223060292734)
        self.instance.pm25 = test_value
        self.assertEqual(self.instance.pm25, test_value)
    
    def test_pm25_statut_property(self):
        """
        Test pm25_statut property
        """
        test_value = int(100)
        self.instance.pm25_statut = test_value
        self.assertEqual(self.instance.pm25_statut, test_value)
    
    def test_pm4_property(self):
        """
        Test pm4 property
        """
        test_value = float(58.53989368581607)
        self.instance.pm4 = test_value
        self.assertEqual(self.instance.pm4, test_value)
    
    def test_pm4_statut_property(self):
        """
        Test pm4_statut property
        """
        test_value = int(59)
        self.instance.pm4_statut = test_value
        self.assertEqual(self.instance.pm4_statut, test_value)
    
    def test_pm10_property(self):
        """
        Test pm10 property
        """
        test_value = float(78.17333809168763)
        self.instance.pm10 = test_value
        self.assertEqual(self.instance.pm10, test_value)
    
    def test_pm10_statut_property(self):
        """
        Test pm10_statut property
        """
        test_value = int(10)
        self.instance.pm10_statut = test_value
        self.assertEqual(self.instance.pm10_statut, test_value)
    
    def test_vbat_property(self):
        """
        Test vbat property
        """
        test_value = float(92.70115078855189)
        self.instance.vbat = test_value
        self.assertEqual(self.instance.vbat, test_value)
    
    def test_vbat_statut_property(self):
        """
        Test vbat_statut property
        """
        test_value = int(36)
        self.instance.vbat_statut = test_value
        self.assertEqual(self.instance.vbat_statut, test_value)
    
    def test_mwh_bat_property(self):
        """
        Test mwh_bat property
        """
        test_value = float(81.17658722022883)
        self.instance.mwh_bat = test_value
        self.assertEqual(self.instance.mwh_bat, test_value)
    
    def test_mwh_pv_property(self):
        """
        Test mwh_pv property
        """
        test_value = float(61.01358538438968)
        self.instance.mwh_pv = test_value
        self.assertEqual(self.instance.mwh_pv, test_value)
    
    def test_co_rf_property(self):
        """
        Test co_rf property
        """
        test_value = float(21.88846915003254)
        self.instance.co_rf = test_value
        self.assertEqual(self.instance.co_rf, test_value)
    
    def test_no_rf_property(self):
        """
        Test no_rf property
        """
        test_value = float(2.7808634804511345)
        self.instance.no_rf = test_value
        self.assertEqual(self.instance.no_rf, test_value)
    
    def test_no2_rf_property(self):
        """
        Test no2_rf property
        """
        test_value = float(6.979188514044099)
        self.instance.no2_rf = test_value
        self.assertEqual(self.instance.no2_rf, test_value)
    
    def test_o3no2_rf_property(self):
        """
        Test o3no2_rf property
        """
        test_value = float(88.0150221249027)
        self.instance.o3no2_rf = test_value
        self.assertEqual(self.instance.o3no2_rf, test_value)
    
    def test_o3_rf_property(self):
        """
        Test o3_rf property
        """
        test_value = float(82.8859582386486)
        self.instance.o3_rf = test_value
        self.assertEqual(self.instance.o3_rf, test_value)
    
    def test_pm10_rf_property(self):
        """
        Test pm10_rf property
        """
        test_value = float(80.89091760373559)
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

