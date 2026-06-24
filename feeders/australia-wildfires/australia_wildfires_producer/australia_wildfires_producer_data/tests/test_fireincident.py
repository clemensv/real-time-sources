"""
Test case for FireIncident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from australia_wildfires_producer_data.fireincident import FireIncident
import datetime


class Test_FireIncident(unittest.TestCase):
    """
    Test case for FireIncident
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_FireIncident.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of FireIncident for testing
        """
        instance = FireIncident(
            incident_id='ilwqsbeqeeaiuerttrgm',
            state='cnvrchvdxpdljkscssgk',
            title='gagjhvybpagavrfuihph',
            alert_level='ktuvmtbewgsezwmttkrb',
            status='ifozldewqitdodumrjqg',
            location='efggjyuwrkpyzjhshbbk',
            latitude=float(77.31380349686448),
            longitude=float(85.41329346336181),
            size_hectares=float(96.6403438426712),
            type='xkrglikpoijpjpvypdka',
            responsible_agency='ubprjvejfrlndmkjftvd',
            updated=datetime.datetime.now(datetime.timezone.utc),
            source_url='igihhxmkkpapgwtvrunx'
        )
        return instance

    
    def test_incident_id_property(self):
        """
        Test incident_id property
        """
        test_value = 'ilwqsbeqeeaiuerttrgm'
        self.instance.incident_id = test_value
        self.assertEqual(self.instance.incident_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'cnvrchvdxpdljkscssgk'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'gagjhvybpagavrfuihph'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_alert_level_property(self):
        """
        Test alert_level property
        """
        test_value = 'ktuvmtbewgsezwmttkrb'
        self.instance.alert_level = test_value
        self.assertEqual(self.instance.alert_level, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'ifozldewqitdodumrjqg'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'efggjyuwrkpyzjhshbbk'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(77.31380349686448)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(85.41329346336181)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_size_hectares_property(self):
        """
        Test size_hectares property
        """
        test_value = float(96.6403438426712)
        self.instance.size_hectares = test_value
        self.assertEqual(self.instance.size_hectares, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'xkrglikpoijpjpvypdka'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_responsible_agency_property(self):
        """
        Test responsible_agency property
        """
        test_value = 'ubprjvejfrlndmkjftvd'
        self.instance.responsible_agency = test_value
        self.assertEqual(self.instance.responsible_agency, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_source_url_property(self):
        """
        Test source_url property
        """
        test_value = 'igihhxmkkpapgwtvrunx'
        self.instance.source_url = test_value
        self.assertEqual(self.instance.source_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = FireIncident.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = FireIncident.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

