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
            sensor_id=int(85),
            timestamp='tiihnezvcozqyvpsbsvg',
            sensor_type_name='xlvmmafylnybiksohmmx',
            pm10_ug_m3=float(37.24290410668114),
            pm2_5_ug_m3=float(18.788230767604453),
            pm1_0_ug_m3=float(87.15876545625201),
            pm4_0_ug_m3=float(93.11095035254014),
            temperature_celsius=float(94.84106795950039),
            humidity_percent=float(27.241353137450975),
            pressure_pa=float(69.77641029917724),
            pressure_sealevel_pa=float(42.30934860852271),
            noise_laeq_db=float(36.90053034159596),
            noise_la_min_db=float(72.03629743718973),
            noise_la_max_db=float(13.872311736200515)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(85)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'tiihnezvcozqyvpsbsvg'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'xlvmmafylnybiksohmmx'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(37.24290410668114)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(18.788230767604453)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_pm1_0_ug_m3_property(self):
        """
        Test pm1_0_ug_m3 property
        """
        test_value = float(87.15876545625201)
        self.instance.pm1_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm1_0_ug_m3, test_value)
    
    def test_pm4_0_ug_m3_property(self):
        """
        Test pm4_0_ug_m3 property
        """
        test_value = float(93.11095035254014)
        self.instance.pm4_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm4_0_ug_m3, test_value)
    
    def test_temperature_celsius_property(self):
        """
        Test temperature_celsius property
        """
        test_value = float(94.84106795950039)
        self.instance.temperature_celsius = test_value
        self.assertEqual(self.instance.temperature_celsius, test_value)
    
    def test_humidity_percent_property(self):
        """
        Test humidity_percent property
        """
        test_value = float(27.241353137450975)
        self.instance.humidity_percent = test_value
        self.assertEqual(self.instance.humidity_percent, test_value)
    
    def test_pressure_pa_property(self):
        """
        Test pressure_pa property
        """
        test_value = float(69.77641029917724)
        self.instance.pressure_pa = test_value
        self.assertEqual(self.instance.pressure_pa, test_value)
    
    def test_pressure_sealevel_pa_property(self):
        """
        Test pressure_sealevel_pa property
        """
        test_value = float(42.30934860852271)
        self.instance.pressure_sealevel_pa = test_value
        self.assertEqual(self.instance.pressure_sealevel_pa, test_value)
    
    def test_noise_laeq_db_property(self):
        """
        Test noise_laeq_db property
        """
        test_value = float(36.90053034159596)
        self.instance.noise_laeq_db = test_value
        self.assertEqual(self.instance.noise_laeq_db, test_value)
    
    def test_noise_la_min_db_property(self):
        """
        Test noise_la_min_db property
        """
        test_value = float(72.03629743718973)
        self.instance.noise_la_min_db = test_value
        self.assertEqual(self.instance.noise_la_min_db, test_value)
    
    def test_noise_la_max_db_property(self):
        """
        Test noise_la_max_db property
        """
        test_value = float(13.872311736200515)
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

