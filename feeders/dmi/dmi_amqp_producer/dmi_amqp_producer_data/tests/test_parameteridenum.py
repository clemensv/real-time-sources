import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_amqp_producer_data.parameteridenum import ParameterIdenum


class Test_ParameterIdenum(unittest.TestCase):
    """
    Test case for ParameterIdenum
    """

    def setUp(self):
        """
        Setup test
        """
        self.instance = ParameterIdenum.temp_dry

    @staticmethod
    def create_instance():
        """
        Create instance of ParameterIdenum
        """
        return ParameterIdenum.temp_dry

    def test_enum_values(self):
        """
        Test that all enum values are defined
        """
        self.assertEqual(ParameterIdenum.temp_dry.value, 'temp_dry')
        self.assertEqual(ParameterIdenum.temp_dew.value, 'temp_dew')
        self.assertEqual(ParameterIdenum.temp_grass.value, 'temp_grass')
        self.assertEqual(ParameterIdenum.temp_soil_10cm.value, 'temp_soil_10cm')
        self.assertEqual(ParameterIdenum.temp_mean_past1h.value, 'temp_mean_past1h')
        self.assertEqual(ParameterIdenum.temp_max_past1h.value, 'temp_max_past1h')
        self.assertEqual(ParameterIdenum.temp_min_past1h.value, 'temp_min_past1h')
        self.assertEqual(ParameterIdenum.humidity.value, 'humidity')
        self.assertEqual(ParameterIdenum.humidity_past1h.value, 'humidity_past1h')
        self.assertEqual(ParameterIdenum.pressure.value, 'pressure')
        self.assertEqual(ParameterIdenum.pressure_at_sea.value, 'pressure_at_sea')
        self.assertEqual(ParameterIdenum.wind_dir.value, 'wind_dir')
        self.assertEqual(ParameterIdenum.wind_dir_past1h.value, 'wind_dir_past1h')
        self.assertEqual(ParameterIdenum.wind_speed.value, 'wind_speed')
        self.assertEqual(ParameterIdenum.wind_speed_past1h.value, 'wind_speed_past1h')
        self.assertEqual(ParameterIdenum.wind_max.value, 'wind_max')
        self.assertEqual(ParameterIdenum.wind_min.value, 'wind_min')
        self.assertEqual(ParameterIdenum.wind_max_per10min_past1h.value, 'wind_max_per10min_past1h')
        self.assertEqual(ParameterIdenum.wind_min_past1h.value, 'wind_min_past1h')
        self.assertEqual(ParameterIdenum.gust_always_past1h.value, 'gust_always_past1h')
        self.assertEqual(ParameterIdenum.precip_past1h.value, 'precip_past1h')
        self.assertEqual(ParameterIdenum.precip_past10min.value, 'precip_past10min')
        self.assertEqual(ParameterIdenum.precip_past24h.value, 'precip_past24h')
        self.assertEqual(ParameterIdenum.snow_depth_man.value, 'snow_depth_man')
        self.assertEqual(ParameterIdenum.snow_cover_man.value, 'snow_cover_man')
        self.assertEqual(ParameterIdenum.visibility.value, 'visibility')
        self.assertEqual(ParameterIdenum.visib_mean_last10min.value, 'visib_mean_last10min')
        self.assertEqual(ParameterIdenum.cloud_cover.value, 'cloud_cover')
        self.assertEqual(ParameterIdenum.cloud_height.value, 'cloud_height')
        self.assertEqual(ParameterIdenum.weather.value, 'weather')
        self.assertEqual(ParameterIdenum.leav_hum_dur_past10min.value, 'leav_hum_dur_past10min')
        self.assertEqual(ParameterIdenum.radia_glob.value, 'radia_glob')
        self.assertEqual(ParameterIdenum.radia_glob_past1h.value, 'radia_glob_past1h')
        self.assertEqual(ParameterIdenum.sun_last10min_glob.value, 'sun_last10min_glob')
        self.assertEqual(ParameterIdenum.sun_last1h_glob.value, 'sun_last1h_glob')