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
            agency_cd='bnikzbmrrucuwlcnvdfh',
            site_no='ahenyclyuxrmsvnvvxyu',
            station_nm='ezmecebspwuuiwymklry',
            site_tp_cd='eumjqhiwfaldzspfamha',
            lat_va='lcjfdjfuqbqrwuwfxnvn',
            long_va='qzqqyeyxtgarnjlnejqf',
            dec_lat_va=float(52.72224029804974),
            dec_long_va=float(56.66026589831653),
            coord_meth_cd='aequdbzpsgfzlmkkssga',
            coord_acy_cd='odgdufyskdqjplpmwjrl',
            coord_datum_cd='srwneutaknlmlseugbsz',
            dec_coord_datum_cd='tssgmdvdkdbqubwvqlsy',
            district_cd='dhstamwyzxcvnqtfygfk',
            state_cd='oylufulxwqzpjrwqwngv',
            county_cd='dvofpggmnyflryojpjms',
            country_cd='kanxqqidnxzujncknttz',
            land_net_ds='uaflokxinboyorzecqkv',
            map_nm='tlyokahgcmsswgpvmkhj',
            map_scale_fc=float(97.24361942481295),
            alt_va=float(47.26860728532586),
            alt_meth_cd='kggvdfwgrmojpyqxbhxf',
            alt_acy_va=float(9.09118401226342),
            alt_datum_cd='cokbuhrzldybgurcyvbd',
            huc_cd='emntgewdssxsusxrjack',
            basin_cd='yggskmysbgiomyxpfwoe',
            topo_cd='koqftejbovztakeuibxd',
            instruments_cd='hakfdhpabvcdwnoqdecf',
            construction_dt='puiyoviqoiptjbpbyhou',
            inventory_dt='qtrirmzoghroxfffawak',
            drain_area_va=float(41.160854767068955),
            contrib_drain_area_va=float(32.99894168613717),
            tz_cd='ggsewraqedfyawbafhdr',
            local_time_fg=True,
            reliability_cd='rwzcbdsvqzdfzimuhsdj',
            gw_file_cd='hictkcxhudiswedgckgi',
            nat_aqfr_cd='qjeyxpfmphngrqkgaxtx',
            aqfr_cd='jarsdhmgddkzsyhzsqlb',
            aqfr_type_cd='fixhtfmkqscntnipcrms',
            well_depth_va=float(65.9045005164135),
            hole_depth_va=float(81.03092969135828),
            depth_src_cd='vrrlcqqxxnblcibxwisi',
            project_no='aotlvfpayvcfvzzjvrwf'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'bnikzbmrrucuwlcnvdfh'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'ahenyclyuxrmsvnvvxyu'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'ezmecebspwuuiwymklry'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'eumjqhiwfaldzspfamha'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_lat_va_property(self):
        """
        Test lat_va property
        """
        test_value = 'lcjfdjfuqbqrwuwfxnvn'
        self.instance.lat_va = test_value
        self.assertEqual(self.instance.lat_va, test_value)
    
    def test_long_va_property(self):
        """
        Test long_va property
        """
        test_value = 'qzqqyeyxtgarnjlnejqf'
        self.instance.long_va = test_value
        self.assertEqual(self.instance.long_va, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(52.72224029804974)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(56.66026589831653)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_meth_cd_property(self):
        """
        Test coord_meth_cd property
        """
        test_value = 'aequdbzpsgfzlmkkssga'
        self.instance.coord_meth_cd = test_value
        self.assertEqual(self.instance.coord_meth_cd, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'odgdufyskdqjplpmwjrl'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_coord_datum_cd_property(self):
        """
        Test coord_datum_cd property
        """
        test_value = 'srwneutaknlmlseugbsz'
        self.instance.coord_datum_cd = test_value
        self.assertEqual(self.instance.coord_datum_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'tssgmdvdkdbqubwvqlsy'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_district_cd_property(self):
        """
        Test district_cd property
        """
        test_value = 'dhstamwyzxcvnqtfygfk'
        self.instance.district_cd = test_value
        self.assertEqual(self.instance.district_cd, test_value)
    
    def test_state_cd_property(self):
        """
        Test state_cd property
        """
        test_value = 'oylufulxwqzpjrwqwngv'
        self.instance.state_cd = test_value
        self.assertEqual(self.instance.state_cd, test_value)
    
    def test_county_cd_property(self):
        """
        Test county_cd property
        """
        test_value = 'dvofpggmnyflryojpjms'
        self.instance.county_cd = test_value
        self.assertEqual(self.instance.county_cd, test_value)
    
    def test_country_cd_property(self):
        """
        Test country_cd property
        """
        test_value = 'kanxqqidnxzujncknttz'
        self.instance.country_cd = test_value
        self.assertEqual(self.instance.country_cd, test_value)
    
    def test_land_net_ds_property(self):
        """
        Test land_net_ds property
        """
        test_value = 'uaflokxinboyorzecqkv'
        self.instance.land_net_ds = test_value
        self.assertEqual(self.instance.land_net_ds, test_value)
    
    def test_map_nm_property(self):
        """
        Test map_nm property
        """
        test_value = 'tlyokahgcmsswgpvmkhj'
        self.instance.map_nm = test_value
        self.assertEqual(self.instance.map_nm, test_value)
    
    def test_map_scale_fc_property(self):
        """
        Test map_scale_fc property
        """
        test_value = float(97.24361942481295)
        self.instance.map_scale_fc = test_value
        self.assertEqual(self.instance.map_scale_fc, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(47.26860728532586)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_meth_cd_property(self):
        """
        Test alt_meth_cd property
        """
        test_value = 'kggvdfwgrmojpyqxbhxf'
        self.instance.alt_meth_cd = test_value
        self.assertEqual(self.instance.alt_meth_cd, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(9.09118401226342)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'cokbuhrzldybgurcyvbd'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
    def test_huc_cd_property(self):
        """
        Test huc_cd property
        """
        test_value = 'emntgewdssxsusxrjack'
        self.instance.huc_cd = test_value
        self.assertEqual(self.instance.huc_cd, test_value)
    
    def test_basin_cd_property(self):
        """
        Test basin_cd property
        """
        test_value = 'yggskmysbgiomyxpfwoe'
        self.instance.basin_cd = test_value
        self.assertEqual(self.instance.basin_cd, test_value)
    
    def test_topo_cd_property(self):
        """
        Test topo_cd property
        """
        test_value = 'koqftejbovztakeuibxd'
        self.instance.topo_cd = test_value
        self.assertEqual(self.instance.topo_cd, test_value)
    
    def test_instruments_cd_property(self):
        """
        Test instruments_cd property
        """
        test_value = 'hakfdhpabvcdwnoqdecf'
        self.instance.instruments_cd = test_value
        self.assertEqual(self.instance.instruments_cd, test_value)
    
    def test_construction_dt_property(self):
        """
        Test construction_dt property
        """
        test_value = 'puiyoviqoiptjbpbyhou'
        self.instance.construction_dt = test_value
        self.assertEqual(self.instance.construction_dt, test_value)
    
    def test_inventory_dt_property(self):
        """
        Test inventory_dt property
        """
        test_value = 'qtrirmzoghroxfffawak'
        self.instance.inventory_dt = test_value
        self.assertEqual(self.instance.inventory_dt, test_value)
    
    def test_drain_area_va_property(self):
        """
        Test drain_area_va property
        """
        test_value = float(41.160854767068955)
        self.instance.drain_area_va = test_value
        self.assertEqual(self.instance.drain_area_va, test_value)
    
    def test_contrib_drain_area_va_property(self):
        """
        Test contrib_drain_area_va property
        """
        test_value = float(32.99894168613717)
        self.instance.contrib_drain_area_va = test_value
        self.assertEqual(self.instance.contrib_drain_area_va, test_value)
    
    def test_tz_cd_property(self):
        """
        Test tz_cd property
        """
        test_value = 'ggsewraqedfyawbafhdr'
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
        test_value = 'rwzcbdsvqzdfzimuhsdj'
        self.instance.reliability_cd = test_value
        self.assertEqual(self.instance.reliability_cd, test_value)
    
    def test_gw_file_cd_property(self):
        """
        Test gw_file_cd property
        """
        test_value = 'hictkcxhudiswedgckgi'
        self.instance.gw_file_cd = test_value
        self.assertEqual(self.instance.gw_file_cd, test_value)
    
    def test_nat_aqfr_cd_property(self):
        """
        Test nat_aqfr_cd property
        """
        test_value = 'qjeyxpfmphngrqkgaxtx'
        self.instance.nat_aqfr_cd = test_value
        self.assertEqual(self.instance.nat_aqfr_cd, test_value)
    
    def test_aqfr_cd_property(self):
        """
        Test aqfr_cd property
        """
        test_value = 'jarsdhmgddkzsyhzsqlb'
        self.instance.aqfr_cd = test_value
        self.assertEqual(self.instance.aqfr_cd, test_value)
    
    def test_aqfr_type_cd_property(self):
        """
        Test aqfr_type_cd property
        """
        test_value = 'fixhtfmkqscntnipcrms'
        self.instance.aqfr_type_cd = test_value
        self.assertEqual(self.instance.aqfr_type_cd, test_value)
    
    def test_well_depth_va_property(self):
        """
        Test well_depth_va property
        """
        test_value = float(65.9045005164135)
        self.instance.well_depth_va = test_value
        self.assertEqual(self.instance.well_depth_va, test_value)
    
    def test_hole_depth_va_property(self):
        """
        Test hole_depth_va property
        """
        test_value = float(81.03092969135828)
        self.instance.hole_depth_va = test_value
        self.assertEqual(self.instance.hole_depth_va, test_value)
    
    def test_depth_src_cd_property(self):
        """
        Test depth_src_cd property
        """
        test_value = 'vrrlcqqxxnblcibxwisi'
        self.instance.depth_src_cd = test_value
        self.assertEqual(self.instance.depth_src_cd, test_value)
    
    def test_project_no_property(self):
        """
        Test project_no property
        """
        test_value = 'aotlvfpayvcfvzzjvrwf'
        self.instance.project_no = test_value
        self.assertEqual(self.instance.project_no, test_value)
    
