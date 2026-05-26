"""
Test case for SensorReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from sensor_community_producer_data.io.sensor.community.sensorreading import SensorReading


class Test_SensorReading(unittest.TestCase):
    """
    Test case for SensorReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_SensorReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of SensorReading for testing
        """
        instance = SensorReading(
            sensor_id=int(90),
            timestamp='yvneiiptprmddheahkwp',
            sensor_type_name='tqxvbgfaclitlysbvyjx',
            pm10_ug_m3=float(40.27054673861492),
            pm2_5_ug_m3=float(39.483500151261396),
            pm1_0_ug_m3=float(50.04608851069903),
            pm4_0_ug_m3=float(51.020802051967884),
            temperature_celsius=float(33.59196397423806),
            humidity_percent=float(73.38623635875157),
            pressure_pa=float(12.0544783152152),
            pressure_sealevel_pa=float(87.78429402787586),
            noise_laeq_db=float(0.9011697823062215),
            noise_la_min_db=float(62.55911139513534),
            noise_la_max_db=float(36.80961417300337)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(90)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'yvneiiptprmddheahkwp'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'tqxvbgfaclitlysbvyjx'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(40.27054673861492)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(39.483500151261396)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_pm1_0_ug_m3_property(self):
        """
        Test pm1_0_ug_m3 property
        """
        test_value = float(50.04608851069903)
        self.instance.pm1_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm1_0_ug_m3, test_value)
    
    def test_pm4_0_ug_m3_property(self):
        """
        Test pm4_0_ug_m3 property
        """
        test_value = float(51.020802051967884)
        self.instance.pm4_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm4_0_ug_m3, test_value)
    
    def test_temperature_celsius_property(self):
        """
        Test temperature_celsius property
        """
        test_value = float(33.59196397423806)
        self.instance.temperature_celsius = test_value
        self.assertEqual(self.instance.temperature_celsius, test_value)
    
    def test_humidity_percent_property(self):
        """
        Test humidity_percent property
        """
        test_value = float(73.38623635875157)
        self.instance.humidity_percent = test_value
        self.assertEqual(self.instance.humidity_percent, test_value)
    
    def test_pressure_pa_property(self):
        """
        Test pressure_pa property
        """
        test_value = float(12.0544783152152)
        self.instance.pressure_pa = test_value
        self.assertEqual(self.instance.pressure_pa, test_value)
    
    def test_pressure_sealevel_pa_property(self):
        """
        Test pressure_sealevel_pa property
        """
        test_value = float(87.78429402787586)
        self.instance.pressure_sealevel_pa = test_value
        self.assertEqual(self.instance.pressure_sealevel_pa, test_value)
    
    def test_noise_laeq_db_property(self):
        """
        Test noise_laeq_db property
        """
        test_value = float(0.9011697823062215)
        self.instance.noise_laeq_db = test_value
        self.assertEqual(self.instance.noise_laeq_db, test_value)
    
    def test_noise_la_min_db_property(self):
        """
        Test noise_la_min_db property
        """
        test_value = float(62.55911139513534)
        self.instance.noise_la_min_db = test_value
        self.assertEqual(self.instance.noise_la_min_db, test_value)
    
    def test_noise_la_max_db_property(self):
        """
        Test noise_la_max_db property
        """
        test_value = float(36.80961417300337)
        self.instance.noise_la_max_db = test_value
        self.assertEqual(self.instance.noise_la_max_db, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SensorReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
