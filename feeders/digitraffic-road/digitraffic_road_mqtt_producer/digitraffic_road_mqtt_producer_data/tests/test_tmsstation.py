"""
Test case for TmsStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_mqtt_producer_data.tmsstation import TmsStation


class Test_TmsStation(unittest.TestCase):
    """
    Test case for TmsStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TmsStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TmsStation for testing
        """
        instance = TmsStation(
            station_id=int(3),
            name='rypoiodeljuxlpzlsoyg',
            tms_number=int(3),
            names_fi='ccmuysratxqxjqgzddqm',
            names_sv='huvhsiaojbdgcivtrglb',
            names_en='pvgwpvemdqqaiqvliogd',
            longitude=float(55.26916410746641),
            latitude=float(74.42860198936894),
            altitude=float(29.347223182889735),
            municipality='cccyzcsjnnrhnrkzczwq',
            municipality_code=int(8),
            province='ynakjezhqklicmzdmvfb',
            province_code=int(93),
            road_number=int(41),
            road_section=int(14),
            distance_from_section_start=int(30),
            carriageway='dkzvoaxvdmdisljejjnc',
            side='ffjzsbfdbpklksjqyhia',
            station_type='scvzjghjfriuchsksapx',
            collection_status='teqmpuodvacroggqkkyz',
            state='loftrmsgxnbwxlaayylz',
            free_flow_speed_1=float(23.29801963281244),
            free_flow_speed_2=float(82.80909023699681),
            bearing=int(28),
            start_time='kcglqifxfmmhcvnnesmf',
            livi_id='flbsuurycmldxhfkzuou',
            sensors=[int(8), int(67), int(24), int(25), int(72)],
            data_updated_time='myhtaslqmxvjpjylttxk'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(3)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'rypoiodeljuxlpzlsoyg'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_tms_number_property(self):
        """
        Test tms_number property
        """
        test_value = int(3)
        self.instance.tms_number = test_value
        self.assertEqual(self.instance.tms_number, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'ccmuysratxqxjqgzddqm'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'huvhsiaojbdgcivtrglb'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'pvgwpvemdqqaiqvliogd'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(55.26916410746641)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(74.42860198936894)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(29.347223182889735)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'cccyzcsjnnrhnrkzczwq'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(8)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'ynakjezhqklicmzdmvfb'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(93)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(41)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(14)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(30)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'dkzvoaxvdmdisljejjnc'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'ffjzsbfdbpklksjqyhia'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'scvzjghjfriuchsksapx'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_collection_status_property(self):
        """
        Test collection_status property
        """
        test_value = 'teqmpuodvacroggqkkyz'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'loftrmsgxnbwxlaayylz'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_free_flow_speed_1_property(self):
        """
        Test free_flow_speed_1 property
        """
        test_value = float(23.29801963281244)
        self.instance.free_flow_speed_1 = test_value
        self.assertEqual(self.instance.free_flow_speed_1, test_value)
    
    def test_free_flow_speed_2_property(self):
        """
        Test free_flow_speed_2 property
        """
        test_value = float(82.80909023699681)
        self.instance.free_flow_speed_2 = test_value
        self.assertEqual(self.instance.free_flow_speed_2, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(28)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'kcglqifxfmmhcvnnesmf'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'flbsuurycmldxhfkzuou'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(8), int(67), int(24), int(25), int(72)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'myhtaslqmxvjpjylttxk'
        self.instance.data_updated_time = test_value
        self.assertEqual(self.instance.data_updated_time, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TmsStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TmsStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

