"""
Test case for Incident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from seattle_911_producer_data.incident import Incident


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
            incident_number='gdgqduvgrmffquksgivn',
            incident_type='bggmvxkfqtopbzawxjbw',
            incident_datetime='ipqyncduqchfsteejbch',
            address='bizjujqfeyznosunebqd',
            latitude=float(58.90694147483404),
            longitude=float(65.52139347607613)
        )
        return instance

    
    def test_incident_number_property(self):
        """
        Test incident_number property
        """
        test_value = 'gdgqduvgrmffquksgivn'
        self.instance.incident_number = test_value
        self.assertEqual(self.instance.incident_number, test_value)
    
    def test_incident_type_property(self):
        """
        Test incident_type property
        """
        test_value = 'bggmvxkfqtopbzawxjbw'
        self.instance.incident_type = test_value
        self.assertEqual(self.instance.incident_type, test_value)
    
    def test_incident_datetime_property(self):
        """
        Test incident_datetime property
        """
        test_value = 'ipqyncduqchfsteejbch'
        self.instance.incident_datetime = test_value
        self.assertEqual(self.instance.incident_datetime, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'bizjujqfeyznosunebqd'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(58.90694147483404)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(65.52139347607613)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
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

