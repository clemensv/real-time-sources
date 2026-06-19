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
            icao_id='qbbyccpjgdszcxhzjgmh',
            obs_time=datetime.datetime.now(datetime.timezone.utc),
            report_time=datetime.datetime.now(datetime.timezone.utc),
            temp=float(89.41801380349182),
            dewp=float(76.3191198223251),
            wdir=int(3),
            wspd=int(17),
            wgst=int(73),
            visib='snrijlkfquqsuiwlpibs',
            altim=float(99.28945963836625),
            slp=float(88.9116752618568),
            qc_field=int(81),
            wx_string='shhqegilzvrcmfglqobe',
            metar_type='sexyohxqkemxkrbpulfa',
            raw_ob='hujuqojrtascjdsxrkbo',
            latitude=float(18.46037153338983),
            longitude=float(10.35718329400771),
            elevation=float(22.467466692320425),
            flt_cat='jlquxwpfutgltyyqbepv',
            clouds='vqfauwimflxlollvgidu',
            name='uwdzscsejyiesivjjjih'
        )
        return instance

    
    def test_icao_id_property(self):
        """
        Test icao_id property
        """
        test_value = 'qbbyccpjgdszcxhzjgmh'
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
        test_value = float(89.41801380349182)
        self.instance.temp = test_value
        self.assertEqual(self.instance.temp, test_value)
    
    def test_dewp_property(self):
        """
        Test dewp property
        """
        test_value = float(76.3191198223251)
        self.instance.dewp = test_value
        self.assertEqual(self.instance.dewp, test_value)
    
    def test_wdir_property(self):
        """
        Test wdir property
        """
        test_value = int(3)
        self.instance.wdir = test_value
        self.assertEqual(self.instance.wdir, test_value)
    
    def test_wspd_property(self):
        """
        Test wspd property
        """
        test_value = int(17)
        self.instance.wspd = test_value
        self.assertEqual(self.instance.wspd, test_value)
    
    def test_wgst_property(self):
        """
        Test wgst property
        """
        test_value = int(73)
        self.instance.wgst = test_value
        self.assertEqual(self.instance.wgst, test_value)
    
    def test_visib_property(self):
        """
        Test visib property
        """
        test_value = 'snrijlkfquqsuiwlpibs'
        self.instance.visib = test_value
        self.assertEqual(self.instance.visib, test_value)
    
    def test_altim_property(self):
        """
        Test altim property
        """
        test_value = float(99.28945963836625)
        self.instance.altim = test_value
        self.assertEqual(self.instance.altim, test_value)
    
    def test_slp_property(self):
        """
        Test slp property
        """
        test_value = float(88.9116752618568)
        self.instance.slp = test_value
        self.assertEqual(self.instance.slp, test_value)
    
    def test_qc_field_property(self):
        """
        Test qc_field property
        """
        test_value = int(81)
        self.instance.qc_field = test_value
        self.assertEqual(self.instance.qc_field, test_value)
    
    def test_wx_string_property(self):
        """
        Test wx_string property
        """
        test_value = 'shhqegilzvrcmfglqobe'
        self.instance.wx_string = test_value
        self.assertEqual(self.instance.wx_string, test_value)
    
    def test_metar_type_property(self):
        """
        Test metar_type property
        """
        test_value = 'sexyohxqkemxkrbpulfa'
        self.instance.metar_type = test_value
        self.assertEqual(self.instance.metar_type, test_value)
    
    def test_raw_ob_property(self):
        """
        Test raw_ob property
        """
        test_value = 'hujuqojrtascjdsxrkbo'
        self.instance.raw_ob = test_value
        self.assertEqual(self.instance.raw_ob, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(18.46037153338983)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(10.35718329400771)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_property(self):
        """
        Test elevation property
        """
        test_value = float(22.467466692320425)
        self.instance.elevation = test_value
        self.assertEqual(self.instance.elevation, test_value)
    
    def test_flt_cat_property(self):
        """
        Test flt_cat property
        """
        test_value = 'jlquxwpfutgltyyqbepv'
        self.instance.flt_cat = test_value
        self.assertEqual(self.instance.flt_cat, test_value)
    
    def test_clouds_property(self):
        """
        Test clouds property
        """
        test_value = 'vqfauwimflxlollvgidu'
        self.instance.clouds = test_value
        self.assertEqual(self.instance.clouds, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'uwdzscsejyiesivjjjih'
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

