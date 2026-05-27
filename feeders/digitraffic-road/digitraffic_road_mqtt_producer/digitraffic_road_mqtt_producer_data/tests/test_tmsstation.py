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
            station_id=int(35),
            name='mgzguqpkdqayaxrptsyd',
            tms_number=int(71),
            names_fi='tutbiebbawmslokczpae',
            names_sv='svsikbjsqarkoefvqcww',
            names_en='vprhkajmbkolhjzqaenp',
            longitude=float(52.43042515998687),
            latitude=float(63.45769766918943),
            altitude=float(56.64742729965633),
            municipality='wyxtvadbcwgetylpxhbg',
            municipality_code=int(84),
            province='dtgwueixntfvzwcnhbur',
            province_code=int(13),
            road_number=int(89),
            road_section=int(11),
            distance_from_section_start=int(92),
            carriageway='gfotahafccpyxswwtmko',
            side='qailqazzkoaludvybtig',
            station_type='oilmoojjcdrxpcmsomqj',
            collection_status='zemuzaknadhhjtudeppw',
            state='neaqsguhanxeruevcgxz',
            free_flow_speed_1=float(38.49016632673118),
            free_flow_speed_2=float(73.58898758677358),
            bearing=int(89),
            start_time='njdjejdakjwkbzjivrji',
            livi_id='nskookymlqwxwzopimde',
            sensors=[int(25), int(29), int(23)],
            data_updated_time='sgdpvnejjcbyfnnfbhxr'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(35)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'mgzguqpkdqayaxrptsyd'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_tms_number_property(self):
        """
        Test tms_number property
        """
        test_value = int(71)
        self.instance.tms_number = test_value
        self.assertEqual(self.instance.tms_number, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'tutbiebbawmslokczpae'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'svsikbjsqarkoefvqcww'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'vprhkajmbkolhjzqaenp'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(52.43042515998687)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(63.45769766918943)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(56.64742729965633)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'wyxtvadbcwgetylpxhbg'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(84)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'dtgwueixntfvzwcnhbur'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(13)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(89)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(11)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(92)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'gfotahafccpyxswwtmko'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'qailqazzkoaludvybtig'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'oilmoojjcdrxpcmsomqj'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_collection_status_property(self):
        """
        Test collection_status property
        """
        test_value = 'zemuzaknadhhjtudeppw'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'neaqsguhanxeruevcgxz'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_free_flow_speed_1_property(self):
        """
        Test free_flow_speed_1 property
        """
        test_value = float(38.49016632673118)
        self.instance.free_flow_speed_1 = test_value
        self.assertEqual(self.instance.free_flow_speed_1, test_value)
    
    def test_free_flow_speed_2_property(self):
        """
        Test free_flow_speed_2 property
        """
        test_value = float(73.58898758677358)
        self.instance.free_flow_speed_2 = test_value
        self.assertEqual(self.instance.free_flow_speed_2, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(89)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'njdjejdakjwkbzjivrji'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'nskookymlqwxwzopimde'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(25), int(29), int(23)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'sgdpvnejjcbyfnnfbhxr'
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

