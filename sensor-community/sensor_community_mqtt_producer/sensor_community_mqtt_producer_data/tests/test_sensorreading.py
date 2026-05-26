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
            sensor_id=int(2),
            timestamp='qqtpshwhltahebudarkb',
            sensor_type_name='publzvkhvwytltyxrqai',
            pm10_ug_m3=float(33.755339014989026),
            pm2_5_ug_m3=float(84.095951246011),
            pm1_0_ug_m3=float(33.600040045365375),
            pm4_0_ug_m3=float(81.07258413037425),
            temperature_celsius=float(60.36022476479885),
            humidity_percent=float(86.2108947244489),
            pressure_pa=float(65.19667270860711),
            pressure_sealevel_pa=float(28.743757110745662),
            noise_laeq_db=float(45.090203455833446),
            noise_la_min_db=float(98.42121512232839),
            noise_la_max_db=float(68.37681598752475)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = int(2)
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'qqtpshwhltahebudarkb'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_sensor_type_name_property(self):
        """
        Test sensor_type_name property
        """
        test_value = 'publzvkhvwytltyxrqai'
        self.instance.sensor_type_name = test_value
        self.assertEqual(self.instance.sensor_type_name, test_value)
    
    def test_pm10_ug_m3_property(self):
        """
        Test pm10_ug_m3 property
        """
        test_value = float(33.755339014989026)
        self.instance.pm10_ug_m3 = test_value
        self.assertEqual(self.instance.pm10_ug_m3, test_value)
    
    def test_pm2_5_ug_m3_property(self):
        """
        Test pm2_5_ug_m3 property
        """
        test_value = float(84.095951246011)
        self.instance.pm2_5_ug_m3 = test_value
        self.assertEqual(self.instance.pm2_5_ug_m3, test_value)
    
    def test_pm1_0_ug_m3_property(self):
        """
        Test pm1_0_ug_m3 property
        """
        test_value = float(33.600040045365375)
        self.instance.pm1_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm1_0_ug_m3, test_value)
    
    def test_pm4_0_ug_m3_property(self):
        """
        Test pm4_0_ug_m3 property
        """
        test_value = float(81.07258413037425)
        self.instance.pm4_0_ug_m3 = test_value
        self.assertEqual(self.instance.pm4_0_ug_m3, test_value)
    
    def test_temperature_celsius_property(self):
        """
        Test temperature_celsius property
        """
        test_value = float(60.36022476479885)
        self.instance.temperature_celsius = test_value
        self.assertEqual(self.instance.temperature_celsius, test_value)
    
    def test_humidity_percent_property(self):
        """
        Test humidity_percent property
        """
        test_value = float(86.2108947244489)
        self.instance.humidity_percent = test_value
        self.assertEqual(self.instance.humidity_percent, test_value)
    
    def test_pressure_pa_property(self):
        """
        Test pressure_pa property
        """
        test_value = float(65.19667270860711)
        self.instance.pressure_pa = test_value
        self.assertEqual(self.instance.pressure_pa, test_value)
    
    def test_pressure_sealevel_pa_property(self):
        """
        Test pressure_sealevel_pa property
        """
        test_value = float(28.743757110745662)
        self.instance.pressure_sealevel_pa = test_value
        self.assertEqual(self.instance.pressure_sealevel_pa, test_value)
    
    def test_noise_laeq_db_property(self):
        """
        Test noise_laeq_db property
        """
        test_value = float(45.090203455833446)
        self.instance.noise_laeq_db = test_value
        self.assertEqual(self.instance.noise_laeq_db, test_value)
    
    def test_noise_la_min_db_property(self):
        """
        Test noise_la_min_db property
        """
        test_value = float(98.42121512232839)
        self.instance.noise_la_min_db = test_value
        self.assertEqual(self.instance.noise_la_min_db, test_value)
    
    def test_noise_la_max_db_property(self):
        """
        Test noise_la_max_db property
        """
        test_value = float(68.37681598752475)
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

