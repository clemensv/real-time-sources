"""
Test case for SensorReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from sensor_community_mqtt_producer_data.io.sensor.community.sensorreading import SensorReading


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
            sensor_id=int(12),
            timestamp='nlpignkmpjhoqikpujpf',
            sensor_type_name='ixusntgwaijjexslmgos',
            pm10_ug_m3=float(52.99270954678435),
            pm2_5_ug_m3=float(60.11259739652321),
            pm1_0_ug_m3=float(35.571418406686576),
            pm4_0_ug_m3=float(71.3999194363422),
            temperature_celsius=float(56.595226952495956),
            humidity_percent=float(51.04699028687206),
            pressure_pa=float(84.52506560176158),
            pressure_sealevel_pa=float(42.44491680116246),
            noise_laeq_db=float(17.91672926222284),
            noise_la_min_db=float(0.316112963550097),
            noise_la_max_db=float(84.38385808634455)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(12)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'nlpignkmpjhoqikpujpf'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'ixusntgwaijjexslmgos'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(52.99270954678435)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(60.11259739652321)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_pm1_0_ug_m3_property(self):
        """
        Test pm1_0_ug_m3 property
        """
        test_value = float(35.571418406686576)
        self.instance.pm1_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm1_0_ug_m3, test_value)
    
    def test_pm4_0_ug_m3_property(self):
        """
        Test pm4_0_ug_m3 property
        """
        test_value = float(71.3999194363422)
        self.instance.pm4_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm4_0_ug_m3, test_value)
    
    def test_temperature_celsius_property(self):
        """
        Test temperature_celsius property
        """
        test_value = float(56.595226952495956)
        self.instance.temperature_celsius = test_value
        self.assertEqual(self.instance.temperature_celsius, test_value)
    
    def test_humidity_percent_property(self):
        """
        Test humidity_percent property
        """
        test_value = float(51.04699028687206)
        self.instance.humidity_percent = test_value
        self.assertEqual(self.instance.humidity_percent, test_value)
    
    def test_pressure_pa_property(self):
        """
        Test pressure_pa property
        """
        test_value = float(84.52506560176158)
        self.instance.pressure_pa = test_value
        self.assertEqual(self.instance.pressure_pa, test_value)
    
    def test_pressure_sealevel_pa_property(self):
        """
        Test pressure_sealevel_pa property
        """
        test_value = float(42.44491680116246)
        self.instance.pressure_sealevel_pa = test_value
        self.assertEqual(self.instance.pressure_sealevel_pa, test_value)
    
    def test_noise_laeq_db_property(self):
        """
        Test noise_laeq_db property
        """
        test_value = float(17.91672926222284)
        self.instance.noise_laeq_db = test_value
        self.assertEqual(self.instance.noise_laeq_db, test_value)
    
    def test_noise_la_min_db_property(self):
        """
        Test noise_la_min_db property
        """
        test_value = float(0.316112963550097)
        self.instance.noise_la_min_db = test_value
        self.assertEqual(self.instance.noise_la_min_db, test_value)
    
    def test_noise_la_max_db_property(self):
        """
        Test noise_la_max_db property
        """
        test_value = float(84.38385808634455)
        self.instance.noise_la_max_db = test_value
        self.assertEqual(self.instance.noise_la_max_db, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = SensorReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = SensorReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

