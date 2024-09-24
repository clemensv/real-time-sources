"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_producer_data.usgs.sites.site import Site


class Test_Site(unittest.TestCase):
    """
    Test case for Site
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Site.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Site for testing
        """
        instance = Site(
            agency_cd='doodnkhozgaowkzygdah',
            site_no='czvdtwgvxmmqzktpavfu',
            station_nm='kebjdpfdgkbpxwhimyji',
            site_tp_cd='ukoricbpagjvwpfymwjb',
            lat_va='yddexvgosxkolqbbtzyo',
            long_va='fkhjbncengjpgpdarqty',
            dec_lat_va=float(75.48892510817686),
            dec_long_va=float(32.2945351691715),
            coord_meth_cd='vlzlgtftkpoazvnaorfm',
            coord_acy_cd='tkijogwugapdwrygyyas',
            coord_datum_cd='ndnqletanacusbqqfpby',
            dec_coord_datum_cd='omxfsufdpdfrtgamoijl',
            district_cd='xyqellkrnhaewyldocho',
            state_cd='qyspeyvbqdotiluxjpaa',
            county_cd='qdrcsdoxhmeupscbvqnc',
            country_cd='dhrwirpmncbbrzdjddrd',
            land_net_ds='otqggxsakudffzbygqeg',
            map_nm='bvenpdzipinhkwowokoh',
            map_scale_fc=float(75.40491733484674),
            alt_va=float(68.49497823542961),
            alt_meth_cd='nyiowptaldkhctzhvllw',
            alt_acy_va=float(32.919969362106016),
            alt_datum_cd='wjfimmhrcxtqgkuyhzfa',
            huc_cd='mhhqrafeqgnohrcgoyrt',
            basin_cd='cyyzsvyhituoyymcaqnz',
            topo_cd='guibxpeiryvifiqgtkod',
            instruments_cd='imzrdsvthjnazqksnnnc',
            construction_dt='vsoxfmbdmpihfatflmvh',
            inventory_dt='cprncruuscvdtjdgbbfw',
            drain_area_va=float(6.385917742731895),
            contrib_drain_area_va=float(59.60263424090929),
            tz_cd='sjczvvpacqolzudahptf',
            local_time_fg=True,
            reliability_cd='eaxoqdxmcvtblyqdlwlr',
            gw_file_cd='zxwbdiuylbbiiegyifpe',
            nat_aqfr_cd='mwwmfomsakbhrpvrtajy',
            aqfr_cd='toxckkuooirpzogqoqwy',
            aqfr_type_cd='jevjaaukdbqemkvldoum',
            well_depth_va=float(55.695888946234405),
            hole_depth_va=float(61.7720904520213),
            depth_src_cd='rcaendymnxovjddswilr',
            project_no='rzbhvbvpgftlyvknjnxx'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'doodnkhozgaowkzygdah'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'czvdtwgvxmmqzktpavfu'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'kebjdpfdgkbpxwhimyji'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'ukoricbpagjvwpfymwjb'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_lat_va_property(self):
        """
        Test lat_va property
        """
        test_value = 'yddexvgosxkolqbbtzyo'
        self.instance.lat_va = test_value
        self.assertEqual(self.instance.lat_va, test_value)
    
    def test_long_va_property(self):
        """
        Test long_va property
        """
        test_value = 'fkhjbncengjpgpdarqty'
        self.instance.long_va = test_value
        self.assertEqual(self.instance.long_va, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(75.48892510817686)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(32.2945351691715)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_meth_cd_property(self):
        """
        Test coord_meth_cd property
        """
        test_value = 'vlzlgtftkpoazvnaorfm'
        self.instance.coord_meth_cd = test_value
        self.assertEqual(self.instance.coord_meth_cd, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'tkijogwugapdwrygyyas'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_coord_datum_cd_property(self):
        """
        Test coord_datum_cd property
        """
        test_value = 'ndnqletanacusbqqfpby'
        self.instance.coord_datum_cd = test_value
        self.assertEqual(self.instance.coord_datum_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'omxfsufdpdfrtgamoijl'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_district_cd_property(self):
        """
        Test district_cd property
        """
        test_value = 'xyqellkrnhaewyldocho'
        self.instance.district_cd = test_value
        self.assertEqual(self.instance.district_cd, test_value)
    
    def test_state_cd_property(self):
        """
        Test state_cd property
        """
        test_value = 'qyspeyvbqdotiluxjpaa'
        self.instance.state_cd = test_value
        self.assertEqual(self.instance.state_cd, test_value)
    
    def test_county_cd_property(self):
        """
        Test county_cd property
        """
        test_value = 'qdrcsdoxhmeupscbvqnc'
        self.instance.county_cd = test_value
        self.assertEqual(self.instance.county_cd, test_value)
    
    def test_country_cd_property(self):
        """
        Test country_cd property
        """
        test_value = 'dhrwirpmncbbrzdjddrd'
        self.instance.country_cd = test_value
        self.assertEqual(self.instance.country_cd, test_value)
    
    def test_land_net_ds_property(self):
        """
        Test land_net_ds property
        """
        test_value = 'otqggxsakudffzbygqeg'
        self.instance.land_net_ds = test_value
        self.assertEqual(self.instance.land_net_ds, test_value)
    
    def test_map_nm_property(self):
        """
        Test map_nm property
        """
        test_value = 'bvenpdzipinhkwowokoh'
        self.instance.map_nm = test_value
        self.assertEqual(self.instance.map_nm, test_value)
    
    def test_map_scale_fc_property(self):
        """
        Test map_scale_fc property
        """
        test_value = float(75.40491733484674)
        self.instance.map_scale_fc = test_value
        self.assertEqual(self.instance.map_scale_fc, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(68.49497823542961)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_meth_cd_property(self):
        """
        Test alt_meth_cd property
        """
        test_value = 'nyiowptaldkhctzhvllw'
        self.instance.alt_meth_cd = test_value
        self.assertEqual(self.instance.alt_meth_cd, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(32.919969362106016)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'wjfimmhrcxtqgkuyhzfa'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
    def test_huc_cd_property(self):
        """
        Test huc_cd property
        """
        test_value = 'mhhqrafeqgnohrcgoyrt'
        self.instance.huc_cd = test_value
        self.assertEqual(self.instance.huc_cd, test_value)
    
    def test_basin_cd_property(self):
        """
        Test basin_cd property
        """
        test_value = 'cyyzsvyhituoyymcaqnz'
        self.instance.basin_cd = test_value
        self.assertEqual(self.instance.basin_cd, test_value)
    
    def test_topo_cd_property(self):
        """
        Test topo_cd property
        """
        test_value = 'guibxpeiryvifiqgtkod'
        self.instance.topo_cd = test_value
        self.assertEqual(self.instance.topo_cd, test_value)
    
    def test_instruments_cd_property(self):
        """
        Test instruments_cd property
        """
        test_value = 'imzrdsvthjnazqksnnnc'
        self.instance.instruments_cd = test_value
        self.assertEqual(self.instance.instruments_cd, test_value)
    
    def test_construction_dt_property(self):
        """
        Test construction_dt property
        """
        test_value = 'vsoxfmbdmpihfatflmvh'
        self.instance.construction_dt = test_value
        self.assertEqual(self.instance.construction_dt, test_value)
    
    def test_inventory_dt_property(self):
        """
        Test inventory_dt property
        """
        test_value = 'cprncruuscvdtjdgbbfw'
        self.instance.inventory_dt = test_value
        self.assertEqual(self.instance.inventory_dt, test_value)
    
    def test_drain_area_va_property(self):
        """
        Test drain_area_va property
        """
        test_value = float(6.385917742731895)
        self.instance.drain_area_va = test_value
        self.assertEqual(self.instance.drain_area_va, test_value)
    
    def test_contrib_drain_area_va_property(self):
        """
        Test contrib_drain_area_va property
        """
        test_value = float(59.60263424090929)
        self.instance.contrib_drain_area_va = test_value
        self.assertEqual(self.instance.contrib_drain_area_va, test_value)
    
    def test_tz_cd_property(self):
        """
        Test tz_cd property
        """
        test_value = 'sjczvvpacqolzudahptf'
        self.instance.tz_cd = test_value
        self.assertEqual(self.instance.tz_cd, test_value)
    
    def test_local_time_fg_property(self):
        """
        Test local_time_fg property
        """
        test_value = True
        self.instance.local_time_fg = test_value
        self.assertEqual(self.instance.local_time_fg, test_value)
    
    def test_reliability_cd_property(self):
        """
        Test reliability_cd property
        """
        test_value = 'eaxoqdxmcvtblyqdlwlr'
        self.instance.reliability_cd = test_value
        self.assertEqual(self.instance.reliability_cd, test_value)
    
    def test_gw_file_cd_property(self):
        """
        Test gw_file_cd property
        """
        test_value = 'zxwbdiuylbbiiegyifpe'
        self.instance.gw_file_cd = test_value
        self.assertEqual(self.instance.gw_file_cd, test_value)
    
    def test_nat_aqfr_cd_property(self):
        """
        Test nat_aqfr_cd property
        """
        test_value = 'mwwmfomsakbhrpvrtajy'
        self.instance.nat_aqfr_cd = test_value
        self.assertEqual(self.instance.nat_aqfr_cd, test_value)
    
    def test_aqfr_cd_property(self):
        """
        Test aqfr_cd property
        """
        test_value = 'toxckkuooirpzogqoqwy'
        self.instance.aqfr_cd = test_value
        self.assertEqual(self.instance.aqfr_cd, test_value)
    
    def test_aqfr_type_cd_property(self):
        """
        Test aqfr_type_cd property
        """
        test_value = 'jevjaaukdbqemkvldoum'
        self.instance.aqfr_type_cd = test_value
        self.assertEqual(self.instance.aqfr_type_cd, test_value)
    
    def test_well_depth_va_property(self):
        """
        Test well_depth_va property
        """
        test_value = float(55.695888946234405)
        self.instance.well_depth_va = test_value
        self.assertEqual(self.instance.well_depth_va, test_value)
    
    def test_hole_depth_va_property(self):
        """
        Test hole_depth_va property
        """
        test_value = float(61.7720904520213)
        self.instance.hole_depth_va = test_value
        self.assertEqual(self.instance.hole_depth_va, test_value)
    
    def test_depth_src_cd_property(self):
        """
        Test depth_src_cd property
        """
        test_value = 'rcaendymnxovjddswilr'
        self.instance.depth_src_cd = test_value
        self.assertEqual(self.instance.depth_src_cd, test_value)
    
    def test_project_no_property(self):
        """
        Test project_no property
        """
        test_value = 'rzbhvbvpgftlyvknjnxx'
        self.instance.project_no = test_value
        self.assertEqual(self.instance.project_no, test_value)
    
