"""
Test case for WaterQualityReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from king_county_marine_producer_data.waterqualityreading import WaterQualityReading


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
            station_id='tublnpexyrzspsaxqfst',
            station_name='xitgjjcqwkmeehwmzopq',
            observation_time='ldpfqjuurxsrxpapjeav',
            water_temperature_c=float(89.65096389184995),
            conductivity_s_m=float(1.9407997651795017),
            pressure_dbar=float(56.685835689068696),
            dissolved_oxygen_mg_l=float(56.09791216263967),
            ph=float(13.328003329203419),
            chlorophyll_ug_l=float(36.17557359337435),
            turbidity_ntu=float(61.84827466182596),
            chlorophyll_stddev_ug_l=float(99.08940496853124),
            turbidity_stddev_ntu=float(9.083339953186309),
            salinity_psu=float(61.34525599979717),
            specific_conductivity_s_m=float(41.210401593544034),
            dissolved_oxygen_saturation_pct=float(3.6532277962213144),
            nitrate_umol=float(60.56080965687668),
            nitrate_mg_l=float(23.740589217673282),
            wind_direction_deg=float(41.46516957067495),
            wind_speed_m_s=float(36.343872742320684),
            photosynthetically_active_radiation_umol_s_m2=float(7.493467423099586),
            air_temperature_f=float(73.18740340735278),
            air_humidity_pct=float(89.11720542972023),
            air_pressure_in_hg=float(36.0685800452656),
            system_battery_v=float(45.10171758705025),
            sensor_battery_v=float(37.28448813234388)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'tublnpexyrzspsaxqfst'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'xitgjjcqwkmeehwmzopq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'ldpfqjuurxsrxpapjeav'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_water_temperature_c_property(self):
        """
        Test water_temperature_c property
        """
        test_value = float(89.65096389184995)
        self.instance.water_temperature_c = test_value
        self.assertEqual(self.instance.water_temperature_c, test_value)
    
    def test_conductivity_s_m_property(self):
        """
        Test conductivity_s_m property
        """
        test_value = float(1.9407997651795017)
        self.instance.conductivity_s_m = test_value
        self.assertEqual(self.instance.conductivity_s_m, test_value)
    
    def test_pressure_dbar_property(self):
        """
        Test pressure_dbar property
        """
        test_value = float(56.685835689068696)
        self.instance.pressure_dbar = test_value
        self.assertEqual(self.instance.pressure_dbar, test_value)
    
    def test_dissolved_oxygen_mg_l_property(self):
        """
        Test dissolved_oxygen_mg_l property
        """
        test_value = float(56.09791216263967)
        self.instance.dissolved_oxygen_mg_l = test_value
        self.assertEqual(self.instance.dissolved_oxygen_mg_l, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(13.328003329203419)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_chlorophyll_ug_l_property(self):
        """
        Test chlorophyll_ug_l property
        """
        test_value = float(36.17557359337435)
        self.instance.chlorophyll_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_ug_l, test_value)
    
    def test_turbidity_ntu_property(self):
        """
        Test turbidity_ntu property
        """
        test_value = float(61.84827466182596)
        self.instance.turbidity_ntu = test_value
        self.assertEqual(self.instance.turbidity_ntu, test_value)
    
    def test_chlorophyll_stddev_ug_l_property(self):
        """
        Test chlorophyll_stddev_ug_l property
        """
        test_value = float(99.08940496853124)
        self.instance.chlorophyll_stddev_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_stddev_ug_l, test_value)
    
    def test_turbidity_stddev_ntu_property(self):
        """
        Test turbidity_stddev_ntu property
        """
        test_value = float(9.083339953186309)
        self.instance.turbidity_stddev_ntu = test_value
        self.assertEqual(self.instance.turbidity_stddev_ntu, test_value)
    
    def test_salinity_psu_property(self):
        """
        Test salinity_psu property
        """
        test_value = float(61.34525599979717)
        self.instance.salinity_psu = test_value
        self.assertEqual(self.instance.salinity_psu, test_value)
    
    def test_specific_conductivity_s_m_property(self):
        """
        Test specific_conductivity_s_m property
        """
        test_value = float(41.210401593544034)
        self.instance.specific_conductivity_s_m = test_value
        self.assertEqual(self.instance.specific_conductivity_s_m, test_value)
    
    def test_dissolved_oxygen_saturation_pct_property(self):
        """
        Test dissolved_oxygen_saturation_pct property
        """
        test_value = float(3.6532277962213144)
        self.instance.dissolved_oxygen_saturation_pct = test_value
        self.assertEqual(self.instance.dissolved_oxygen_saturation_pct, test_value)
    
    def test_nitrate_umol_property(self):
        """
        Test nitrate_umol property
        """
        test_value = float(60.56080965687668)
        self.instance.nitrate_umol = test_value
        self.assertEqual(self.instance.nitrate_umol, test_value)
    
    def test_nitrate_mg_l_property(self):
        """
        Test nitrate_mg_l property
        """
        test_value = float(23.740589217673282)
        self.instance.nitrate_mg_l = test_value
        self.assertEqual(self.instance.nitrate_mg_l, test_value)
    
    def test_wind_direction_deg_property(self):
        """
        Test wind_direction_deg property
        """
        test_value = float(41.46516957067495)
        self.instance.wind_direction_deg = test_value
        self.assertEqual(self.instance.wind_direction_deg, test_value)
    
    def test_wind_speed_m_s_property(self):
        """
        Test wind_speed_m_s property
        """
        test_value = float(36.343872742320684)
        self.instance.wind_speed_m_s = test_value
        self.assertEqual(self.instance.wind_speed_m_s, test_value)
    
    def test_photosynthetically_active_radiation_umol_s_m2_property(self):
        """
        Test photosynthetically_active_radiation_umol_s_m2 property
        """
        test_value = float(7.493467423099586)
        self.instance.photosynthetically_active_radiation_umol_s_m2 = test_value
        self.assertEqual(self.instance.photosynthetically_active_radiation_umol_s_m2, test_value)
    
    def test_air_temperature_f_property(self):
        """
        Test air_temperature_f property
        """
        test_value = float(73.18740340735278)
        self.instance.air_temperature_f = test_value
        self.assertEqual(self.instance.air_temperature_f, test_value)
    
    def test_air_humidity_pct_property(self):
        """
        Test air_humidity_pct property
        """
        test_value = float(89.11720542972023)
        self.instance.air_humidity_pct = test_value
        self.assertEqual(self.instance.air_humidity_pct, test_value)
    
    def test_air_pressure_in_hg_property(self):
        """
        Test air_pressure_in_hg property
        """
        test_value = float(36.0685800452656)
        self.instance.air_pressure_in_hg = test_value
        self.assertEqual(self.instance.air_pressure_in_hg, test_value)
    
    def test_system_battery_v_property(self):
        """
        Test system_battery_v property
        """
        test_value = float(45.10171758705025)
        self.instance.system_battery_v = test_value
        self.assertEqual(self.instance.system_battery_v, test_value)
    
    def test_sensor_battery_v_property(self):
        """
        Test sensor_battery_v property
        """
        test_value = float(37.28448813234388)
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

