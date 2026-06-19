"""
Test case for TmsStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_road_producer_data.tmsstation import TmsStation


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
            station_id=int(9),
            name='zhgrnpmfvfwwuxyymtvb',
            tms_number=int(72),
            names_fi='zjynmndfprmjyyhpfrop',
            names_sv='zexkqkowewbhhzvzcghf',
            names_en='sliasrnwvtlewizxqidl',
            longitude=float(28.458619209903702),
            latitude=float(34.04603909285594),
            altitude=float(84.56819044053587),
            municipality='nwglzhfybimbwyonushm',
            municipality_code=int(55),
            province='ugkjrxphaiadykzsctpo',
            province_code=int(83),
            road_number=int(49),
            road_section=int(95),
            distance_from_section_start=int(34),
            carriageway='penfdfpvijcxolimfqpx',
            side='roycigyzlirguqnxfooe',
            station_type='dgihrwofwandrakrupaj',
            collection_status='iayzdkuvbdoerdokjitc',
            state='dbhqfjeqjfojpjbxjerc',
            free_flow_speed_1=float(32.6844406860557),
            free_flow_speed_2=float(98.13409753553664),
            bearing=int(9),
            start_time='phctedswulcuqhhegsyw',
            livi_id='fouiitqvodfxaezdrywi',
            sensors=[int(64), int(40)],
            data_updated_time='pqwpttbiczurraijpmso'
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = int(9)
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'zhgrnpmfvfwwuxyymtvb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_tms_number_property(self):
        """
        Test tms_number property
        """
        test_value = int(72)
        self.instance.tms_number = test_value
        self.assertEqual(self.instance.tms_number, test_value)
    
    def test_names_fi_property(self):
        """
        Test names_fi property
        """
        test_value = 'zjynmndfprmjyyhpfrop'
        self.instance.names_fi = test_value
        self.assertEqual(self.instance.names_fi, test_value)
    
    def test_names_sv_property(self):
        """
        Test names_sv property
        """
        test_value = 'zexkqkowewbhhzvzcghf'
        self.instance.names_sv = test_value
        self.assertEqual(self.instance.names_sv, test_value)
    
    def test_names_en_property(self):
        """
        Test names_en property
        """
        test_value = 'sliasrnwvtlewizxqidl'
        self.instance.names_en = test_value
        self.assertEqual(self.instance.names_en, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(28.458619209903702)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(34.04603909285594)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(84.56819044053587)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_municipality_property(self):
        """
        Test municipality property
        """
        test_value = 'nwglzhfybimbwyonushm'
        self.instance.municipality = test_value
        self.assertEqual(self.instance.municipality, test_value)
    
    def test_municipality_code_property(self):
        """
        Test municipality_code property
        """
        test_value = int(55)
        self.instance.municipality_code = test_value
        self.assertEqual(self.instance.municipality_code, test_value)
    
    def test_province_property(self):
        """
        Test province property
        """
        test_value = 'ugkjrxphaiadykzsctpo'
        self.instance.province = test_value
        self.assertEqual(self.instance.province, test_value)
    
    def test_province_code_property(self):
        """
        Test province_code property
        """
        test_value = int(83)
        self.instance.province_code = test_value
        self.assertEqual(self.instance.province_code, test_value)
    
    def test_road_number_property(self):
        """
        Test road_number property
        """
        test_value = int(49)
        self.instance.road_number = test_value
        self.assertEqual(self.instance.road_number, test_value)
    
    def test_road_section_property(self):
        """
        Test road_section property
        """
        test_value = int(95)
        self.instance.road_section = test_value
        self.assertEqual(self.instance.road_section, test_value)
    
    def test_distance_from_section_start_property(self):
        """
        Test distance_from_section_start property
        """
        test_value = int(34)
        self.instance.distance_from_section_start = test_value
        self.assertEqual(self.instance.distance_from_section_start, test_value)
    
    def test_carriageway_property(self):
        """
        Test carriageway property
        """
        test_value = 'penfdfpvijcxolimfqpx'
        self.instance.carriageway = test_value
        self.assertEqual(self.instance.carriageway, test_value)
    
    def test_side_property(self):
        """
        Test side property
        """
        test_value = 'roycigyzlirguqnxfooe'
        self.instance.side = test_value
        self.assertEqual(self.instance.side, test_value)
    
    def test_station_type_property(self):
        """
        Test station_type property
        """
        test_value = 'dgihrwofwandrakrupaj'
        self.instance.station_type = test_value
        self.assertEqual(self.instance.station_type, test_value)
    
    def test_collection_status_property(self):
        """
        Test collection_status property
        """
        test_value = 'iayzdkuvbdoerdokjitc'
        self.instance.collection_status = test_value
        self.assertEqual(self.instance.collection_status, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'dbhqfjeqjfojpjbxjerc'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_free_flow_speed_1_property(self):
        """
        Test free_flow_speed_1 property
        """
        test_value = float(32.6844406860557)
        self.instance.free_flow_speed_1 = test_value
        self.assertEqual(self.instance.free_flow_speed_1, test_value)
    
    def test_free_flow_speed_2_property(self):
        """
        Test free_flow_speed_2 property
        """
        test_value = float(98.13409753553664)
        self.instance.free_flow_speed_2 = test_value
        self.assertEqual(self.instance.free_flow_speed_2, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = int(9)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'phctedswulcuqhhegsyw'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_livi_id_property(self):
        """
        Test livi_id property
        """
        test_value = 'fouiitqvodfxaezdrywi'
        self.instance.livi_id = test_value
        self.assertEqual(self.instance.livi_id, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = [int(64), int(40)]
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_data_updated_time_property(self):
        """
        Test data_updated_time property
        """
        test_value = 'pqwpttbiczurraijpmso'
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

