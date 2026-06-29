"""
Test case for LightningSensor
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dmi_producer_data.lightningsensor import LightningSensor
from dmi_producer_data.countryenum import CountryEnum
import datetime


class Test_LightningSensor(unittest.TestCase):
    """
    Test case for LightningSensor
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_LightningSensor.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of LightningSensor for testing
        """
        instance = LightningSensor(
            sensor_id='wtfafojerqpwysiwkouh',
            name='pqtipqvcwawovoymrvkz',
            owner='hvuogteagtppssdjelhk',
            country=CountryEnum.DNK,
            latitude=float(50.28018347382582),
            longitude=float(90.93079446610791),
            active_from=datetime.datetime.now(datetime.timezone.utc),
            active_to=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_sensor_id_property(self):
        """
        Test sensor_id property
        """
        test_value = 'wtfafojerqpwysiwkouh'
        self.instance.sensor_id = test_value
        self.assertEqual(self.instance.sensor_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'pqtipqvcwawovoymrvkz'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_owner_property(self):
        """
        Test owner property
        """
        test_value = 'hvuogteagtppssdjelhk'
        self.instance.owner = test_value
        self.assertEqual(self.instance.owner, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = CountryEnum.DNK
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(50.28018347382582)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(90.93079446610791)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_active_from_property(self):
        """
        Test active_from property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.active_from = test_value
        self.assertEqual(self.instance.active_from, test_value)
    
    def test_active_to_property(self):
        """
        Test active_to property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.active_to = test_value
        self.assertEqual(self.instance.active_to, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = LightningSensor.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = LightningSensor.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

