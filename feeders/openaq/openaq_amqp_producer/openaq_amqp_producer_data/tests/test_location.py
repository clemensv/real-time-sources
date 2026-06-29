"""
Test case for Location
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from openaq_amqp_producer_data.org.openaq.location import Location
import datetime


class Test_Location(unittest.TestCase):
    """
    Test case for Location
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Location.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Location for testing
        """
        instance = Location(
            location_id=int(4),
            name='hkljkbmcqmjsffvzcmej',
            locality='fbjumoezqaketzuqqwlo',
            timezone='hmlkhjjacwvnzgwexwki',
            country_iso='mtsgftuzmalckwnzwvsf',
            country_name='zddnscsjfykfxpwmkjyt',
            owner_id=int(25),
            owner_name='jqhhwbdipdkcnulmtzli',
            provider_id=int(6),
            provider_name='pptovcfslrleqjalaqta',
            is_mobile=True,
            is_monitor=False,
            latitude=float(10.688349848438838),
            longitude=float(99.54246427519546),
            datetime_first=datetime.datetime.now(datetime.timezone.utc),
            datetime_last=datetime.datetime.now(datetime.timezone.utc),
            license='eahhkaxosftmejmdlhmw',
            sensor_count=int(9)
        )
        return instance

    
    def test_location_id_property(self):
        """
        Test location_id property
        """
        test_value = int(4)
        self.instance.location_id = test_value
        self.assertEqual(self.instance.location_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hkljkbmcqmjsffvzcmej'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_locality_property(self):
        """
        Test locality property
        """
        test_value = 'fbjumoezqaketzuqqwlo'
        self.instance.locality = test_value
        self.assertEqual(self.instance.locality, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'hmlkhjjacwvnzgwexwki'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_country_iso_property(self):
        """
        Test country_iso property
        """
        test_value = 'mtsgftuzmalckwnzwvsf'
        self.instance.country_iso = test_value
        self.assertEqual(self.instance.country_iso, test_value)
    
    def test_country_name_property(self):
        """
        Test country_name property
        """
        test_value = 'zddnscsjfykfxpwmkjyt'
        self.instance.country_name = test_value
        self.assertEqual(self.instance.country_name, test_value)
    
    def test_owner_id_property(self):
        """
        Test owner_id property
        """
        test_value = int(25)
        self.instance.owner_id = test_value
        self.assertEqual(self.instance.owner_id, test_value)
    
    def test_owner_name_property(self):
        """
        Test owner_name property
        """
        test_value = 'jqhhwbdipdkcnulmtzli'
        self.instance.owner_name = test_value
        self.assertEqual(self.instance.owner_name, test_value)
    
    def test_provider_id_property(self):
        """
        Test provider_id property
        """
        test_value = int(6)
        self.instance.provider_id = test_value
        self.assertEqual(self.instance.provider_id, test_value)
    
    def test_provider_name_property(self):
        """
        Test provider_name property
        """
        test_value = 'pptovcfslrleqjalaqta'
        self.instance.provider_name = test_value
        self.assertEqual(self.instance.provider_name, test_value)
    
    def test_is_mobile_property(self):
        """
        Test is_mobile property
        """
        test_value = True
        self.instance.is_mobile = test_value
        self.assertEqual(self.instance.is_mobile, test_value)
    
    def test_is_monitor_property(self):
        """
        Test is_monitor property
        """
        test_value = False
        self.instance.is_monitor = test_value
        self.assertEqual(self.instance.is_monitor, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(10.688349848438838)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(99.54246427519546)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_datetime_first_property(self):
        """
        Test datetime_first property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime_first = test_value
        self.assertEqual(self.instance.datetime_first, test_value)
    
    def test_datetime_last_property(self):
        """
        Test datetime_last property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.datetime_last = test_value
        self.assertEqual(self.instance.datetime_last, test_value)
    
    def test_license_property(self):
        """
        Test license property
        """
        test_value = 'eahhkaxosftmejmdlhmw'
        self.instance.license = test_value
        self.assertEqual(self.instance.license, test_value)
    
    def test_sensor_count_property(self):
        """
        Test sensor_count property
        """
        test_value = int(9)
        self.instance.sensor_count = test_value
        self.assertEqual(self.instance.sensor_count, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Location.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Location.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

