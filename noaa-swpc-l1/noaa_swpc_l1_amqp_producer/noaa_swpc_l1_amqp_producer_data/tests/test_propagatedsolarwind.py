"""
Test case for PropagatedSolarWind
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_swpc_l1_amqp_producer_data.gov.noaa.swpc.l1.propagatedsolarwind import PropagatedSolarWind
from noaa_swpc_l1_amqp_producer_data.gov.noaa.swpc.l1.spacecraftenum import SpacecraftEnum
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
            speed=float(58.89069478006468),
            density=float(94.34471366671488),
            temperature=float(90.83813276387026),
            bx=float(52.88368270981009),
            by=float(55.16092630033713),
            bz=float(22.585677725810903),
            bt=float(48.168451245810864),
            vx=float(75.67640677996404),
            vy=float(45.26384042134315),
            vz=float(64.18937915660132)
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
        test_value = float(58.89069478006468)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_density_property(self):
        """
        Test density property
        """
        test_value = float(94.34471366671488)
        self.instance.density = test_value
        self.assertEqual(self.instance.density, test_value)
    
    def test_temperature_property(self):
        """
        Test temperature property
        """
        test_value = float(90.83813276387026)
        self.instance.temperature = test_value
        self.assertEqual(self.instance.temperature, test_value)
    
    def test_bx_property(self):
        """
        Test bx property
        """
        test_value = float(52.88368270981009)
        self.instance.bx = test_value
        self.assertEqual(self.instance.bx, test_value)
    
    def test_by_property(self):
        """
        Test by property
        """
        test_value = float(55.16092630033713)
        self.instance.by = test_value
        self.assertEqual(self.instance.by, test_value)
    
    def test_bz_property(self):
        """
        Test bz property
        """
        test_value = float(22.585677725810903)
        self.instance.bz = test_value
        self.assertEqual(self.instance.bz, test_value)
    
    def test_bt_property(self):
        """
        Test bt property
        """
        test_value = float(48.168451245810864)
        self.instance.bt = test_value
        self.assertEqual(self.instance.bt, test_value)
    
    def test_vx_property(self):
        """
        Test vx property
        """
        test_value = float(75.67640677996404)
        self.instance.vx = test_value
        self.assertEqual(self.instance.vx, test_value)
    
    def test_vy_property(self):
        """
        Test vy property
        """
        test_value = float(45.26384042134315)
        self.instance.vy = test_value
        self.assertEqual(self.instance.vy, test_value)
    
    def test_vz_property(self):
        """
        Test vz property
        """
        test_value = float(64.18937915660132)
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

