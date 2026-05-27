"""
Test case for MagneticFieldReading
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_geomag_mqtt_producer_data.magneticfieldreading import MagneticFieldReading
import datetime


class Test_MagneticFieldReading(unittest.TestCase):
    """
    Test case for MagneticFieldReading
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MagneticFieldReading.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MagneticFieldReading for testing
        """
        instance = MagneticFieldReading(
            iaga_code='rfyephueuruxjktlzcii',
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            h=float(31.917443457587545),
            d=float(84.80849969836828),
            z=float(86.3781360772114),
            f=float(94.57551044258747)
        )
        return instance

    
    def test_iaga_code_property(self):
        """
        Test iaga_code property
        """
        test_value = 'rfyephueuruxjktlzcii'
        self.instance.iaga_code = test_value
        self.assertEqual(self.instance.iaga_code, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_h_property(self):
        """
        Test h property
        """
        test_value = float(31.917443457587545)
        self.instance.h = test_value
        self.assertEqual(self.instance.h, test_value)
    
    def test_d_property(self):
        """
        Test d property
        """
        test_value = float(84.80849969836828)
        self.instance.d = test_value
        self.assertEqual(self.instance.d, test_value)
    
    def test_z_property(self):
        """
        Test z property
        """
        test_value = float(86.3781360772114)
        self.instance.z = test_value
        self.assertEqual(self.instance.z, test_value)
    
    def test_f_property(self):
        """
        Test f property
        """
        test_value = float(94.57551044258747)
        self.instance.f = test_value
        self.assertEqual(self.instance.f, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MagneticFieldReading.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MagneticFieldReading.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

