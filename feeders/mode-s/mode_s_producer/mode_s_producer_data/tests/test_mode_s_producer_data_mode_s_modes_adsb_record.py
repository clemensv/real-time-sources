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
            icao='mrbxgxxplfiircoxxmuw',
            df=int(36),
            tc=int(58),
            bcode='taopsnfocwhrxzfbqqxx',
            alt=int(31),
            cs='xapnlteegutkfehadrtf',
            sq='xpyblmiruncfbtcmfckh',
            lat=float(28.840026047183642),
            lon=float(58.19052096576263),
            spd=float(67.35765641282823),
            ang=float(49.933950063730315),
            vr=int(33),
            spd_type='xoycpkeebvgwrxllsauw',
            dir_src='jfcnkbuhdcltxuaukhye',
            vr_src='jeogodhrfngyumgydsik',
            ws=int(97),
            wd=int(53),
            at=float(93.89991067422939),
            ap=float(96.76339786773988),
            hm=float(64.0142721435048),
            roll=float(46.442451022699174),
            trak=float(60.7394976908569),
            gs=float(3.1062373764380258),
            tas=float(83.25603058629343),
            hd=float(71.70552052147983),
            ias=float(92.32979141156184),
            m=float(79.4401280693102),
            vrb=float(37.528840725158005),
            vri=float(86.79150966786084),
            rssi=float(66.61719564397717),
            emst='bumkabdpphrzywognflh',
            tgt='wwmcopzycbyyfbzpnyfb',
            opst='gurqpqiguvtwklctmmko'
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
        test_value = 'mrbxgxxplfiircoxxmuw'
        self.instance.icao = test_value
        self.assertEqual(self.instance.icao, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(36)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(58)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'taopsnfocwhrxzfbqqxx'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(31)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'xapnlteegutkfehadrtf'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'xpyblmiruncfbtcmfckh'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(28.840026047183642)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(58.19052096576263)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(67.35765641282823)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(49.933950063730315)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(33)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_spd_type_property(self):
        """
        Test spd_type property
        """
        test_value = 'xoycpkeebvgwrxllsauw'
        self.instance.spd_type = test_value
        self.assertEqual(self.instance.spd_type, test_value)
    
    def test_dir_src_property(self):
        """
        Test dir_src property
        """
        test_value = 'jfcnkbuhdcltxuaukhye'
        self.instance.dir_src = test_value
        self.assertEqual(self.instance.dir_src, test_value)
    
    def test_vr_src_property(self):
        """
        Test vr_src property
        """
        test_value = 'jeogodhrfngyumgydsik'
        self.instance.vr_src = test_value
        self.assertEqual(self.instance.vr_src, test_value)
    
    def test_ws_property(self):
        """
        Test ws property
        """
        test_value = int(97)
        self.instance.ws = test_value
        self.assertEqual(self.instance.ws, test_value)
    
    def test_wd_property(self):
        """
        Test wd property
        """
        test_value = int(53)
        self.instance.wd = test_value
        self.assertEqual(self.instance.wd, test_value)
    
    def test_at_property(self):
        """
        Test at property
        """
        test_value = float(93.89991067422939)
        self.instance.at = test_value
        self.assertEqual(self.instance.at, test_value)
    
    def test_ap_property(self):
        """
        Test ap property
        """
        test_value = float(96.76339786773988)
        self.instance.ap = test_value
        self.assertEqual(self.instance.ap, test_value)
    
    def test_hm_property(self):
        """
        Test hm property
        """
        test_value = float(64.0142721435048)
        self.instance.hm = test_value
        self.assertEqual(self.instance.hm, test_value)
    
    def test_roll_property(self):
        """
        Test roll property
        """
        test_value = float(46.442451022699174)
        self.instance.roll = test_value
        self.assertEqual(self.instance.roll, test_value)
    
    def test_trak_property(self):
        """
        Test trak property
        """
        test_value = float(60.7394976908569)
        self.instance.trak = test_value
        self.assertEqual(self.instance.trak, test_value)
    
    def test_gs_property(self):
        """
        Test gs property
        """
        test_value = float(3.1062373764380258)
        self.instance.gs = test_value
        self.assertEqual(self.instance.gs, test_value)
    
    def test_tas_property(self):
        """
        Test tas property
        """
        test_value = float(83.25603058629343)
        self.instance.tas = test_value
        self.assertEqual(self.instance.tas, test_value)
    
    def test_hd_property(self):
        """
        Test hd property
        """
        test_value = float(71.70552052147983)
        self.instance.hd = test_value
        self.assertEqual(self.instance.hd, test_value)
    
    def test_ias_property(self):
        """
        Test ias property
        """
        test_value = float(92.32979141156184)
        self.instance.ias = test_value
        self.assertEqual(self.instance.ias, test_value)
    
    def test_m_property(self):
        """
        Test m property
        """
        test_value = float(79.4401280693102)
        self.instance.m = test_value
        self.assertEqual(self.instance.m, test_value)
    
    def test_vrb_property(self):
        """
        Test vrb property
        """
        test_value = float(37.528840725158005)
        self.instance.vrb = test_value
        self.assertEqual(self.instance.vrb, test_value)
    
    def test_vri_property(self):
        """
        Test vri property
        """
        test_value = float(86.79150966786084)
        self.instance.vri = test_value
        self.assertEqual(self.instance.vri, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(66.61719564397717)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_emst_property(self):
        """
        Test emst property
        """
        test_value = 'bumkabdpphrzywognflh'
        self.instance.emst = test_value
        self.assertEqual(self.instance.emst, test_value)
    
    def test_tgt_property(self):
        """
        Test tgt property
        """
        test_value = 'wwmcopzycbyyfbzpnyfb'
        self.instance.tgt = test_value
        self.assertEqual(self.instance.tgt, test_value)
    
    def test_opst_property(self):
        """
        Test opst property
        """
        test_value = 'gurqpqiguvtwklctmmko'
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
