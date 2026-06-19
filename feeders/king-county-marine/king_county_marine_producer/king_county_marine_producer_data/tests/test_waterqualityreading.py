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
            station_id='eolizrvuxduszziypcpi',
            station_name='bpmckhwigbnixvqnicgk',
            observation_time='ezgsfzjgcvipofuyckvr',
            water_temperature_c=float(83.20013880693129),
            conductivity_s_m=float(15.252193908068602),
            pressure_dbar=float(1.7490051392557215),
            dissolved_oxygen_mg_l=float(25.362444989014364),
            ph=float(96.21252102202052),
            chlorophyll_ug_l=float(3.50564372293789),
            turbidity_ntu=float(24.604901100939603),
            chlorophyll_stddev_ug_l=float(40.86359363552465),
            turbidity_stddev_ntu=float(30.568154494280154),
            salinity_psu=float(80.87806898240345),
            specific_conductivity_s_m=float(76.56177340943164),
            dissolved_oxygen_saturation_pct=float(23.97136638609787),
            nitrate_umol=float(31.89466467815124),
            nitrate_mg_l=float(1.6000451469877053),
            wind_direction_deg=float(94.88054220563842),
            wind_speed_m_s=float(88.14593872994645),
            photosynthetically_active_radiation_umol_s_m2=float(28.48487337148423),
            air_temperature_f=float(88.5686037903205),
            air_humidity_pct=float(74.97334508476466),
            air_pressure_in_hg=float(23.621856216901193),
            system_battery_v=float(9.341708064057775),
            sensor_battery_v=float(64.26388992199789)
        )
        return instance

    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'eolizrvuxduszziypcpi'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_station_name_property(self):
        """
        Test station_name property
        """
        test_value = 'bpmckhwigbnixvqnicgk'
        self.instance.station_name = test_value
        self.assertEqual(self.instance.station_name, test_value)
    
    def test_observation_time_property(self):
        """
        Test observation_time property
        """
        test_value = 'ezgsfzjgcvipofuyckvr'
        self.instance.observation_time = test_value
        self.assertEqual(self.instance.observation_time, test_value)
    
    def test_water_temperature_c_property(self):
        """
        Test water_temperature_c property
        """
        test_value = float(83.20013880693129)
        self.instance.water_temperature_c = test_value
        self.assertEqual(self.instance.water_temperature_c, test_value)
    
    def test_conductivity_s_m_property(self):
        """
        Test conductivity_s_m property
        """
        test_value = float(15.252193908068602)
        self.instance.conductivity_s_m = test_value
        self.assertEqual(self.instance.conductivity_s_m, test_value)
    
    def test_pressure_dbar_property(self):
        """
        Test pressure_dbar property
        """
        test_value = float(1.7490051392557215)
        self.instance.pressure_dbar = test_value
        self.assertEqual(self.instance.pressure_dbar, test_value)
    
    def test_dissolved_oxygen_mg_l_property(self):
        """
        Test dissolved_oxygen_mg_l property
        """
        test_value = float(25.362444989014364)
        self.instance.dissolved_oxygen_mg_l = test_value
        self.assertEqual(self.instance.dissolved_oxygen_mg_l, test_value)
    
    def test_ph_property(self):
        """
        Test ph property
        """
        test_value = float(96.21252102202052)
        self.instance.ph = test_value
        self.assertEqual(self.instance.ph, test_value)
    
    def test_chlorophyll_ug_l_property(self):
        """
        Test chlorophyll_ug_l property
        """
        test_value = float(3.50564372293789)
        self.instance.chlorophyll_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_ug_l, test_value)
    
    def test_turbidity_ntu_property(self):
        """
        Test turbidity_ntu property
        """
        test_value = float(24.604901100939603)
        self.instance.turbidity_ntu = test_value
        self.assertEqual(self.instance.turbidity_ntu, test_value)
    
    def test_chlorophyll_stddev_ug_l_property(self):
        """
        Test chlorophyll_stddev_ug_l property
        """
        test_value = float(40.86359363552465)
        self.instance.chlorophyll_stddev_ug_l = test_value
        self.assertEqual(self.instance.chlorophyll_stddev_ug_l, test_value)
    
    def test_turbidity_stddev_ntu_property(self):
        """
        Test turbidity_stddev_ntu property
        """
        test_value = float(30.568154494280154)
        self.instance.turbidity_stddev_ntu = test_value
        self.assertEqual(self.instance.turbidity_stddev_ntu, test_value)
    
    def test_salinity_psu_property(self):
        """
        Test salinity_psu property
        """
        test_value = float(80.87806898240345)
        self.instance.salinity_psu = test_value
        self.assertEqual(self.instance.salinity_psu, test_value)
    
    def test_specific_conductivity_s_m_property(self):
        """
        Test specific_conductivity_s_m property
        """
        test_value = float(76.56177340943164)
        self.instance.specific_conductivity_s_m = test_value
        self.assertEqual(self.instance.specific_conductivity_s_m, test_value)
    
    def test_dissolved_oxygen_saturation_pct_property(self):
        """
        Test dissolved_oxygen_saturation_pct property
        """
        test_value = float(23.97136638609787)
        self.instance.dissolved_oxygen_saturation_pct = test_value
        self.assertEqual(self.instance.dissolved_oxygen_saturation_pct, test_value)
    
    def test_nitrate_umol_property(self):
        """
        Test nitrate_umol property
        """
        test_value = float(31.89466467815124)
        self.instance.nitrate_umol = test_value
        self.assertEqual(self.instance.nitrate_umol, test_value)
    
    def test_nitrate_mg_l_property(self):
        """
        Test nitrate_mg_l property
        """
        test_value = float(1.6000451469877053)
        self.instance.nitrate_mg_l = test_value
        self.assertEqual(self.instance.nitrate_mg_l, test_value)
    
    def test_wind_direction_deg_property(self):
        """
        Test wind_direction_deg property
        """
        test_value = float(94.88054220563842)
        self.instance.wind_direction_deg = test_value
        self.assertEqual(self.instance.wind_direction_deg, test_value)
    
    def test_wind_speed_m_s_property(self):
        """
        Test wind_speed_m_s property
        """
        test_value = float(88.14593872994645)
        self.instance.wind_speed_m_s = test_value
        self.assertEqual(self.instance.wind_speed_m_s, test_value)
    
    def test_photosynthetically_active_radiation_umol_s_m2_property(self):
        """
        Test photosynthetically_active_radiation_umol_s_m2 property
        """
        test_value = float(28.48487337148423)
        self.instance.photosynthetically_active_radiation_umol_s_m2 = test_value
        self.assertEqual(self.instance.photosynthetically_active_radiation_umol_s_m2, test_value)
    
    def test_air_temperature_f_property(self):
        """
        Test air_temperature_f property
        """
        test_value = float(88.5686037903205)
        self.instance.air_temperature_f = test_value
        self.assertEqual(self.instance.air_temperature_f, test_value)
    
    def test_air_humidity_pct_property(self):
        """
        Test air_humidity_pct property
        """
        test_value = float(74.97334508476466)
        self.instance.air_humidity_pct = test_value
        self.assertEqual(self.instance.air_humidity_pct, test_value)
    
    def test_air_pressure_in_hg_property(self):
        """
        Test air_pressure_in_hg property
        """
        test_value = float(23.621856216901193)
        self.instance.air_pressure_in_hg = test_value
        self.assertEqual(self.instance.air_pressure_in_hg, test_value)
    
    def test_system_battery_v_property(self):
        """
        Test system_battery_v property
        """
        test_value = float(9.341708064057775)
        self.instance.system_battery_v = test_value
        self.assertEqual(self.instance.system_battery_v, test_value)
    
    def test_sensor_battery_v_property(self):
        """
        Test sensor_battery_v property
        """
        test_value = float(64.26388992199789)
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

