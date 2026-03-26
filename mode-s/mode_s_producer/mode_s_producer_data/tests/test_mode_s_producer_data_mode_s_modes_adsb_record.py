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
            icao='tzpgqpzgjztpftvksids',
            df=int(78),
            tc=int(6),
            bcode='wgayshfljvykgtmmpqcx',
            alt=int(14),
            cs='dpirbxxpfztoilxokkin',
            sq='yavaghmdelecynosjkwj',
            lat=float(9.885090183715784),
            lon=float(95.25891394898882),
            spd=float(66.76932231068776),
            ang=float(78.11966399037402),
            vr=int(53),
            spd_type='cfvuvlhcmrsrvqmtlgui',
            dir_src='ohfjwyghyqdupuosjyhr',
            vr_src='vnrudgbjocbhtefdfiyy',
            ws=int(39),
            wd=int(33),
            at=float(40.28228632397568),
            ap=float(88.3640127628172),
            hm=float(48.33508641506171),
            roll=float(31.791411521150724),
            trak=float(90.19728566647287),
            gs=float(2.070356956120256),
            tas=float(28.201794834246385),
            hd=float(13.713406021083706),
            ias=float(92.14496948681673),
            m=float(57.85935540229604),
            vrb=float(49.37475634501005),
            vri=float(84.12092997342575),
            rssi=float(70.51307542026105),
            emst='ubpftjakhxgkjavmknmi',
            tgt='fjyjnzswdixiywyrruzw',
            opst='jvfiqdrbhrylbtvfxqjd'
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
        test_value = 'tzpgqpzgjztpftvksids'
        self.instance.icao = test_value
        self.assertEqual(self.instance.icao, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(78)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(6)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'wgayshfljvykgtmmpqcx'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(14)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'dpirbxxpfztoilxokkin'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'yavaghmdelecynosjkwj'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(9.885090183715784)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(95.25891394898882)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(66.76932231068776)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(78.11966399037402)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(53)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_spd_type_property(self):
        """
        Test spd_type property
        """
        test_value = 'cfvuvlhcmrsrvqmtlgui'
        self.instance.spd_type = test_value
        self.assertEqual(self.instance.spd_type, test_value)
    
    def test_dir_src_property(self):
        """
        Test dir_src property
        """
        test_value = 'ohfjwyghyqdupuosjyhr'
        self.instance.dir_src = test_value
        self.assertEqual(self.instance.dir_src, test_value)
    
    def test_vr_src_property(self):
        """
        Test vr_src property
        """
        test_value = 'vnrudgbjocbhtefdfiyy'
        self.instance.vr_src = test_value
        self.assertEqual(self.instance.vr_src, test_value)
    
    def test_ws_property(self):
        """
        Test ws property
        """
        test_value = int(39)
        self.instance.ws = test_value
        self.assertEqual(self.instance.ws, test_value)
    
    def test_wd_property(self):
        """
        Test wd property
        """
        test_value = int(33)
        self.instance.wd = test_value
        self.assertEqual(self.instance.wd, test_value)
    
    def test_at_property(self):
        """
        Test at property
        """
        test_value = float(40.28228632397568)
        self.instance.at = test_value
        self.assertEqual(self.instance.at, test_value)
    
    def test_ap_property(self):
        """
        Test ap property
        """
        test_value = float(88.3640127628172)
        self.instance.ap = test_value
        self.assertEqual(self.instance.ap, test_value)
    
    def test_hm_property(self):
        """
        Test hm property
        """
        test_value = float(48.33508641506171)
        self.instance.hm = test_value
        self.assertEqual(self.instance.hm, test_value)
    
    def test_roll_property(self):
        """
        Test roll property
        """
        test_value = float(31.791411521150724)
        self.instance.roll = test_value
        self.assertEqual(self.instance.roll, test_value)
    
    def test_trak_property(self):
        """
        Test trak property
        """
        test_value = float(90.19728566647287)
        self.instance.trak = test_value
        self.assertEqual(self.instance.trak, test_value)
    
    def test_gs_property(self):
        """
        Test gs property
        """
        test_value = float(2.070356956120256)
        self.instance.gs = test_value
        self.assertEqual(self.instance.gs, test_value)
    
    def test_tas_property(self):
        """
        Test tas property
        """
        test_value = float(28.201794834246385)
        self.instance.tas = test_value
        self.assertEqual(self.instance.tas, test_value)
    
    def test_hd_property(self):
        """
        Test hd property
        """
        test_value = float(13.713406021083706)
        self.instance.hd = test_value
        self.assertEqual(self.instance.hd, test_value)
    
    def test_ias_property(self):
        """
        Test ias property
        """
        test_value = float(92.14496948681673)
        self.instance.ias = test_value
        self.assertEqual(self.instance.ias, test_value)
    
    def test_m_property(self):
        """
        Test m property
        """
        test_value = float(57.85935540229604)
        self.instance.m = test_value
        self.assertEqual(self.instance.m, test_value)
    
    def test_vrb_property(self):
        """
        Test vrb property
        """
        test_value = float(49.37475634501005)
        self.instance.vrb = test_value
        self.assertEqual(self.instance.vrb, test_value)
    
    def test_vri_property(self):
        """
        Test vri property
        """
        test_value = float(84.12092997342575)
        self.instance.vri = test_value
        self.assertEqual(self.instance.vri, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(70.51307542026105)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_emst_property(self):
        """
        Test emst property
        """
        test_value = 'ubpftjakhxgkjavmknmi'
        self.instance.emst = test_value
        self.assertEqual(self.instance.emst, test_value)
    
    def test_tgt_property(self):
        """
        Test tgt property
        """
        test_value = 'fjyjnzswdixiywyrruzw'
        self.instance.tgt = test_value
        self.assertEqual(self.instance.tgt, test_value)
    
    def test_opst_property(self):
        """
        Test opst property
        """
        test_value = 'jvfiqdrbhrylbtvfxqjd'
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
