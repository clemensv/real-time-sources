"""
Test case for ModeS_ADSB_Record
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from mode_s_producer_data.mode_s.modes_adsb_record import ModeS_ADSB_Record
import datetime


class Test_ModeS_ADSB_Record(unittest.TestCase):
    """
    Test case for ModeS_ADSB_Record
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ModeS_ADSB_Record.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ModeS_ADSB_Record for testing
        """
        instance = ModeS_ADSB_Record(
            ts=datetime.datetime.now(datetime.timezone.utc),
            icao='zlztxaaqochegbffzqgg',
            df=int(89),
            tc=int(43),
            bcode='mnonugupqcnhqrtzvxym',
            alt=int(38),
            cs='mgckkyfgweotrvoaucek',
            sq='cmqowbsbgolblasfuztw',
            lat=float(59.80068139835269),
            lon=float(90.69177834880803),
            spd=float(21.03358238939461),
            ang=float(32.37406585871273),
            vr=int(14),
            spd_type='ekbcyumwbmapagaqswin',
            dir_src='twzdlmxzeqldmafjqlcu',
            vr_src='wuzfgccbvxoeqpffyhni',
            ws=int(95),
            wd=int(78),
            at=float(86.01691328228745),
            ap=float(14.727706740879952),
            hm=float(9.192367879662445),
            roll=float(73.6874615249422),
            trak=float(75.2291912431659),
            gs=float(66.98818373201738),
            tas=float(95.77046789457498),
            hd=float(29.62614555523999),
            ias=float(16.364399040561473),
            m=float(78.80793215619025),
            vrb=float(81.79692269182215),
            vri=float(73.92618150619205),
            rssi=float(8.728881757053596),
            emst='ofwgvukltvphwstzjrzz',
            tgt='sahemnfdoxmxampstvxy',
            opst='lgwhtkfvfuuctujiqgld'
        )
        return instance

    
    def test_ts_property(self):
        """
        Test ts property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ts = test_value
        self.assertEqual(self.instance.ts, test_value)
    
    def test_icao_property(self):
        """
        Test icao property
        """
        test_value = 'zlztxaaqochegbffzqgg'
        self.instance.icao = test_value
        self.assertEqual(self.instance.icao, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(89)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(43)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'mnonugupqcnhqrtzvxym'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(38)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'mgckkyfgweotrvoaucek'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'cmqowbsbgolblasfuztw'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(59.80068139835269)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(90.69177834880803)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(21.03358238939461)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(32.37406585871273)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(14)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_spd_type_property(self):
        """
        Test spd_type property
        """
        test_value = 'ekbcyumwbmapagaqswin'
        self.instance.spd_type = test_value
        self.assertEqual(self.instance.spd_type, test_value)
    
    def test_dir_src_property(self):
        """
        Test dir_src property
        """
        test_value = 'twzdlmxzeqldmafjqlcu'
        self.instance.dir_src = test_value
        self.assertEqual(self.instance.dir_src, test_value)
    
    def test_vr_src_property(self):
        """
        Test vr_src property
        """
        test_value = 'wuzfgccbvxoeqpffyhni'
        self.instance.vr_src = test_value
        self.assertEqual(self.instance.vr_src, test_value)
    
    def test_ws_property(self):
        """
        Test ws property
        """
        test_value = int(95)
        self.instance.ws = test_value
        self.assertEqual(self.instance.ws, test_value)
    
    def test_wd_property(self):
        """
        Test wd property
        """
        test_value = int(78)
        self.instance.wd = test_value
        self.assertEqual(self.instance.wd, test_value)
    
    def test_at_property(self):
        """
        Test at property
        """
        test_value = float(86.01691328228745)
        self.instance.at = test_value
        self.assertEqual(self.instance.at, test_value)
    
    def test_ap_property(self):
        """
        Test ap property
        """
        test_value = float(14.727706740879952)
        self.instance.ap = test_value
        self.assertEqual(self.instance.ap, test_value)
    
    def test_hm_property(self):
        """
        Test hm property
        """
        test_value = float(9.192367879662445)
        self.instance.hm = test_value
        self.assertEqual(self.instance.hm, test_value)
    
    def test_roll_property(self):
        """
        Test roll property
        """
        test_value = float(73.6874615249422)
        self.instance.roll = test_value
        self.assertEqual(self.instance.roll, test_value)
    
    def test_trak_property(self):
        """
        Test trak property
        """
        test_value = float(75.2291912431659)
        self.instance.trak = test_value
        self.assertEqual(self.instance.trak, test_value)
    
    def test_gs_property(self):
        """
        Test gs property
        """
        test_value = float(66.98818373201738)
        self.instance.gs = test_value
        self.assertEqual(self.instance.gs, test_value)
    
    def test_tas_property(self):
        """
        Test tas property
        """
        test_value = float(95.77046789457498)
        self.instance.tas = test_value
        self.assertEqual(self.instance.tas, test_value)
    
    def test_hd_property(self):
        """
        Test hd property
        """
        test_value = float(29.62614555523999)
        self.instance.hd = test_value
        self.assertEqual(self.instance.hd, test_value)
    
    def test_ias_property(self):
        """
        Test ias property
        """
        test_value = float(16.364399040561473)
        self.instance.ias = test_value
        self.assertEqual(self.instance.ias, test_value)
    
    def test_m_property(self):
        """
        Test m property
        """
        test_value = float(78.80793215619025)
        self.instance.m = test_value
        self.assertEqual(self.instance.m, test_value)
    
    def test_vrb_property(self):
        """
        Test vrb property
        """
        test_value = float(81.79692269182215)
        self.instance.vrb = test_value
        self.assertEqual(self.instance.vrb, test_value)
    
    def test_vri_property(self):
        """
        Test vri property
        """
        test_value = float(73.92618150619205)
        self.instance.vri = test_value
        self.assertEqual(self.instance.vri, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(8.728881757053596)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_emst_property(self):
        """
        Test emst property
        """
        test_value = 'ofwgvukltvphwstzjrzz'
        self.instance.emst = test_value
        self.assertEqual(self.instance.emst, test_value)
    
    def test_tgt_property(self):
        """
        Test tgt property
        """
        test_value = 'sahemnfdoxmxampstvxy'
        self.instance.tgt = test_value
        self.assertEqual(self.instance.tgt, test_value)
    
    def test_opst_property(self):
        """
        Test opst property
        """
        test_value = 'lgwhtkfvfuuctujiqgld'
        self.instance.opst = test_value
        self.assertEqual(self.instance.opst, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ModeS_ADSB_Record.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
