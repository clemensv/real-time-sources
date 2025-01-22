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
            icao='ualloqojcjxxahgipglc',
            df=int(50),
            tc=int(83),
            bcode='trvcsqwbzaevskiimvzp',
            alt=int(52),
            cs='jbckopjblvwjkoidefiy',
            sq='zqgayexsakhfuwwhzpck',
            lat=float(59.85950253605944),
            lon=float(69.54292603747979),
            spd=float(45.22880357814202),
            ang=float(41.417231162681624),
            vr=int(52),
            spd_type='phahixzeqyjmhqscpjkd',
            dir_src='ssijffegdcjlwnybsgpf',
            vr_src='irqjybnbpumivgdjwjiq',
            ws=int(67),
            wd=int(57),
            at=float(87.27271301832519),
            ap=float(37.93267772685767),
            hm=float(93.29060596902333),
            roll=float(88.21794125210991),
            trak=float(46.82196543316539),
            gs=float(50.99828950000139),
            tas=float(73.9575807598525),
            hd=float(40.542519650635676),
            ias=float(69.42199086379742),
            m=float(84.97268860320615),
            vrb=float(52.48348129055833),
            vri=float(27.43557472880578),
            rssi=float(90.57240207951655),
            emst='lhfzwgndhvlrmyeejhqe',
            tgt='cmyfslxjplcrquuiwbvj',
            opst='ydgpdjsgxtzydthcpmsc'
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
        test_value = 'ualloqojcjxxahgipglc'
        self.instance.icao = test_value
        self.assertEqual(self.instance.icao, test_value)
    
    def test_df_property(self):
        """
        Test df property
        """
        test_value = int(50)
        self.instance.df = test_value
        self.assertEqual(self.instance.df, test_value)
    
    def test_tc_property(self):
        """
        Test tc property
        """
        test_value = int(83)
        self.instance.tc = test_value
        self.assertEqual(self.instance.tc, test_value)
    
    def test_bcode_property(self):
        """
        Test bcode property
        """
        test_value = 'trvcsqwbzaevskiimvzp'
        self.instance.bcode = test_value
        self.assertEqual(self.instance.bcode, test_value)
    
    def test_alt_property(self):
        """
        Test alt property
        """
        test_value = int(52)
        self.instance.alt = test_value
        self.assertEqual(self.instance.alt, test_value)
    
    def test_cs_property(self):
        """
        Test cs property
        """
        test_value = 'jbckopjblvwjkoidefiy'
        self.instance.cs = test_value
        self.assertEqual(self.instance.cs, test_value)
    
    def test_sq_property(self):
        """
        Test sq property
        """
        test_value = 'zqgayexsakhfuwwhzpck'
        self.instance.sq = test_value
        self.assertEqual(self.instance.sq, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(59.85950253605944)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lon_property(self):
        """
        Test lon property
        """
        test_value = float(69.54292603747979)
        self.instance.lon = test_value
        self.assertEqual(self.instance.lon, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(45.22880357814202)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_ang_property(self):
        """
        Test ang property
        """
        test_value = float(41.417231162681624)
        self.instance.ang = test_value
        self.assertEqual(self.instance.ang, test_value)
    
    def test_vr_property(self):
        """
        Test vr property
        """
        test_value = int(52)
        self.instance.vr = test_value
        self.assertEqual(self.instance.vr, test_value)
    
    def test_spd_type_property(self):
        """
        Test spd_type property
        """
        test_value = 'phahixzeqyjmhqscpjkd'
        self.instance.spd_type = test_value
        self.assertEqual(self.instance.spd_type, test_value)
    
    def test_dir_src_property(self):
        """
        Test dir_src property
        """
        test_value = 'ssijffegdcjlwnybsgpf'
        self.instance.dir_src = test_value
        self.assertEqual(self.instance.dir_src, test_value)
    
    def test_vr_src_property(self):
        """
        Test vr_src property
        """
        test_value = 'irqjybnbpumivgdjwjiq'
        self.instance.vr_src = test_value
        self.assertEqual(self.instance.vr_src, test_value)
    
    def test_ws_property(self):
        """
        Test ws property
        """
        test_value = int(67)
        self.instance.ws = test_value
        self.assertEqual(self.instance.ws, test_value)
    
    def test_wd_property(self):
        """
        Test wd property
        """
        test_value = int(57)
        self.instance.wd = test_value
        self.assertEqual(self.instance.wd, test_value)
    
    def test_at_property(self):
        """
        Test at property
        """
        test_value = float(87.27271301832519)
        self.instance.at = test_value
        self.assertEqual(self.instance.at, test_value)
    
    def test_ap_property(self):
        """
        Test ap property
        """
        test_value = float(37.93267772685767)
        self.instance.ap = test_value
        self.assertEqual(self.instance.ap, test_value)
    
    def test_hm_property(self):
        """
        Test hm property
        """
        test_value = float(93.29060596902333)
        self.instance.hm = test_value
        self.assertEqual(self.instance.hm, test_value)
    
    def test_roll_property(self):
        """
        Test roll property
        """
        test_value = float(88.21794125210991)
        self.instance.roll = test_value
        self.assertEqual(self.instance.roll, test_value)
    
    def test_trak_property(self):
        """
        Test trak property
        """
        test_value = float(46.82196543316539)
        self.instance.trak = test_value
        self.assertEqual(self.instance.trak, test_value)
    
    def test_gs_property(self):
        """
        Test gs property
        """
        test_value = float(50.99828950000139)
        self.instance.gs = test_value
        self.assertEqual(self.instance.gs, test_value)
    
    def test_tas_property(self):
        """
        Test tas property
        """
        test_value = float(73.9575807598525)
        self.instance.tas = test_value
        self.assertEqual(self.instance.tas, test_value)
    
    def test_hd_property(self):
        """
        Test hd property
        """
        test_value = float(40.542519650635676)
        self.instance.hd = test_value
        self.assertEqual(self.instance.hd, test_value)
    
    def test_ias_property(self):
        """
        Test ias property
        """
        test_value = float(69.42199086379742)
        self.instance.ias = test_value
        self.assertEqual(self.instance.ias, test_value)
    
    def test_m_property(self):
        """
        Test m property
        """
        test_value = float(84.97268860320615)
        self.instance.m = test_value
        self.assertEqual(self.instance.m, test_value)
    
    def test_vrb_property(self):
        """
        Test vrb property
        """
        test_value = float(52.48348129055833)
        self.instance.vrb = test_value
        self.assertEqual(self.instance.vrb, test_value)
    
    def test_vri_property(self):
        """
        Test vri property
        """
        test_value = float(27.43557472880578)
        self.instance.vri = test_value
        self.assertEqual(self.instance.vri, test_value)
    
    def test_rssi_property(self):
        """
        Test rssi property
        """
        test_value = float(90.57240207951655)
        self.instance.rssi = test_value
        self.assertEqual(self.instance.rssi, test_value)
    
    def test_emst_property(self):
        """
        Test emst property
        """
        test_value = 'lhfzwgndhvlrmyeejhqe'
        self.instance.emst = test_value
        self.assertEqual(self.instance.emst, test_value)
    
    def test_tgt_property(self):
        """
        Test tgt property
        """
        test_value = 'cmyfslxjplcrquuiwbvj'
        self.instance.tgt = test_value
        self.assertEqual(self.instance.tgt, test_value)
    
    def test_opst_property(self):
        """
        Test opst property
        """
        test_value = 'ydgpdjsgxtzydthcpmsc'
        self.instance.opst = test_value
        self.assertEqual(self.instance.opst, test_value)
    
