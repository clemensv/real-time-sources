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
            agency_cd='gxsvzhdfsanzmnomllob',
            site_no='nqfmofoxmfrdlnrravkh',
            station_nm='svvrqqarvigblzirimyc',
            site_tp_cd='rgqcdqgqowvmztrilshx',
            dec_lat_va=float(34.71144559971256),
            dec_long_va=float(52.730965531771155),
            coord_acy_cd='empgpcrwznnmsnbohxdu',
            dec_coord_datum_cd='wwytfjttroxvdgcxwxuq',
            alt_va=float(93.09156700051052),
            alt_acy_va=float(13.887457811307847),
            alt_datum_cd='yqjnusfafhiamkbijtet'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'gxsvzhdfsanzmnomllob'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'nqfmofoxmfrdlnrravkh'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'svvrqqarvigblzirimyc'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'rgqcdqgqowvmztrilshx'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(34.71144559971256)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(52.730965531771155)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'empgpcrwznnmsnbohxdu'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'wwytfjttroxvdgcxwxuq'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(93.09156700051052)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(13.887457811307847)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'yqjnusfafhiamkbijtet'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    
