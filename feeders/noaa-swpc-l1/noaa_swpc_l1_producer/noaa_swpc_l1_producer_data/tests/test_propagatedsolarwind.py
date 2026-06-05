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
            speed=float(25.8640598111456),
            density=float(98.2405476734723),
            temperature=float(84.08352541220967),
            bx=float(54.44178832096718),
            by=float(25.890708168661646),
            bz=float(43.5237100775375),
            bt=float(22.683814429467574),
            vx=float(50.50094523938851),
            vy=float(13.133270252098427),
            vz=float(8.538517310020344)
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
        test_value = float(25.8640598111456)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_density_property(self):
        """
        Test density property
        """
        test_value = float(98.2405476734723)
        self.instance.density = test_value
        self.assertEqual(self.instance.density, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(84.08352541220967)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_bx_property(self):
        """
        Test bx property
        """
        test_value = float(54.44178832096718)
        self.instance.bx = test_value
        self.assertEqual(self.instance.bx, test_value)
    
    def test_by_property(self):
        """
        Test by property
        """
        test_value = float(25.890708168661646)
        self.instance.by = test_value
        self.assertEqual(self.instance.by, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(43.5237100775375)
        self.instance.bz = test_value
        self.assertEqual(self.instance.bz, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(22.683814429467574)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_vx_property(self):
        """
        Test vx property
        """
        test_value = float(50.50094523938851)
        self.instance.vx = test_value
        self.assertEqual(self.instance.vx, test_value)
    
    def test_vy_property(self):
        """
        Test vy property
        """
        test_value = float(13.133270252098427)
        self.instance.vy = test_value
        self.assertEqual(self.instance.vy, test_value)
    
    def test_vz_property(self):
        """
        Test vz property
        """
        test_value = float(8.538517310020344)
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

