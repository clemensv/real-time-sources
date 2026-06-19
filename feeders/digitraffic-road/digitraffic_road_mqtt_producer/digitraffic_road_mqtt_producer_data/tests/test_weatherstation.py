"""
Test case for WeatherStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_mqtt_producer_data.weatherstation import WeatherStation


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
            name='krggakehjeqgkfeioejv',
            names_fi='dhfspzbcsghojocemgkx',
            names_sv='cqkpjqajlkizujytmyfw',
            names_en='hvydgovbsgvdbywiroew',
            longitude=float(72.39224119612975),
            latitude=float(99.78398850097209),
            altitude=float(21.20282882926047),
            municipality='rcqqasnrxirqctbqlckd',
            municipality_code=int(95),
            province='rxxpovbgekcsniogywae',
            province_code=int(86),
            road_number=int(28),
            road_section=int(10),
            distance_from_section_start=int(66),
            carriageway='joogoymvtbfopfpgsash',
            side='ojufpqfulmunirtcuomx',
            contract_area='cazxbcaflnpernwfghhv',
            contract_area_code=int(81),
            station_type='trzxauyuolazishvvnyt',
            master=True,
            collection_status='degfpnwhohgeldcktkkf',
            collection_interval=int(92),
            state='gyuvdpcfhntdvsytrkcq',
            start_time='twvuihctqdqvlxhfuieu',
            livi_id='xvlydiiowsffdttabusl',
            sensors=[int(89)],
            data_updated_time='pjuvufgssywrqqqgijxg'
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
        test_value = 'krggakehjeqgkfeioejv'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'dhfspzbcsghojocemgkx'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'cqkpjqajlkizujytmyfw'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'hvydgovbsgvdbywiroew'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(72.39224119612975)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(99.78398850097209)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(21.20282882926047)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'rcqqasnrxirqctbqlckd'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(95)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'rxxpovbgekcsniogywae'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(86)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(28)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(10)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(66)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'joogoymvtbfopfpgsash'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'ojufpqfulmunirtcuomx'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_contract_area_property(self):
        """
        Test contract_area property
        """
        test_value = 'cazxbcaflnpernwfghhv'
        self.instance.contract_area = test_value
        self.assertEqual(self.instance.contract_area, test_value)
    
    def test_contract_area_code_property(self):
        """
        Test contract_area_code property
        """
        test_value = int(81)
        self.instance.contract_area_code = test_value
        self.assertEqual(self.instance.contract_area_code, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'trzxauyuolazishvvnyt'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_master_property(self):
        """
        Test master property
        """
        test_value = True
        self.instance.master = test_value
        self.assertEqual(self.instance.master, test_value)
    
    def test_collection_status_property(self):
        """
        Test collection_status property
        """
        test_value = 'degfpnwhohgeldcktkkf'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_collection_interval_property(self):
        """
        Test collection_interval property
        """
        test_value = int(92)
        self.instance.collection_interval = test_value
        self.assertEqual(self.instance.collection_interval, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'gyuvdpcfhntdvsytrkcq'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'twvuihctqdqvlxhfuieu'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'xvlydiiowsffdttabusl'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(89)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'pjuvufgssywrqqqgijxg'
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

