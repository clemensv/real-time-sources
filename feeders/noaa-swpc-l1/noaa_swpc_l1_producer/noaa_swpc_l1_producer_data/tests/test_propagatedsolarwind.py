"""
Test case for PropagatedSolarWind
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_swpc_l1_producer_data.gov.noaa.swpc.l1.propagatedsolarwind import PropagatedSolarWind
from noaa_swpc_l1_producer_data.gov.noaa.swpc.l1.spacecraftenum import SpacecraftEnum
import datetime


class Test_PropagatedSolarWind(unittest.TestCase):
    """
    Test case for PropagatedSolarWind
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PropagatedSolarWind.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PropagatedSolarWind for testing
        """
        instance = PropagatedSolarWind(
            spacecraft=SpacecraftEnum.dscovr,
            time_tag=datetime.datetime.now(datetime.timezone.utc),
            propagated_time_tag=datetime.datetime.now(datetime.timezone.utc),
            speed=float(24.700287027174795),
            density=float(89.38884428806652),
            temperature=float(41.83175530041044),
            bx=float(70.16723044485424),
            by=float(13.37206778889909),
            bz=float(90.85089216254335),
            bt=float(41.36464246973786),
            vx=float(40.23808212448644),
            vy=float(51.07892420766792),
            vz=float(37.80393146967599)
        )
        return instance

    
    def test_spacecraft_property(self):
        """
        Test spacecraft property
        """
        test_value = SpacecraftEnum.dscovr
        self.instance.spacecraft = test_value
        self.assertEqual(self.instance.spacecraft, test_value)
    
    def test_time_tag_property(self):
        """
        Test time_tag property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.time_tag = test_value
        self.assertEqual(self.instance.time_tag, test_value)
    
    def test_propagated_time_tag_property(self):
        """
        Test propagated_time_tag property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.propagated_time_tag = test_value
        self.assertEqual(self.instance.propagated_time_tag, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(24.700287027174795)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_density_property(self):
        """
        Test density property
        """
        test_value = float(89.38884428806652)
        self.instance.density = test_value
        self.assertEqual(self.instance.density, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(41.83175530041044)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_bx_property(self):
        """
        Test bx property
        """
        test_value = float(70.16723044485424)
        self.instance.bx = test_value
        self.assertEqual(self.instance.bx, test_value)
    
    def test_by_property(self):
        """
        Test by property
        """
        test_value = float(13.37206778889909)
        self.instance.by = test_value
        self.assertEqual(self.instance.by, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(90.85089216254335)
        self.instance.bz = test_value
        self.assertEqual(self.instance.bz, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(41.36464246973786)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_vx_property(self):
        """
        Test vx property
        """
        test_value = float(40.23808212448644)
        self.instance.vx = test_value
        self.assertEqual(self.instance.vx, test_value)
    
    def test_vy_property(self):
        """
        Test vy property
        """
        test_value = float(51.07892420766792)
        self.instance.vy = test_value
        self.assertEqual(self.instance.vy, test_value)
    
    def test_vz_property(self):
        """
        Test vz property
        """
        test_value = float(37.80393146967599)
        self.instance.vz = test_value
        self.assertEqual(self.instance.vz, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PropagatedSolarWind.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PropagatedSolarWind.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

