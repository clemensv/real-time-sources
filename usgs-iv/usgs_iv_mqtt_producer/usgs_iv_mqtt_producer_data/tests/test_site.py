"""
Test case for Site
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_iv_mqtt_producer_data.usgs.sites.site import Site


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
            agency_cd='tcodizmaepqquflqytsg',
            site_no='rfuddlekhggjwyeeidbd',
            station_nm='zvklfrukuzsevbuudfpd',
            site_tp_cd='nmbwnsrgeclaeaftxhel',
            lat_va='mvkpwgkcsfjzofwtjswz',
            long_va='twukygyuzkybaddyhgxa',
            dec_lat_va=float(10.794733823040204),
            dec_long_va=float(92.31480870374166),
            coord_meth_cd='pcodvmabcvgjhyiyuqxe',
            coord_acy_cd='xppiheppbymoyhtwohtt',
            coord_datum_cd='vqooouchxfulrcclurlh',
            dec_coord_datum_cd='djfrbycsjdsgbnsuabqx',
            district_cd='phatexvxfxwsjqzpnexo',
            state_cd='jzpyuwmobnontxxtmhvb',
            county_cd='fxchujhrjygdjnhqglii',
            country_cd='evajzroycsoxveshmjmf',
            land_net_ds='hbriavbopqvtrjjqzryz',
            map_nm='upuvezmwkmuldweemzxe',
            map_scale_fc=float(89.25548696811596),
            alt_va=float(44.746525296418994),
            alt_meth_cd='hklrsbwjeikyfviwcgfs',
            alt_acy_va=float(61.14349985967722),
            alt_datum_cd='ukzgftnfzdwdirfezlmb',
            huc_cd='sirqbbcdkgbzliyprtct',
            basin_cd='ibrvcgvszsideqftgkdj',
            topo_cd='opofmjsqibetzzkakudq',
            instruments_cd='pgjzzcaoukqcmxmfmhli',
            construction_dt='jynkigfoyezptiwkfind',
            inventory_dt='csnmqawncceyaaohnfxx',
            drain_area_va=float(55.7377665112297),
            contrib_drain_area_va=float(89.46942492018033),
            tz_cd='vxzqnntfukhficqpquyx',
            local_time_fg=True,
            reliability_cd='qpkquhtbhyxdcckfgdic',
            gw_file_cd='dheuuebctwutsltptnmt',
            nat_aqfr_cd='hmowioijtpniwzwdgqwy',
            aqfr_cd='acyhnmpypizozfucdyjc',
            aqfr_type_cd='qkfeymbmcjhxskfgafqg',
            well_depth_va=float(22.583208642281328),
            hole_depth_va=float(4.3069611257407825),
            depth_src_cd='tehusabsltqeyawbjewi',
            project_no='ggzbjydtdqniutgcxzcv'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'tcodizmaepqquflqytsg'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rfuddlekhggjwyeeidbd'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'zvklfrukuzsevbuudfpd'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'nmbwnsrgeclaeaftxhel'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_lat_va_property(self):
        """
        Test lat_va property
        """
        test_value = 'mvkpwgkcsfjzofwtjswz'
        self.instance.lat_va = test_value
        self.assertEqual(self.instance.lat_va, test_value)
    
    def test_long_va_property(self):
        """
        Test long_va property
        """
        test_value = 'twukygyuzkybaddyhgxa'
        self.instance.long_va = test_value
        self.assertEqual(self.instance.long_va, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(10.794733823040204)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(92.31480870374166)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_meth_cd_property(self):
        """
        Test coord_meth_cd property
        """
        test_value = 'pcodvmabcvgjhyiyuqxe'
        self.instance.coord_meth_cd = test_value
        self.assertEqual(self.instance.coord_meth_cd, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'xppiheppbymoyhtwohtt'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_coord_datum_cd_property(self):
        """
        Test coord_datum_cd property
        """
        test_value = 'vqooouchxfulrcclurlh'
        self.instance.coord_datum_cd = test_value
        self.assertEqual(self.instance.coord_datum_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'djfrbycsjdsgbnsuabqx'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_district_cd_property(self):
        """
        Test district_cd property
        """
        test_value = 'phatexvxfxwsjqzpnexo'
        self.instance.district_cd = test_value
        self.assertEqual(self.instance.district_cd, test_value)
    
    def test_state_cd_property(self):
        """
        Test state_cd property
        """
        test_value = 'jzpyuwmobnontxxtmhvb'
        self.instance.state_cd = test_value
        self.assertEqual(self.instance.state_cd, test_value)
    
    def test_county_cd_property(self):
        """
        Test county_cd property
        """
        test_value = 'fxchujhrjygdjnhqglii'
        self.instance.county_cd = test_value
        self.assertEqual(self.instance.county_cd, test_value)
    
    def test_country_cd_property(self):
        """
        Test country_cd property
        """
        test_value = 'evajzroycsoxveshmjmf'
        self.instance.country_cd = test_value
        self.assertEqual(self.instance.country_cd, test_value)
    
    def test_land_net_ds_property(self):
        """
        Test land_net_ds property
        """
        test_value = 'hbriavbopqvtrjjqzryz'
        self.instance.land_net_ds = test_value
        self.assertEqual(self.instance.land_net_ds, test_value)
    
    def test_map_nm_property(self):
        """
        Test map_nm property
        """
        test_value = 'upuvezmwkmuldweemzxe'
        self.instance.map_nm = test_value
        self.assertEqual(self.instance.map_nm, test_value)
    
    def test_map_scale_fc_property(self):
        """
        Test map_scale_fc property
        """
        test_value = float(89.25548696811596)
        self.instance.map_scale_fc = test_value
        self.assertEqual(self.instance.map_scale_fc, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(44.746525296418994)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_meth_cd_property(self):
        """
        Test alt_meth_cd property
        """
        test_value = 'hklrsbwjeikyfviwcgfs'
        self.instance.alt_meth_cd = test_value
        self.assertEqual(self.instance.alt_meth_cd, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(61.14349985967722)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'ukzgftnfzdwdirfezlmb'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
    def test_huc_cd_property(self):
        """
        Test huc_cd property
        """
        test_value = 'sirqbbcdkgbzliyprtct'
        self.instance.huc_cd = test_value
        self.assertEqual(self.instance.huc_cd, test_value)
    
    def test_basin_cd_property(self):
        """
        Test basin_cd property
        """
        test_value = 'ibrvcgvszsideqftgkdj'
        self.instance.basin_cd = test_value
        self.assertEqual(self.instance.basin_cd, test_value)
    
    def test_topo_cd_property(self):
        """
        Test topo_cd property
        """
        test_value = 'opofmjsqibetzzkakudq'
        self.instance.topo_cd = test_value
        self.assertEqual(self.instance.topo_cd, test_value)
    
    def test_instruments_cd_property(self):
        """
        Test instruments_cd property
        """
        test_value = 'pgjzzcaoukqcmxmfmhli'
        self.instance.instruments_cd = test_value
        self.assertEqual(self.instance.instruments_cd, test_value)
    
    def test_construction_dt_property(self):
        """
        Test construction_dt property
        """
        test_value = 'jynkigfoyezptiwkfind'
        self.instance.construction_dt = test_value
        self.assertEqual(self.instance.construction_dt, test_value)
    
    def test_inventory_dt_property(self):
        """
        Test inventory_dt property
        """
        test_value = 'csnmqawncceyaaohnfxx'
        self.instance.inventory_dt = test_value
        self.assertEqual(self.instance.inventory_dt, test_value)
    
    def test_drain_area_va_property(self):
        """
        Test drain_area_va property
        """
        test_value = float(55.7377665112297)
        self.instance.drain_area_va = test_value
        self.assertEqual(self.instance.drain_area_va, test_value)
    
    def test_contrib_drain_area_va_property(self):
        """
        Test contrib_drain_area_va property
        """
        test_value = float(89.46942492018033)
        self.instance.contrib_drain_area_va = test_value
        self.assertEqual(self.instance.contrib_drain_area_va, test_value)
    
    def test_tz_cd_property(self):
        """
        Test tz_cd property
        """
        test_value = 'vxzqnntfukhficqpquyx'
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
        test_value = 'qpkquhtbhyxdcckfgdic'
        self.instance.reliability_cd = test_value
        self.assertEqual(self.instance.reliability_cd, test_value)
    
    def test_gw_file_cd_property(self):
        """
        Test gw_file_cd property
        """
        test_value = 'dheuuebctwutsltptnmt'
        self.instance.gw_file_cd = test_value
        self.assertEqual(self.instance.gw_file_cd, test_value)
    
    def test_nat_aqfr_cd_property(self):
        """
        Test nat_aqfr_cd property
        """
        test_value = 'hmowioijtpniwzwdgqwy'
        self.instance.nat_aqfr_cd = test_value
        self.assertEqual(self.instance.nat_aqfr_cd, test_value)
    
    def test_aqfr_cd_property(self):
        """
        Test aqfr_cd property
        """
        test_value = 'acyhnmpypizozfucdyjc'
        self.instance.aqfr_cd = test_value
        self.assertEqual(self.instance.aqfr_cd, test_value)
    
    def test_aqfr_type_cd_property(self):
        """
        Test aqfr_type_cd property
        """
        test_value = 'qkfeymbmcjhxskfgafqg'
        self.instance.aqfr_type_cd = test_value
        self.assertEqual(self.instance.aqfr_type_cd, test_value)
    
    def test_well_depth_va_property(self):
        """
        Test well_depth_va property
        """
        test_value = float(22.583208642281328)
        self.instance.well_depth_va = test_value
        self.assertEqual(self.instance.well_depth_va, test_value)
    
    def test_hole_depth_va_property(self):
        """
        Test hole_depth_va property
        """
        test_value = float(4.3069611257407825)
        self.instance.hole_depth_va = test_value
        self.assertEqual(self.instance.hole_depth_va, test_value)
    
    def test_depth_src_cd_property(self):
        """
        Test depth_src_cd property
        """
        test_value = 'tehusabsltqeyawbjewi'
        self.instance.depth_src_cd = test_value
        self.assertEqual(self.instance.depth_src_cd, test_value)
    
    def test_project_no_property(self):
        """
        Test project_no property
        """
        test_value = 'ggzbjydtdqniutgcxzcv'
        self.instance.project_no = test_value
        self.assertEqual(self.instance.project_no, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Site.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

