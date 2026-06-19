"""
Test case for WeatherStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_amqp_producer_data.weatherstation import WeatherStation


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
            station_id=int(72),
            name='ihlzemzeclfjcjrqkjbp',
            names_fi='bstcbprqmwmwjptgsknz',
            names_sv='ixyneylbiaslkedofwnh',
            names_en='dwqzbbnrdmthcerwhhco',
            longitude=float(87.32551747233703),
            latitude=float(19.092461666647566),
            altitude=float(74.99911999616953),
            municipality='oouaufewdbawjcyqvplk',
            municipality_code=int(41),
            province='ssbhbaltrhqnwboufjyu',
            province_code=int(19),
            road_number=int(36),
            road_section=int(84),
            distance_from_section_start=int(97),
            carriageway='pacnfojprpdbqttnqadf',
            side='vqhmlalkrqgheyrhgxqv',
            contract_area='fwrlappnjjokckvssghu',
            contract_area_code=int(47),
            station_type='kibayolbgakupdlfgswp',
            master=False,
            collection_status='sdpghmkandrselkubsjm',
            collection_interval=int(21),
            state='jptmgxuqfhsdbwwcwgsr',
            start_time='fbctxmmxdmhalncolrjo',
            livi_id='jqqkrfsarptijkpxaemz',
            sensors=[int(71), int(44)],
            data_updated_time='jvmzavrohlkglmrdfshw'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(72)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ihlzemzeclfjcjrqkjbp'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'bstcbprqmwmwjptgsknz'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'ixyneylbiaslkedofwnh'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'dwqzbbnrdmthcerwhhco'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(87.32551747233703)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(19.092461666647566)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(74.99911999616953)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'oouaufewdbawjcyqvplk'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(41)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'ssbhbaltrhqnwboufjyu'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(19)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(36)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(84)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(97)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'pacnfojprpdbqttnqadf'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'vqhmlalkrqgheyrhgxqv'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_contract_area_property(self):
        """
        Test contract_area property
        """
        test_value = 'fwrlappnjjokckvssghu'
        self.instance.contract_area = test_value
        self.assertEqual(self.instance.contract_area, test_value)
    
    def test_contract_area_code_property(self):
        """
        Test contract_area_code property
        """
        test_value = int(47)
        self.instance.contract_area_code = test_value
        self.assertEqual(self.instance.contract_area_code, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'kibayolbgakupdlfgswp'
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
        test_value = 'sdpghmkandrselkubsjm'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_collection_interval_property(self):
        """
        Test collection_interval property
        """
        test_value = int(21)
        self.instance.collection_interval = test_value
        self.assertEqual(self.instance.collection_interval, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'jptmgxuqfhsdbwwcwgsr'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'fbctxmmxdmhalncolrjo'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'jqqkrfsarptijkpxaemz'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(71), int(44)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'jvmzavrohlkglmrdfshw'
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

