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
            agency_cd='lywtvhsalruzpimmlenq',
            site_no='gewlgrhanpfbmknuhdfc',
            station_nm='muqqvpabueogixejorse',
            site_tp_cd='ctnbgsgzcbtdzjcnkrxs',
            dec_lat_va=float(14.063112737295903),
            dec_long_va=float(10.207566253715772),
            coord_acy_cd='lfoafqqrzziwuippchot',
            dec_coord_datum_cd='icqqblzulptcwxkcmozf',
            alt_va=float(93.48557150652064),
            alt_acy_va=float(64.28798820927469),
            alt_datum_cd='ufixhbyzsbklbuqbhqyo'
        )
        return instance

    
    def test_agency_cd_property(self):
        """
        Test agency_cd property
        """
        test_value = 'lywtvhsalruzpimmlenq'
        self.instance.agency_cd = test_value
        self.assertEqual(self.instance.agency_cd, test_value)
    
    def test_site_no_property(self):
        """
        Test site_no property
        """
        test_value = 'gewlgrhanpfbmknuhdfc'
        self.instance.site_no = test_value
        self.assertEqual(self.instance.site_no, test_value)
    
    def test_station_nm_property(self):
        """
        Test station_nm property
        """
        test_value = 'muqqvpabueogixejorse'
        self.instance.station_nm = test_value
        self.assertEqual(self.instance.station_nm, test_value)
    
    def test_site_tp_cd_property(self):
        """
        Test site_tp_cd property
        """
        test_value = 'ctnbgsgzcbtdzjcnkrxs'
        self.instance.site_tp_cd = test_value
        self.assertEqual(self.instance.site_tp_cd, test_value)
    
    def test_dec_lat_va_property(self):
        """
        Test dec_lat_va property
        """
        test_value = float(14.063112737295903)
        self.instance.dec_lat_va = test_value
        self.assertEqual(self.instance.dec_lat_va, test_value)
    
    def test_dec_long_va_property(self):
        """
        Test dec_long_va property
        """
        test_value = float(10.207566253715772)
        self.instance.dec_long_va = test_value
        self.assertEqual(self.instance.dec_long_va, test_value)
    
    def test_coord_acy_cd_property(self):
        """
        Test coord_acy_cd property
        """
        test_value = 'lfoafqqrzziwuippchot'
        self.instance.coord_acy_cd = test_value
        self.assertEqual(self.instance.coord_acy_cd, test_value)
    
    def test_dec_coord_datum_cd_property(self):
        """
        Test dec_coord_datum_cd property
        """
        test_value = 'icqqblzulptcwxkcmozf'
        self.instance.dec_coord_datum_cd = test_value
        self.assertEqual(self.instance.dec_coord_datum_cd, test_value)
    
    def test_alt_va_property(self):
        """
        Test alt_va property
        """
        test_value = float(93.48557150652064)
        self.instance.alt_va = test_value
        self.assertEqual(self.instance.alt_va, test_value)
    
    def test_alt_acy_va_property(self):
        """
        Test alt_acy_va property
        """
        test_value = float(64.28798820927469)
        self.instance.alt_acy_va = test_value
        self.assertEqual(self.instance.alt_acy_va, test_value)
    
    def test_alt_datum_cd_property(self):
        """
        Test alt_datum_cd property
        """
        test_value = 'ufixhbyzsbklbuqbhqyo'
        self.instance.alt_datum_cd = test_value
        self.assertEqual(self.instance.alt_datum_cd, test_value)
    