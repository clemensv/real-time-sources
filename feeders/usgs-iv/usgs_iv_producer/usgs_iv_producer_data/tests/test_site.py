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
            agency_cd='pkmjimmhcjxrmmypabsn',
            site_no='rlodoydhawrtkavcyeys',
            station_nm='diiqesgwkjogtzojreis',
            site_tp_cd='abraxgxaurqlubpmjzkt',
            lat_va='qtgsbvmchikdbqmpznph',
            long_va='uxwbjjwvfcxpsaranagc',
            dec_lat_va=float(50.44394509645467),
            dec_long_va=float(27.59247969462847),
            coord_meth_cd='xkxtcijesaksvtdpszau',
            coord_acy_cd='hxldiveoqgcjotsoarge',
            coord_datum_cd='yycveumabiftyhgwilvv',
            dec_coord_datum_cd='vjsjzltswsyggwxychlq',
            district_cd='dhiuwhcfuidlacgpqwnb',
            state_cd='xtvcurnxnzihqeqtegyy',
            county_cd='mustilekoafytidnjszt',
            country_cd='iesiejslrundeurcefkm',
            land_net_ds='xyodnmsgkllvqtquwcor',
            map_nm='vswpqjagyyrdlqtlswry',
            map_scale_fc=float(46.638118188201496),
            alt_va=float(2.2201163098746868),
            alt_meth_cd='akpogekitsngigsulaor',
            alt_acy_va=float(94.7673055082616),
            alt_datum_cd='vnsedjsktqqzrdfllsdj',
            huc_cd='hlpdyraolxalwcqyqknh',
            basin_cd='bibtabvzsrbswnxwyhxr',
            topo_cd='tnuhowsjjwaafvcednpz',
            instruments_cd='ebdvndffpfgqhxjulbak',
            construction_dt='kqcvrfxeaohjkggeytco',
            inventory_dt='owjaeprizttfygprppdh',
            drain_area_va=float(1.3940120624103103),
            contrib_drain_area_va=float(29.538892306756924),
            tz_cd='wzmxuacgfosvjbadstou',
            local_time_fg=True,
            reliability_cd='ghmmpjqqbcceiqynwfpw',
            gw_file_cd='kbvicymfgvwxjuxcruip',
            nat_aqfr_cd='vuvmjtaziwombtepyznq',
            aqfr_cd='jpodcrlbswfxfgmwmcej',
            aqfr_type_cd='pibpsjvxwavxkkogvffw',
            well_depth_va=float(46.6607892815963),
            hole_depth_va=float(44.81395734911722),
            depth_src_cd='snkapogilupeisgwlekp',
            project_no='ivwkljfnseslcyyubxsh'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'pkmjimmhcjxrmmypabsn'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'rlodoydhawrtkavcyeys'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'diiqesgwkjogtzojreis'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'abraxgxaurqlubpmjzkt'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_lat_va_property(self):
        """
        Test lat_va property
        """
        test_value = 'qtgsbvmchikdbqmpznph'
        self.instance.lat_va = test_value
        self.assertEqual(self.instance.lat_va, test_value)
    
    def test_long_va_property(self):
        """
        Test long_va property
        """
        test_value = 'uxwbjjwvfcxpsaranagc'
        self.instance.long_va = test_value
        self.assertEqual(self.instance.long_va, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(50.44394509645467)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(27.59247969462847)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_meth_cd_property(self):
        """
        Test coord_meth_cd property
        """
        test_value = 'xkxtcijesaksvtdpszau'
        self.instance.coord_meth_cd = test_value
        self.assertEqual(self.instance.coord_meth_cd, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'hxldiveoqgcjotsoarge'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_coord_datum_cd_property(self):
        """
        Test coord_datum_cd property
        """
        test_value = 'yycveumabiftyhgwilvv'
        self.instance.coord_datum_cd = test_value
        self.assertEqual(self.instance.coord_datum_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'vjsjzltswsyggwxychlq'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_district_cd_property(self):
        """
        Test district_cd property
        """
        test_value = 'dhiuwhcfuidlacgpqwnb'
        self.instance.district_cd = test_value
        self.assertEqual(self.instance.district_cd, test_value)
    
    def test_state_cd_property(self):
        """
        Test state_cd property
        """
        test_value = 'xtvcurnxnzihqeqtegyy'
        self.instance.state_cd = test_value
        self.assertEqual(self.instance.state_cd, test_value)
    
    def test_county_cd_property(self):
        """
        Test county_cd property
        """
        test_value = 'mustilekoafytidnjszt'
        self.instance.county_cd = test_value
        self.assertEqual(self.instance.county_cd, test_value)
    
    def test_country_cd_property(self):
        """
        Test country_cd property
        """
        test_value = 'iesiejslrundeurcefkm'
        self.instance.country_cd = test_value
        self.assertEqual(self.instance.country_cd, test_value)
    
    def test_land_net_ds_property(self):
        """
        Test land_net_ds property
        """
        test_value = 'xyodnmsgkllvqtquwcor'
        self.instance.land_net_ds = test_value
        self.assertEqual(self.instance.land_net_ds, test_value)
    
    def test_map_nm_property(self):
        """
        Test map_nm property
        """
        test_value = 'vswpqjagyyrdlqtlswry'
        self.instance.map_nm = test_value
        self.assertEqual(self.instance.map_nm, test_value)
    
    def test_map_scale_fc_property(self):
        """
        Test map_scale_fc property
        """
        test_value = float(46.638118188201496)
        self.instance.map_scale_fc = test_value
        self.assertEqual(self.instance.map_scale_fc, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(2.2201163098746868)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_meth_cd_property(self):
        """
        Test alt_meth_cd property
        """
        test_value = 'akpogekitsngigsulaor'
        self.instance.alt_meth_cd = test_value
        self.assertEqual(self.instance.alt_meth_cd, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(94.7673055082616)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'vnsedjsktqqzrdfllsdj'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
    def test_huc_cd_property(self):
        """
        Test huc_cd property
        """
        test_value = 'hlpdyraolxalwcqyqknh'
        self.instance.huc_cd = test_value
        self.assertEqual(self.instance.huc_cd, test_value)
    
    def test_basin_cd_property(self):
        """
        Test basin_cd property
        """
        test_value = 'bibtabvzsrbswnxwyhxr'
        self.instance.basin_cd = test_value
        self.assertEqual(self.instance.basin_cd, test_value)
    
    def test_topo_cd_property(self):
        """
        Test topo_cd property
        """
        test_value = 'tnuhowsjjwaafvcednpz'
        self.instance.topo_cd = test_value
        self.assertEqual(self.instance.topo_cd, test_value)
    
    def test_instruments_cd_property(self):
        """
        Test instruments_cd property
        """
        test_value = 'ebdvndffpfgqhxjulbak'
        self.instance.instruments_cd = test_value
        self.assertEqual(self.instance.instruments_cd, test_value)
    
    def test_construction_dt_property(self):
        """
        Test construction_dt property
        """
        test_value = 'kqcvrfxeaohjkggeytco'
        self.instance.construction_dt = test_value
        self.assertEqual(self.instance.construction_dt, test_value)
    
    def test_inventory_dt_property(self):
        """
        Test inventory_dt property
        """
        test_value = 'owjaeprizttfygprppdh'
        self.instance.inventory_dt = test_value
        self.assertEqual(self.instance.inventory_dt, test_value)
    
    def test_drain_area_va_property(self):
        """
        Test drain_area_va property
        """
        test_value = float(1.3940120624103103)
        self.instance.drain_area_va = test_value
        self.assertEqual(self.instance.drain_area_va, test_value)
    
    def test_contrib_drain_area_va_property(self):
        """
        Test contrib_drain_area_va property
        """
        test_value = float(29.538892306756924)
        self.instance.contrib_drain_area_va = test_value
        self.assertEqual(self.instance.contrib_drain_area_va, test_value)
    
    def test_tz_cd_property(self):
        """
        Test tz_cd property
        """
        test_value = 'wzmxuacgfosvjbadstou'
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
        test_value = 'ghmmpjqqbcceiqynwfpw'
        self.instance.reliability_cd = test_value
        self.assertEqual(self.instance.reliability_cd, test_value)
    
    def test_gw_file_cd_property(self):
        """
        Test gw_file_cd property
        """
        test_value = 'kbvicymfgvwxjuxcruip'
        self.instance.gw_file_cd = test_value
        self.assertEqual(self.instance.gw_file_cd, test_value)
    
    def test_nat_aqfr_cd_property(self):
        """
        Test nat_aqfr_cd property
        """
        test_value = 'vuvmjtaziwombtepyznq'
        self.instance.nat_aqfr_cd = test_value
        self.assertEqual(self.instance.nat_aqfr_cd, test_value)
    
    def test_aqfr_cd_property(self):
        """
        Test aqfr_cd property
        """
        test_value = 'jpodcrlbswfxfgmwmcej'
        self.instance.aqfr_cd = test_value
        self.assertEqual(self.instance.aqfr_cd, test_value)
    
    def test_aqfr_type_cd_property(self):
        """
        Test aqfr_type_cd property
        """
        test_value = 'pibpsjvxwavxkkogvffw'
        self.instance.aqfr_type_cd = test_value
        self.assertEqual(self.instance.aqfr_type_cd, test_value)
    
    def test_well_depth_va_property(self):
        """
        Test well_depth_va property
        """
        test_value = float(46.6607892815963)
        self.instance.well_depth_va = test_value
        self.assertEqual(self.instance.well_depth_va, test_value)
    
    def test_hole_depth_va_property(self):
        """
        Test hole_depth_va property
        """
        test_value = float(44.81395734911722)
        self.instance.hole_depth_va = test_value
        self.assertEqual(self.instance.hole_depth_va, test_value)
    
    def test_depth_src_cd_property(self):
        """
        Test depth_src_cd property
        """
        test_value = 'snkapogilupeisgwlekp'
        self.instance.depth_src_cd = test_value
        self.assertEqual(self.instance.depth_src_cd, test_value)
    
    def test_project_no_property(self):
        """
        Test project_no property
        """
        test_value = 'ivwkljfnseslcyyubxsh'
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

