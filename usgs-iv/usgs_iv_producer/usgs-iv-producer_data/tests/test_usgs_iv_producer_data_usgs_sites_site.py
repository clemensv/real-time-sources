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
            agency_cd='pkfmmruflwvybcrxowmr',
            site_no='nezgouyhexrjcnynxwev',
            station_nm='inrthaegwnusblgfonle',
            site_tp_cd='xkiiywmkdnuaomtwladx',
            lat_va='pssjtdqkfjauuveiczxs',
            long_va='fzhknnuwdmjxzxznunys',
            dec_lat_va=float(87.83513831672431),
            dec_long_va=float(6.264639230751179),
            coord_meth_cd='tvqtzrgfdlqbxvlgzwnb',
            coord_acy_cd='jhtyfdzzgjcffhymhbry',
            coord_datum_cd='cbblnpvcktulmieglydm',
            dec_coord_datum_cd='llfyoewwduontdkujqja',
            district_cd='ohrwazdqojxfmfiawojg',
            state_cd='uvefrxvjqkdonsdoosin',
            county_cd='wcgepfwvugvkqwlpegrp',
            country_cd='bklfrhneamzkxdvmcjzf',
            land_net_ds='zjosctlpmskrhccdntyy',
            map_nm='sczsxtypnfuyqzoufczd',
            map_scale_fc=float(92.69029365917545),
            alt_va=float(75.5582753791),
            alt_meth_cd='ogmnhfxymeztuomodpxc',
            alt_acy_va=float(49.704657555352995),
            alt_datum_cd='pqmxhfglvqewhnrfkqlp',
            huc_cd='gaxdubuavsskmfdazrue',
            basin_cd='ketorqrhiijzhfoccxwm',
            topo_cd='epgjacgqiixhbplokjnv',
            instruments_cd='udpkgugizbbbvnxydehr',
            construction_dt='xbxflngrgdxjrvaijlep',
            inventory_dt='tjskhjjzournzmigeaig',
            drain_area_va=float(49.98801506064016),
            contrib_drain_area_va=float(24.06523225599404),
            tz_cd='sruqapemecofpkvrmgai',
            local_time_fg=True,
            reliability_cd='tcjwwuyxnmpnzomqprir',
            gw_file_cd='ekafviacbwbhmcidqcnn',
            nat_aqfr_cd='emdtpszlsowfxuapixvb',
            aqfr_cd='xoarvfdcolegfwvuscav',
            aqfr_type_cd='gewypqzqkhrjrtqjxdkj',
            well_depth_va=float(86.86807964264412),
            hole_depth_va=float(31.91891755088253),
            depth_src_cd='nibapveffsjcfxvbldwf',
            project_no='hidqkgvbhkmvczfvmsiq'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'pkfmmruflwvybcrxowmr'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'nezgouyhexrjcnynxwev'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'inrthaegwnusblgfonle'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'xkiiywmkdnuaomtwladx'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_lat_va_property(self):
        """
        Test lat_va property
        """
        test_value = 'pssjtdqkfjauuveiczxs'
        self.instance.lat_va = test_value
        self.assertEqual(self.instance.lat_va, test_value)
    
    def test_long_va_property(self):
        """
        Test long_va property
        """
        test_value = 'fzhknnuwdmjxzxznunys'
        self.instance.long_va = test_value
        self.assertEqual(self.instance.long_va, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(87.83513831672431)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(6.264639230751179)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_meth_cd_property(self):
        """
        Test coord_meth_cd property
        """
        test_value = 'tvqtzrgfdlqbxvlgzwnb'
        self.instance.coord_meth_cd = test_value
        self.assertEqual(self.instance.coord_meth_cd, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'jhtyfdzzgjcffhymhbry'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_coord_datum_cd_property(self):
        """
        Test coord_datum_cd property
        """
        test_value = 'cbblnpvcktulmieglydm'
        self.instance.coord_datum_cd = test_value
        self.assertEqual(self.instance.coord_datum_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'llfyoewwduontdkujqja'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_district_cd_property(self):
        """
        Test district_cd property
        """
        test_value = 'ohrwazdqojxfmfiawojg'
        self.instance.district_cd = test_value
        self.assertEqual(self.instance.district_cd, test_value)
    
    def test_state_cd_property(self):
        """
        Test state_cd property
        """
        test_value = 'uvefrxvjqkdonsdoosin'
        self.instance.state_cd = test_value
        self.assertEqual(self.instance.state_cd, test_value)
    
    def test_county_cd_property(self):
        """
        Test county_cd property
        """
        test_value = 'wcgepfwvugvkqwlpegrp'
        self.instance.county_cd = test_value
        self.assertEqual(self.instance.county_cd, test_value)
    
    def test_country_cd_property(self):
        """
        Test country_cd property
        """
        test_value = 'bklfrhneamzkxdvmcjzf'
        self.instance.country_cd = test_value
        self.assertEqual(self.instance.country_cd, test_value)
    
    def test_land_net_ds_property(self):
        """
        Test land_net_ds property
        """
        test_value = 'zjosctlpmskrhccdntyy'
        self.instance.land_net_ds = test_value
        self.assertEqual(self.instance.land_net_ds, test_value)
    
    def test_map_nm_property(self):
        """
        Test map_nm property
        """
        test_value = 'sczsxtypnfuyqzoufczd'
        self.instance.map_nm = test_value
        self.assertEqual(self.instance.map_nm, test_value)
    
    def test_map_scale_fc_property(self):
        """
        Test map_scale_fc property
        """
        test_value = float(92.69029365917545)
        self.instance.map_scale_fc = test_value
        self.assertEqual(self.instance.map_scale_fc, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(75.5582753791)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_meth_cd_property(self):
        """
        Test alt_meth_cd property
        """
        test_value = 'ogmnhfxymeztuomodpxc'
        self.instance.alt_meth_cd = test_value
        self.assertEqual(self.instance.alt_meth_cd, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(49.704657555352995)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'pqmxhfglvqewhnrfkqlp'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
    def test_huc_cd_property(self):
        """
        Test huc_cd property
        """
        test_value = 'gaxdubuavsskmfdazrue'
        self.instance.huc_cd = test_value
        self.assertEqual(self.instance.huc_cd, test_value)
    
    def test_basin_cd_property(self):
        """
        Test basin_cd property
        """
        test_value = 'ketorqrhiijzhfoccxwm'
        self.instance.basin_cd = test_value
        self.assertEqual(self.instance.basin_cd, test_value)
    
    def test_topo_cd_property(self):
        """
        Test topo_cd property
        """
        test_value = 'epgjacgqiixhbplokjnv'
        self.instance.topo_cd = test_value
        self.assertEqual(self.instance.topo_cd, test_value)
    
    def test_instruments_cd_property(self):
        """
        Test instruments_cd property
        """
        test_value = 'udpkgugizbbbvnxydehr'
        self.instance.instruments_cd = test_value
        self.assertEqual(self.instance.instruments_cd, test_value)
    
    def test_construction_dt_property(self):
        """
        Test construction_dt property
        """
        test_value = 'xbxflngrgdxjrvaijlep'
        self.instance.construction_dt = test_value
        self.assertEqual(self.instance.construction_dt, test_value)
    
    def test_inventory_dt_property(self):
        """
        Test inventory_dt property
        """
        test_value = 'tjskhjjzournzmigeaig'
        self.instance.inventory_dt = test_value
        self.assertEqual(self.instance.inventory_dt, test_value)
    
    def test_drain_area_va_property(self):
        """
        Test drain_area_va property
        """
        test_value = float(49.98801506064016)
        self.instance.drain_area_va = test_value
        self.assertEqual(self.instance.drain_area_va, test_value)
    
    def test_contrib_drain_area_va_property(self):
        """
        Test contrib_drain_area_va property
        """
        test_value = float(24.06523225599404)
        self.instance.contrib_drain_area_va = test_value
        self.assertEqual(self.instance.contrib_drain_area_va, test_value)
    
    def test_tz_cd_property(self):
        """
        Test tz_cd property
        """
        test_value = 'sruqapemecofpkvrmgai'
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
        test_value = 'tcjwwuyxnmpnzomqprir'
        self.instance.reliability_cd = test_value
        self.assertEqual(self.instance.reliability_cd, test_value)
    
    def test_gw_file_cd_property(self):
        """
        Test gw_file_cd property
        """
        test_value = 'ekafviacbwbhmcidqcnn'
        self.instance.gw_file_cd = test_value
        self.assertEqual(self.instance.gw_file_cd, test_value)
    
    def test_nat_aqfr_cd_property(self):
        """
        Test nat_aqfr_cd property
        """
        test_value = 'emdtpszlsowfxuapixvb'
        self.instance.nat_aqfr_cd = test_value
        self.assertEqual(self.instance.nat_aqfr_cd, test_value)
    
    def test_aqfr_cd_property(self):
        """
        Test aqfr_cd property
        """
        test_value = 'xoarvfdcolegfwvuscav'
        self.instance.aqfr_cd = test_value
        self.assertEqual(self.instance.aqfr_cd, test_value)
    
    def test_aqfr_type_cd_property(self):
        """
        Test aqfr_type_cd property
        """
        test_value = 'gewypqzqkhrjrtqjxdkj'
        self.instance.aqfr_type_cd = test_value
        self.assertEqual(self.instance.aqfr_type_cd, test_value)
    
    def test_well_depth_va_property(self):
        """
        Test well_depth_va property
        """
        test_value = float(86.86807964264412)
        self.instance.well_depth_va = test_value
        self.assertEqual(self.instance.well_depth_va, test_value)
    
    def test_hole_depth_va_property(self):
        """
        Test hole_depth_va property
        """
        test_value = float(31.91891755088253)
        self.instance.hole_depth_va = test_value
        self.assertEqual(self.instance.hole_depth_va, test_value)
    
    def test_depth_src_cd_property(self):
        """
        Test depth_src_cd property
        """
        test_value = 'nibapveffsjcfxvbldwf'
        self.instance.depth_src_cd = test_value
        self.assertEqual(self.instance.depth_src_cd, test_value)
    
    def test_project_no_property(self):
        """
        Test project_no property
        """
        test_value = 'hidqkgvbhkmvczfvmsiq'
        self.instance.project_no = test_value
        self.assertEqual(self.instance.project_no, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Site.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
