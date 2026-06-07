"""
Test case for EarthquakeReport
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_quake_producer_data.earthquakereport import EarthquakeReport
from jma_bosai_quake_producer_data.affectedprefecture import AffectedPrefecture
from jma_bosai_quake_producer_data.maxintensityenum import MaxIntensityenum
from jma_bosai_quake_producer_data.affectedcity import AffectedCity
from jma_bosai_quake_producer_data.infotypeenum import InfoTypeenum
from jma_bosai_quake_producer_data.bulletintypeenum import BulletinTypeenum
import datetime


class Test_EarthquakeReport(unittest.TestCase):
    """
    Test case for EarthquakeReport
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EarthquakeReport.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EarthquakeReport for testing
        """
        instance = EarthquakeReport(
            prefecture='wfphjtdzotowsorwnukz',
            magnitude_bucket='vlfirfgffdrabahwkopj',
            event_id='kvupqzxkmlkekyhskgee',
            serial=int(23),
            report_id='fwebykfrxcmwycfanomh',
            info_type=InfoTypeenum.ISSUED,
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            control_datetime=datetime.datetime.now(datetime.timezone.utc),
            control_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            origin_datetime=datetime.datetime.now(datetime.timezone.utc),
            origin_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            title_jp='zhxelhuclarerrtwwhhr',
            title_en='nmtlsincastfgduduxzg',
            epicenter_area_code='pebcbsqerahpmdmgmazd',
            epicenter_area_jp='ywltajaplmzcqvanwxpo',
            epicenter_area_en='zhvcaqwhkzjbmdasbtrr',
            latitude=float(60.126398733280226),
            longitude=float(43.10696309804229),
            depth_km=float(74.35338581856773),
            magnitude=float(66.94679135547042),
            max_intensity=MaxIntensityenum.INTENSITY_1,
            bulletin_type=BulletinTypeenum.VXSE51,
            detail_url='ogcslpncauzpwsrfutfo',
            affected_prefectures=[None],
            affected_cities=[None, None, None, None, None],
            tsunami_possible=True
        )
        return instance

    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'wfphjtdzotowsorwnukz'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_magnitude_bucket_property(self):
        """
        Test magnitude_bucket property
        """
        test_value = 'vlfirfgffdrabahwkopj'
        self.instance.magnitude_bucket = test_value
        self.assertEqual(self.instance.magnitude_bucket, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'kvupqzxkmlkekyhskgee'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_serial_property(self):
        """
        Test serial property
        """
        test_value = int(23)
        self.instance.serial = test_value
        self.assertEqual(self.instance.serial, test_value)
    
    def test_report_id_property(self):
        """
        Test report_id property
        """
        test_value = 'fwebykfrxcmwycfanomh'
        self.instance.report_id = test_value
        self.assertEqual(self.instance.report_id, test_value)
    
    def test_info_type_property(self):
        """
        Test info_type property
        """
        test_value = InfoTypeenum.ISSUED
        self.instance.info_type = test_value
        self.assertEqual(self.instance.info_type, test_value)
    
    def test_report_datetime_property(self):
        """
        Test report_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime = test_value
        self.assertEqual(self.instance.report_datetime, test_value)
    
    def test_report_datetime_local_property(self):
        """
        Test report_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime_local = test_value
        self.assertEqual(self.instance.report_datetime_local, test_value)
    
    def test_control_datetime_property(self):
        """
        Test control_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.control_datetime = test_value
        self.assertEqual(self.instance.control_datetime, test_value)
    
    def test_control_datetime_local_property(self):
        """
        Test control_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.control_datetime_local = test_value
        self.assertEqual(self.instance.control_datetime_local, test_value)
    
    def test_origin_datetime_property(self):
        """
        Test origin_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.origin_datetime = test_value
        self.assertEqual(self.instance.origin_datetime, test_value)
    
    def test_origin_datetime_local_property(self):
        """
        Test origin_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.origin_datetime_local = test_value
        self.assertEqual(self.instance.origin_datetime_local, test_value)
    
    def test_title_jp_property(self):
        """
        Test title_jp property
        """
        test_value = 'zhxelhuclarerrtwwhhr'
        self.instance.title_jp = test_value
        self.assertEqual(self.instance.title_jp, test_value)
    
    def test_title_en_property(self):
        """
        Test title_en property
        """
        test_value = 'nmtlsincastfgduduxzg'
        self.instance.title_en = test_value
        self.assertEqual(self.instance.title_en, test_value)
    
    def test_epicenter_area_code_property(self):
        """
        Test epicenter_area_code property
        """
        test_value = 'pebcbsqerahpmdmgmazd'
        self.instance.epicenter_area_code = test_value
        self.assertEqual(self.instance.epicenter_area_code, test_value)
    
    def test_epicenter_area_jp_property(self):
        """
        Test epicenter_area_jp property
        """
        test_value = 'ywltajaplmzcqvanwxpo'
        self.instance.epicenter_area_jp = test_value
        self.assertEqual(self.instance.epicenter_area_jp, test_value)
    
    def test_epicenter_area_en_property(self):
        """
        Test epicenter_area_en property
        """
        test_value = 'zhvcaqwhkzjbmdasbtrr'
        self.instance.epicenter_area_en = test_value
        self.assertEqual(self.instance.epicenter_area_en, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(60.126398733280226)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(43.10696309804229)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_km_property(self):
        """
        Test depth_km property
        """
        test_value = float(74.35338581856773)
        self.instance.depth_km = test_value
        self.assertEqual(self.instance.depth_km, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(66.94679135547042)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_max_intensity_property(self):
        """
        Test max_intensity property
        """
        test_value = MaxIntensityenum.INTENSITY_1
        self.instance.max_intensity = test_value
        self.assertEqual(self.instance.max_intensity, test_value)
    
    def test_bulletin_type_property(self):
        """
        Test bulletin_type property
        """
        test_value = BulletinTypeenum.VXSE51
        self.instance.bulletin_type = test_value
        self.assertEqual(self.instance.bulletin_type, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'ogcslpncauzpwsrfutfo'
        self.instance.detail_url = test_value
        self.assertEqual(self.instance.detail_url, test_value)
    
    def test_affected_prefectures_property(self):
        """
        Test affected_prefectures property
        """
        test_value = [None]
        self.instance.affected_prefectures = test_value
        self.assertEqual(self.instance.affected_prefectures, test_value)
    
    def test_affected_cities_property(self):
        """
        Test affected_cities property
        """
        test_value = [None, None, None, None, None]
        self.instance.affected_cities = test_value
        self.assertEqual(self.instance.affected_cities, test_value)
    
    def test_tsunami_possible_property(self):
        """
        Test tsunami_possible property
        """
        test_value = True
        self.instance.tsunami_possible = test_value
        self.assertEqual(self.instance.tsunami_possible, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EarthquakeReport.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EarthquakeReport.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)


