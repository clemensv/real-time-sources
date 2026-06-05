"""
Test case for WeatherStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.weatherstation import WeatherStation


class Test_WeatherStation(unittest.TestCase):
    """
    Test case for WeatherStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherStation for testing
        """
        instance = WeatherStation(
            station_id=int(78),
            name='dbcsvmeidpsmnssrtoqi',
            names_fi='vjneyzcuqmsclvvadbxg',
            names_sv='fsqogrvuuilvfrgpltwe',
            names_en='ozzheacmsboowzqedzxo',
            longitude=float(99.51189586662699),
            latitude=float(87.44334418390378),
            altitude=float(13.603522957088543),
            municipality='iguudymcogjcmiuaoqsf',
            municipality_code=int(38),
            province='vrbpujnbphcfkiecnqul',
            province_code=int(80),
            road_number=int(21),
            road_section=int(33),
            distance_from_section_start=int(65),
            carriageway='hxcldezevshppijwwapc',
            side='vwfllwxxtvaouajdqkgl',
            contract_area='lyltjaqgxvywuzaovffx',
            contract_area_code=int(89),
            station_type='evewgehkswpqcbseychn',
            master=False,
            collection_status='szshtupcxdbxmuzchxsd',
            collection_interval=int(72),
            state='xbdnfxfcuyiupuidkicr',
            start_time='ldojsmdekfwjnllbgdmx',
            livi_id='hhigafgikcqgpbjsryiu',
            sensors=[int(71), int(8), int(37)],
            data_updated_time='dgrikboivklmosowneer'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(78)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'dbcsvmeidpsmnssrtoqi'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'vjneyzcuqmsclvvadbxg'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'fsqogrvuuilvfrgpltwe'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'ozzheacmsboowzqedzxo'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(99.51189586662699)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(87.44334418390378)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(13.603522957088543)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'iguudymcogjcmiuaoqsf'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(38)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'vrbpujnbphcfkiecnqul'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(80)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(21)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(33)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(65)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'hxcldezevshppijwwapc'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'vwfllwxxtvaouajdqkgl'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_contract_area_property(self):
        """
        Test contract_area property
        """
        test_value = 'lyltjaqgxvywuzaovffx'
        self.instance.contract_area = test_value
        self.assertEqual(self.instance.contract_area, test_value)
    
    def test_contract_area_code_property(self):
        """
        Test contract_area_code property
        """
        test_value = int(89)
        self.instance.contract_area_code = test_value
        self.assertEqual(self.instance.contract_area_code, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'evewgehkswpqcbseychn'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_master_property(self):
        """
        Test master property
        """
        test_value = False
        self.instance.master = test_value
        self.assertEqual(self.instance.master, test_value)
    
    def test_collection_status_property(self):
        """
        Test collection_status property
        """
        test_value = 'szshtupcxdbxmuzchxsd'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_collection_interval_property(self):
        """
        Test collection_interval property
        """
        test_value = int(72)
        self.instance.collection_interval = test_value
        self.assertEqual(self.instance.collection_interval, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'xbdnfxfcuyiupuidkicr'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'ldojsmdekfwjnllbgdmx'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'hhigafgikcqgpbjsryiu'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(71), int(8), int(37)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'dgrikboivklmosowneer'
        self.instance.data_updated_time = test_value
        self.assertEqual(self.instance.data_updated_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WeatherStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

