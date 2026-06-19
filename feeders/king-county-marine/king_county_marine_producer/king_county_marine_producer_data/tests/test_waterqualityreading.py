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
            station_id='jsazoszlremoiwpwlsjd',
            station_name='yswaheqfpltmyexrwgaq',
            observation_time='qjebnszhcqlodttdxtaf',
            water_temperature_c=float(63.88907720360123),
            conductivity_s_m=float(41.06414096058655),
            pressure_dbar=float(4.559623701768823),
            dissolved_oxygen_mg_l=float(13.126467737185688),
            ph=float(53.23828267294871),
            chlorophyll_ug_l=float(56.20257389390674),
            turbidity_ntu=float(57.87407539227486),
            chlorophyll_stddev_ug_l=float(55.91356641811879),
            turbidity_stddev_ntu=float(45.69481592758473),
            salinity_psu=float(30.36474211098872),
            specific_conductivity_s_m=float(67.76924411893486),
            dissolved_oxygen_saturation_pct=float(14.384613717625182),
            nitrate_umol=float(72.43667503786799),
            nitrate_mg_l=float(31.219651184992646),
            wind_direction_deg=float(92.22890080488439),
            wind_speed_m_s=float(36.807966612500046),
            photosynthetically_active_radiation_umol_s_m2=float(46.23006670877081),
            air_temperature_f=float(4.191305083449304),
            air_humidity_pct=float(3.953808084935384),
            air_pressure_in_hg=float(7.085738430283694),
            system_battery_v=float(64.01240744622058),
            sensor_battery_v=float(37.747183167261454)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'jsazoszlremoiwpwlsjd'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'yswaheqfpltmyexrwgaq'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'qjebnszhcqlodttdxtaf'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_water_temperature_c_property(self):
        """
        Test water_temperature_c property
        """
        test_value = float(63.88907720360123)
        self.instance.water_temperature_c = test_value
        self.assertEqual(self.instance.water_temperature_c, test_value)
    
    def test_conductivity_s_m_property(self):
        """
        Test conductivity_s_m property
        """
        test_value = float(41.06414096058655)
        self.instance.conductivity_s_m = test_value
        self.assertEqual(self.instance.conductivity_s_m, test_value)
    
    def test_pressure_dbar_property(self):
        """
        Test pressure_dbar property
        """
        test_value = float(4.559623701768823)
        self.instance.pressure_dbar = test_value
        self.assertEqual(self.instance.pressure_dbar, test_value)
    
    def test_dissolved_oxygen_mg_l_property(self):
        """
        Test dissolved_oxygen_mg_l property
        """
        test_value = float(13.126467737185688)
        self.instance.dissolved_oxygen_mg_l = test_value
        self.assertEqual(self.instance.dissolved_oxygen_mg_l, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(53.23828267294871)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_chlorophyll_ug_l_property(self):
        """
        Test chlorophyll_ug_l property
        """
        test_value = float(56.20257389390674)
        self.instance.chlorophyll_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_ug_l, test_value)
    
    def test_turbidity_ntu_property(self):
        """
        Test turbidity_ntu property
        """
        test_value = float(57.87407539227486)
        self.instance.turbidity_ntu = test_value
        self.assertEqual(self.instance.turbidity_ntu, test_value)
    
    def test_chlorophyll_stddev_ug_l_property(self):
        """
        Test chlorophyll_stddev_ug_l property
        """
        test_value = float(55.91356641811879)
        self.instance.chlorophyll_stddev_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_stddev_ug_l, test_value)
    
    def test_turbidity_stddev_ntu_property(self):
        """
        Test turbidity_stddev_ntu property
        """
        test_value = float(45.69481592758473)
        self.instance.turbidity_stddev_ntu = test_value
        self.assertEqual(self.instance.turbidity_stddev_ntu, test_value)
    
    def test_salinity_psu_property(self):
        """
        Test salinity_psu property
        """
        test_value = float(30.36474211098872)
        self.instance.salinity_psu = test_value
        self.assertEqual(self.instance.salinity_psu, test_value)
    
    def test_specific_conductivity_s_m_property(self):
        """
        Test specific_conductivity_s_m property
        """
        test_value = float(67.76924411893486)
        self.instance.specific_conductivity_s_m = test_value
        self.assertEqual(self.instance.specific_conductivity_s_m, test_value)
    
    def test_dissolved_oxygen_saturation_pct_property(self):
        """
        Test dissolved_oxygen_saturation_pct property
        """
        test_value = float(14.384613717625182)
        self.instance.dissolved_oxygen_saturation_pct = test_value
        self.assertEqual(self.instance.dissolved_oxygen_saturation_pct, test_value)
    
    def test_nitrate_umol_property(self):
        """
        Test nitrate_umol property
        """
        test_value = float(72.43667503786799)
        self.instance.nitrate_umol = test_value
        self.assertEqual(self.instance.nitrate_umol, test_value)
    
    def test_nitrate_mg_l_property(self):
        """
        Test nitrate_mg_l property
        """
        test_value = float(31.219651184992646)
        self.instance.nitrate_mg_l = test_value
        self.assertEqual(self.instance.nitrate_mg_l, test_value)
    
    def test_wind_direction_deg_property(self):
        """
        Test wind_direction_deg property
        """
        test_value = float(92.22890080488439)
        self.instance.wind_direction_deg = test_value
        self.assertEqual(self.instance.wind_direction_deg, test_value)
    
    def test_wind_speed_m_s_property(self):
        """
        Test wind_speed_m_s property
        """
        test_value = float(36.807966612500046)
        self.instance.wind_speed_m_s = test_value
        self.assertEqual(self.instance.wind_speed_m_s, test_value)
    
    def test_photosynthetically_active_radiation_umol_s_m2_property(self):
        """
        Test photosynthetically_active_radiation_umol_s_m2 property
        """
        test_value = float(46.23006670877081)
        self.instance.photosynthetically_active_radiation_umol_s_m2 = test_value
        self.assertEqual(self.instance.photosynthetically_active_radiation_umol_s_m2, test_value)
    
    def test_air_temperature_f_property(self):
        """
        Test air_temperature_f property
        """
        test_value = float(4.191305083449304)
        self.instance.air_temperature_f = test_value
        self.assertEqual(self.instance.air_temperature_f, test_value)
    
    def test_air_humidity_pct_property(self):
        """
        Test air_humidity_pct property
        """
        test_value = float(3.953808084935384)
        self.instance.air_humidity_pct = test_value
        self.assertEqual(self.instance.air_humidity_pct, test_value)
    
    def test_air_pressure_in_hg_property(self):
        """
        Test air_pressure_in_hg property
        """
        test_value = float(7.085738430283694)
        self.instance.air_pressure_in_hg = test_value
        self.assertEqual(self.instance.air_pressure_in_hg, test_value)
    
    def test_system_battery_v_property(self):
        """
        Test system_battery_v property
        """
        test_value = float(64.01240744622058)
        self.instance.system_battery_v = test_value
        self.assertEqual(self.instance.system_battery_v, test_value)
    
    def test_sensor_battery_v_property(self):
        """
        Test sensor_battery_v property
        """
        test_value = float(37.747183167261454)
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

