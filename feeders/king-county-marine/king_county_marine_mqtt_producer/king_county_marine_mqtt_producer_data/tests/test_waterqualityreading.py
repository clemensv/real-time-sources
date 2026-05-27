"""
Test case for WaterQualityReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from king_county_marine_mqtt_producer_data.waterqualityreading import WaterQualityReading


class Test_WaterQualityReading(unittest.TestCase):
    """
    Test case for WaterQualityReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterQualityReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterQualityReading for testing
        """
        instance = WaterQualityReading(
            station_id='mwfditawtuajdjwzomli',
            station_name='hgdbjgegbnhnoihpytsk',
            observation_time='abqtwbktzvlewovgeeqe',
            water_temperature_c=float(99.17724721847311),
            conductivity_s_m=float(30.788921957826567),
            pressure_dbar=float(78.65130504456988),
            dissolved_oxygen_mg_l=float(68.19895002954627),
            ph=float(27.07903907158309),
            chlorophyll_ug_l=float(42.85501216570024),
            turbidity_ntu=float(15.038937810517206),
            chlorophyll_stddev_ug_l=float(61.532712221052186),
            turbidity_stddev_ntu=float(70.03270595681929),
            salinity_psu=float(35.92990605671324),
            specific_conductivity_s_m=float(8.601621586916297),
            dissolved_oxygen_saturation_pct=float(81.73995353268235),
            nitrate_umol=float(36.41455674240237),
            nitrate_mg_l=float(82.36403986423724),
            wind_direction_deg=float(75.1110051620823),
            wind_speed_m_s=float(0.6623360917644927),
            photosynthetically_active_radiation_umol_s_m2=float(18.780990756627215),
            air_temperature_f=float(51.235489691836236),
            air_humidity_pct=float(18.41430019767255),
            air_pressure_in_hg=float(32.3678708742918),
            system_battery_v=float(74.4155417701577),
            sensor_battery_v=float(24.85128644420348)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'mwfditawtuajdjwzomli'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'hgdbjgegbnhnoihpytsk'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'abqtwbktzvlewovgeeqe'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_water_temperature_c_property(self):
        """
        Test water_temperature_c property
        """
        test_value = float(99.17724721847311)
        self.instance.water_temperature_c = test_value
        self.assertEqual(self.instance.water_temperature_c, test_value)
    
    def test_conductivity_s_m_property(self):
        """
        Test conductivity_s_m property
        """
        test_value = float(30.788921957826567)
        self.instance.conductivity_s_m = test_value
        self.assertEqual(self.instance.conductivity_s_m, test_value)
    
    def test_pressure_dbar_property(self):
        """
        Test pressure_dbar property
        """
        test_value = float(78.65130504456988)
        self.instance.pressure_dbar = test_value
        self.assertEqual(self.instance.pressure_dbar, test_value)
    
    def test_dissolved_oxygen_mg_l_property(self):
        """
        Test dissolved_oxygen_mg_l property
        """
        test_value = float(68.19895002954627)
        self.instance.dissolved_oxygen_mg_l = test_value
        self.assertEqual(self.instance.dissolved_oxygen_mg_l, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(27.07903907158309)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_chlorophyll_ug_l_property(self):
        """
        Test chlorophyll_ug_l property
        """
        test_value = float(42.85501216570024)
        self.instance.chlorophyll_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_ug_l, test_value)
    
    def test_turbidity_ntu_property(self):
        """
        Test turbidity_ntu property
        """
        test_value = float(15.038937810517206)
        self.instance.turbidity_ntu = test_value
        self.assertEqual(self.instance.turbidity_ntu, test_value)
    
    def test_chlorophyll_stddev_ug_l_property(self):
        """
        Test chlorophyll_stddev_ug_l property
        """
        test_value = float(61.532712221052186)
        self.instance.chlorophyll_stddev_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_stddev_ug_l, test_value)
    
    def test_turbidity_stddev_ntu_property(self):
        """
        Test turbidity_stddev_ntu property
        """
        test_value = float(70.03270595681929)
        self.instance.turbidity_stddev_ntu = test_value
        self.assertEqual(self.instance.turbidity_stddev_ntu, test_value)
    
    def test_salinity_psu_property(self):
        """
        Test salinity_psu property
        """
        test_value = float(35.92990605671324)
        self.instance.salinity_psu = test_value
        self.assertEqual(self.instance.salinity_psu, test_value)
    
    def test_specific_conductivity_s_m_property(self):
        """
        Test specific_conductivity_s_m property
        """
        test_value = float(8.601621586916297)
        self.instance.specific_conductivity_s_m = test_value
        self.assertEqual(self.instance.specific_conductivity_s_m, test_value)
    
    def test_dissolved_oxygen_saturation_pct_property(self):
        """
        Test dissolved_oxygen_saturation_pct property
        """
        test_value = float(81.73995353268235)
        self.instance.dissolved_oxygen_saturation_pct = test_value
        self.assertEqual(self.instance.dissolved_oxygen_saturation_pct, test_value)
    
    def test_nitrate_umol_property(self):
        """
        Test nitrate_umol property
        """
        test_value = float(36.41455674240237)
        self.instance.nitrate_umol = test_value
        self.assertEqual(self.instance.nitrate_umol, test_value)
    
    def test_nitrate_mg_l_property(self):
        """
        Test nitrate_mg_l property
        """
        test_value = float(82.36403986423724)
        self.instance.nitrate_mg_l = test_value
        self.assertEqual(self.instance.nitrate_mg_l, test_value)
    
    def test_wind_direction_deg_property(self):
        """
        Test wind_direction_deg property
        """
        test_value = float(75.1110051620823)
        self.instance.wind_direction_deg = test_value
        self.assertEqual(self.instance.wind_direction_deg, test_value)
    
    def test_wind_speed_m_s_property(self):
        """
        Test wind_speed_m_s property
        """
        test_value = float(0.6623360917644927)
        self.instance.wind_speed_m_s = test_value
        self.assertEqual(self.instance.wind_speed_m_s, test_value)
    
    def test_photosynthetically_active_radiation_umol_s_m2_property(self):
        """
        Test photosynthetically_active_radiation_umol_s_m2 property
        """
        test_value = float(18.780990756627215)
        self.instance.photosynthetically_active_radiation_umol_s_m2 = test_value
        self.assertEqual(self.instance.photosynthetically_active_radiation_umol_s_m2, test_value)
    
    def test_air_temperature_f_property(self):
        """
        Test air_temperature_f property
        """
        test_value = float(51.235489691836236)
        self.instance.air_temperature_f = test_value
        self.assertEqual(self.instance.air_temperature_f, test_value)
    
    def test_air_humidity_pct_property(self):
        """
        Test air_humidity_pct property
        """
        test_value = float(18.41430019767255)
        self.instance.air_humidity_pct = test_value
        self.assertEqual(self.instance.air_humidity_pct, test_value)
    
    def test_air_pressure_in_hg_property(self):
        """
        Test air_pressure_in_hg property
        """
        test_value = float(32.3678708742918)
        self.instance.air_pressure_in_hg = test_value
        self.assertEqual(self.instance.air_pressure_in_hg, test_value)
    
    def test_system_battery_v_property(self):
        """
        Test system_battery_v property
        """
        test_value = float(74.4155417701577)
        self.instance.system_battery_v = test_value
        self.assertEqual(self.instance.system_battery_v, test_value)
    
    def test_sensor_battery_v_property(self):
        """
        Test sensor_battery_v property
        """
        test_value = float(24.85128644420348)
        self.instance.sensor_battery_v = test_value
        self.assertEqual(self.instance.sensor_battery_v, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterQualityReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterQualityReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

