"""
Test case for WaterLevelObservation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nve_hydro_amqp_producer_data.waterlevelobservation import WaterLevelObservation
import datetime


class Test_WaterLevelObservation(unittest.TestCase):
    """
    Test case for WaterLevelObservation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WaterLevelObservation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WaterLevelObservation for testing
        """
        instance = WaterLevelObservation(
            station_id='hvcdsdkisxkrtlnapwru',
            river_name='dbiffhdfxkzkghpkoecp',
            water_level=float(4.545082686657221),
            water_level_unit='nyntizmjghmucbgvusdx',
            water_level_timestamp=datetime.datetime.now(datetime.timezone.utc),
            water_level_quality=int(97),
            water_level_correction=int(33),
            water_level_series_version=int(7),
            water_level_method='lupjhjjokeuurmzhnlww',
            discharge=float(82.30553457401926),
            discharge_unit='ayowlhlxtiqmyqxcbsfp',
            discharge_timestamp=datetime.datetime.now(datetime.timezone.utc),
            discharge_quality=int(63),
            discharge_correction=int(5),
            discharge_series_version=int(78),
            discharge_method='vklqlpkkkhpmjgkgytdk'
        )
        return instance


    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'hvcdsdkisxkrtlnapwru'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)

    def test_river_name_property(self):
        """
        Test river_name property
        """
        test_value = 'dbiffhdfxkzkghpkoecp'
        self.instance.river_name = test_value
        self.assertEqual(self.instance.river_name, test_value)

    def test_water_level_property(self):
        """
        Test water_level property
        """
        test_value = float(4.545082686657221)
        self.instance.water_level = test_value
        self.assertEqual(self.instance.water_level, test_value)

    def test_water_level_unit_property(self):
        """
        Test water_level_unit property
        """
        test_value = 'nyntizmjghmucbgvusdx'
        self.instance.water_level_unit = test_value
        self.assertEqual(self.instance.water_level_unit, test_value)

    def test_water_level_timestamp_property(self):
        """
        Test water_level_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.water_level_timestamp = test_value
        self.assertEqual(self.instance.water_level_timestamp, test_value)

    def test_water_level_quality_property(self):
        """
        Test water_level_quality property
        """
        test_value = int(97)
        self.instance.water_level_quality = test_value
        self.assertEqual(self.instance.water_level_quality, test_value)

    def test_water_level_correction_property(self):
        """
        Test water_level_correction property
        """
        test_value = int(33)
        self.instance.water_level_correction = test_value
        self.assertEqual(self.instance.water_level_correction, test_value)

    def test_water_level_series_version_property(self):
        """
        Test water_level_series_version property
        """
        test_value = int(7)
        self.instance.water_level_series_version = test_value
        self.assertEqual(self.instance.water_level_series_version, test_value)

    def test_water_level_method_property(self):
        """
        Test water_level_method property
        """
        test_value = 'lupjhjjokeuurmzhnlww'
        self.instance.water_level_method = test_value
        self.assertEqual(self.instance.water_level_method, test_value)

    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = float(82.30553457401926)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)

    def test_discharge_unit_property(self):
        """
        Test discharge_unit property
        """
        test_value = 'ayowlhlxtiqmyqxcbsfp'
        self.instance.discharge_unit = test_value
        self.assertEqual(self.instance.discharge_unit, test_value)

    def test_discharge_timestamp_property(self):
        """
        Test discharge_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.discharge_timestamp = test_value
        self.assertEqual(self.instance.discharge_timestamp, test_value)

    def test_discharge_quality_property(self):
        """
        Test discharge_quality property
        """
        test_value = int(63)
        self.instance.discharge_quality = test_value
        self.assertEqual(self.instance.discharge_quality, test_value)

    def test_discharge_correction_property(self):
        """
        Test discharge_correction property
        """
        test_value = int(5)
        self.instance.discharge_correction = test_value
        self.assertEqual(self.instance.discharge_correction, test_value)

    def test_discharge_series_version_property(self):
        """
        Test discharge_series_version property
        """
        test_value = int(78)
        self.instance.discharge_series_version = test_value
        self.assertEqual(self.instance.discharge_series_version, test_value)

    def test_discharge_method_property(self):
        """
        Test discharge_method property
        """
        test_value = 'vklqlpkkkhpmjgkgytdk'
        self.instance.discharge_method = test_value
        self.assertEqual(self.instance.discharge_method, test_value)

    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WaterLevelObservation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WaterLevelObservation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

