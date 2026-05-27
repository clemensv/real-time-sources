"""
Test case for Metar
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aviationweather_producer_data.metar import Metar
import datetime


class Test_Metar(unittest.TestCase):
    """
    Test case for Metar
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Metar.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Metar for testing
        """
        instance = Metar(
            icao_id='iulvyzwabzzodtrtfzay',
            obs_time=datetime.datetime.now(datetime.timezone.utc),
            report_time=datetime.datetime.now(datetime.timezone.utc),
            temp=float(76.73136863945238),
            dewp=float(67.37168005986483),
            wdir=int(96),
            wspd=int(31),
            wgst=int(18),
            visib='ztvfnrbhncijcjofhlyp',
            altim=float(34.81349058175527),
            slp=float(1.469525502506852),
            qc_field=int(85),
            wx_string='peahngsgzxemcvkfotdf',
            metar_type='scbvjozsjcarafwglmnu',
            raw_ob='yqxbtppweizipuinkasy',
            latitude=float(76.67301751094355),
            longitude=float(11.785536421389386),
            elevation=float(31.605887882630658),
            flt_cat='ddfojimvidesvsyqtxzy',
            clouds='bvkzmofqopryklxrscql',
            name='puahodvhoplqixtqvaka'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'iulvyzwabzzodtrtfzay'
        self.instance.icao_id = test_value
        self.assertEqual(self.instance.icao_id, test_value)
    
    def test_obs_time_property(self):
        """
        Test obs_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.obs_time = test_value
        self.assertEqual(self.instance.obs_time, test_value)
    
    def test_report_time_property(self):
        """
        Test report_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_time = test_value
        self.assertEqual(self.instance.report_time, test_value)
    
    def test_temp_property(self):
        """
        Test temp property
        """
        test_value = float(76.73136863945238)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_dewp_property(self):
        """
        Test dewp property
        """
        test_value = float(67.37168005986483)
        self.instance.dewp = test_value
        self.assertEqual(self.instance.dewp, test_value)
    
    def test_wdir_property(self):
        """
        Test wdir property
        """
        test_value = int(96)
        self.instance.wdir = test_value
        self.assertEqual(self.instance.wdir, test_value)
    
    def test_wspd_property(self):
        """
        Test wspd property
        """
        test_value = int(31)
        self.instance.wspd = test_value
        self.assertEqual(self.instance.wspd, test_value)
    
    def test_wgst_property(self):
        """
        Test wgst property
        """
        test_value = int(18)
        self.instance.wgst = test_value
        self.assertEqual(self.instance.wgst, test_value)
    
    def test_visib_property(self):
        """
        Test visib property
        """
        test_value = 'ztvfnrbhncijcjofhlyp'
        self.instance.visib = test_value
        self.assertEqual(self.instance.visib, test_value)
    
    def test_altim_property(self):
        """
        Test altim property
        """
        test_value = float(34.81349058175527)
        self.instance.altim = test_value
        self.assertEqual(self.instance.altim, test_value)
    
    def test_slp_property(self):
        """
        Test slp property
        """
        test_value = float(1.469525502506852)
        self.instance.slp = test_value
        self.assertEqual(self.instance.slp, test_value)
    
    def test_qc_field_property(self):
        """
        Test qc_field property
        """
        test_value = int(85)
        self.instance.qc_field = test_value
        self.assertEqual(self.instance.qc_field, test_value)
    
    def test_wx_string_property(self):
        """
        Test wx_string property
        """
        test_value = 'peahngsgzxemcvkfotdf'
        self.instance.wx_string = test_value
        self.assertEqual(self.instance.wx_string, test_value)
    
    def test_metar_type_property(self):
        """
        Test metar_type property
        """
        test_value = 'scbvjozsjcarafwglmnu'
        self.instance.metar_type = test_value
        self.assertEqual(self.instance.metar_type, test_value)
    
    def test_raw_ob_property(self):
        """
        Test raw_ob property
        """
        test_value = 'yqxbtppweizipuinkasy'
        self.instance.raw_ob = test_value
        self.assertEqual(self.instance.raw_ob, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(76.67301751094355)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(11.785536421389386)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(31.605887882630658)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_flt_cat_property(self):
        """
        Test flt_cat property
        """
        test_value = 'ddfojimvidesvsyqtxzy'
        self.instance.flt_cat = test_value
        self.assertEqual(self.instance.flt_cat, test_value)
    
    def test_clouds_property(self):
        """
        Test clouds property
        """
        test_value = 'bvkzmofqopryklxrscql'
        self.instance.clouds = test_value
        self.assertEqual(self.instance.clouds, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'puahodvhoplqixtqvaka'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Metar.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Metar.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

