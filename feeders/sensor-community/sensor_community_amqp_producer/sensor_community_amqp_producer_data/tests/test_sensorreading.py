"""
Test case for SensorReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from sensor_community_amqp_producer_data.io.sensor.community.sensorreading import SensorReading


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
            sensor_id=int(4),
            timestamp='zydinauddogdkvurqxfq',
            sensor_type_name='dwmjrwywplutaiczommp',
            pm10_ug_m3=float(76.33174760866522),
            pm2_5_ug_m3=float(86.07034131104703),
            pm1_0_ug_m3=float(67.77758935963165),
            pm4_0_ug_m3=float(6.224155356943117),
            temperature_celsius=float(83.42221648006637),
            humidity_percent=float(69.3208239680613),
            pressure_pa=float(70.09384011492409),
            pressure_sealevel_pa=float(28.9864158500269),
            noise_laeq_db=float(45.279416165030916),
            noise_la_min_db=float(34.24223515786061),
            noise_la_max_db=float(16.346075232901224)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(4)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'zydinauddogdkvurqxfq'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'dwmjrwywplutaiczommp'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(76.33174760866522)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(86.07034131104703)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_pm1_0_ug_m3_property(self):
        """
        Test pm1_0_ug_m3 property
        """
        test_value = float(67.77758935963165)
        self.instance.pm1_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm1_0_ug_m3, test_value)
    
    def test_pm4_0_ug_m3_property(self):
        """
        Test pm4_0_ug_m3 property
        """
        test_value = float(6.224155356943117)
        self.instance.pm4_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm4_0_ug_m3, test_value)
    
    def test_temperature_celsius_property(self):
        """
        Test temperature_celsius property
        """
        test_value = float(83.42221648006637)
        self.instance.temperature_celsius = test_value
        self.assertEqual(self.instance.temperature_celsius, test_value)
    
    def test_humidity_percent_property(self):
        """
        Test humidity_percent property
        """
        test_value = float(69.3208239680613)
        self.instance.humidity_percent = test_value
        self.assertEqual(self.instance.humidity_percent, test_value)
    
    def test_pressure_pa_property(self):
        """
        Test pressure_pa property
        """
        test_value = float(70.09384011492409)
        self.instance.pressure_pa = test_value
        self.assertEqual(self.instance.pressure_pa, test_value)
    
    def test_pressure_sealevel_pa_property(self):
        """
        Test pressure_sealevel_pa property
        """
        test_value = float(28.9864158500269)
        self.instance.pressure_sealevel_pa = test_value
        self.assertEqual(self.instance.pressure_sealevel_pa, test_value)
    
    def test_noise_laeq_db_property(self):
        """
        Test noise_laeq_db property
        """
        test_value = float(45.279416165030916)
        self.instance.noise_laeq_db = test_value
        self.assertEqual(self.instance.noise_laeq_db, test_value)
    
    def test_noise_la_min_db_property(self):
        """
        Test noise_la_min_db property
        """
        test_value = float(34.24223515786061)
        self.instance.noise_la_min_db = test_value
        self.assertEqual(self.instance.noise_la_min_db, test_value)
    
    def test_noise_la_max_db_property(self):
        """
        Test noise_la_max_db property
        """
        test_value = float(16.346075232901224)
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

