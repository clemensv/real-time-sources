"""
Test case for Incident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from seattle_911_amqp_producer_data.incident import Incident
import datetime


class Test_Incident(unittest.TestCase):
    """
    Test case for Incident
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Incident.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Incident for testing
        """
        instance = Incident(
            incident_number='rfklzumetyzatcgyhhdm',
            incident_type='drathzmzaunrscfxcbkj',
            incident_datetime='ervwubudeqrttsujzoaa',
            address='cthbfknnwrqditezxtie',
            latitude=float(58.256080881024864),
            longitude=float(20.615590004316953),
            incident_type_slug='bnryfmxvgmtprtsyaszz',
            incident_datetime_utc=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_incident_number_property(self):
        """
        Test incident_number property
        """
        test_value = 'rfklzumetyzatcgyhhdm'
        self.instance.incident_number = test_value
        self.assertEqual(self.instance.incident_number, test_value)
    
    def test_incident_type_property(self):
        """
        Test incident_type property
        """
        test_value = 'drathzmzaunrscfxcbkj'
        self.instance.incident_type = test_value
        self.assertEqual(self.instance.incident_type, test_value)
    
    def test_incident_datetime_property(self):
        """
        Test incident_datetime property
        """
        test_value = 'ervwubudeqrttsujzoaa'
        self.instance.incident_datetime = test_value
        self.assertEqual(self.instance.incident_datetime, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'cthbfknnwrqditezxtie'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(58.256080881024864)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(20.615590004316953)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_incident_type_slug_property(self):
        """
        Test incident_type_slug property
        """
        test_value = 'bnryfmxvgmtprtsyaszz'
        self.instance.incident_type_slug = test_value
        self.assertEqual(self.instance.incident_type_slug, test_value)
    
    def test_incident_datetime_utc_property(self):
        """
        Test incident_datetime_utc property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.incident_datetime_utc = test_value
        self.assertEqual(self.instance.incident_datetime_utc, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Incident.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Incident.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

