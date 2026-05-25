"""
Test case for Metar
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from aviationweather_mqtt_producer_data.metar import Metar
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
            icao_id='vhrtccqxiohjjctosotr',
            obs_time=datetime.datetime.now(datetime.timezone.utc),
            report_time=datetime.datetime.now(datetime.timezone.utc),
            temp=float(59.21871762662666),
            dewp=float(73.10670927501097),
            wdir=int(51),
            wspd=int(4),
            wgst=int(81),
            visib='hbanvybwzejhfacksrfs',
            altim=float(5.103092972638268),
            slp=float(74.59911975971345),
            qc_field=int(65),
            wx_string='mxvhjexnfjjanjklpjga',
            metar_type='iuvvsyrvxgsawocviiyq',
            raw_ob='oqwqkhzaaltehmipwqmt',
            latitude=float(95.28752500882293),
            longitude=float(2.749742701776392),
            elevation=float(77.56758903367417),
            flt_cat='eronbwnuqdwsgujpurmg',
            clouds='vhyjptiuwwonrsvfvull',
            name='ohefiqwhnicllseeysvb'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'vhrtccqxiohjjctosotr'
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
        test_value = float(59.21871762662666)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_dewp_property(self):
        """
        Test dewp property
        """
        test_value = float(73.10670927501097)
        self.instance.dewp = test_value
        self.assertEqual(self.instance.dewp, test_value)
    
    def test_wdir_property(self):
        """
        Test wdir property
        """
        test_value = int(51)
        self.instance.wdir = test_value
        self.assertEqual(self.instance.wdir, test_value)
    
    def test_wspd_property(self):
        """
        Test wspd property
        """
        test_value = int(4)
        self.instance.wspd = test_value
        self.assertEqual(self.instance.wspd, test_value)
    
    def test_wgst_property(self):
        """
        Test wgst property
        """
        test_value = int(81)
        self.instance.wgst = test_value
        self.assertEqual(self.instance.wgst, test_value)
    
    def test_visib_property(self):
        """
        Test visib property
        """
        test_value = 'hbanvybwzejhfacksrfs'
        self.instance.visib = test_value
        self.assertEqual(self.instance.visib, test_value)
    
    def test_altim_property(self):
        """
        Test altim property
        """
        test_value = float(5.103092972638268)
        self.instance.altim = test_value
        self.assertEqual(self.instance.altim, test_value)
    
    def test_slp_property(self):
        """
        Test slp property
        """
        test_value = float(74.59911975971345)
        self.instance.slp = test_value
        self.assertEqual(self.instance.slp, test_value)
    
    def test_qc_field_property(self):
        """
        Test qc_field property
        """
        test_value = int(65)
        self.instance.qc_field = test_value
        self.assertEqual(self.instance.qc_field, test_value)
    
    def test_wx_string_property(self):
        """
        Test wx_string property
        """
        test_value = 'mxvhjexnfjjanjklpjga'
        self.instance.wx_string = test_value
        self.assertEqual(self.instance.wx_string, test_value)
    
    def test_metar_type_property(self):
        """
        Test metar_type property
        """
        test_value = 'iuvvsyrvxgsawocviiyq'
        self.instance.metar_type = test_value
        self.assertEqual(self.instance.metar_type, test_value)
    
    def test_raw_ob_property(self):
        """
        Test raw_ob property
        """
        test_value = 'oqwqkhzaaltehmipwqmt'
        self.instance.raw_ob = test_value
        self.assertEqual(self.instance.raw_ob, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(95.28752500882293)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(2.749742701776392)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(77.56758903367417)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_flt_cat_property(self):
        """
        Test flt_cat property
        """
        test_value = 'eronbwnuqdwsgujpurmg'
        self.instance.flt_cat = test_value
        self.assertEqual(self.instance.flt_cat, test_value)
    
    def test_clouds_property(self):
        """
        Test clouds property
        """
        test_value = 'vhyjptiuwwonrsvfvull'
        self.instance.clouds = test_value
        self.assertEqual(self.instance.clouds, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ohefiqwhnicllseeysvb'
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

