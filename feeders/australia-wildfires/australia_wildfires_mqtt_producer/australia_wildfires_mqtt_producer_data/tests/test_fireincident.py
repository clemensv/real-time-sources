"""
Test case for FireIncident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from australia_wildfires_mqtt_producer_data.fireincident import FireIncident
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
            incident_id='qfswdcbxnlfbiwqavrxp',
            state='ggjeuhlfqcpwwbtzabsy',
            title='lhncjnoznfiqmlaxgjfd',
            alert_level='wzeimsrjtvivznuxxbfq',
            status='nmvckjyozqphxyidzgte',
            location='cyxhjcdsrwlvntpjvbsc',
            latitude=float(77.23411198588978),
            longitude=float(43.655104617444884),
            size_hectares=float(97.54792733834306),
            type='eechprvjlpybfacetjcz',
            responsible_agency='ehrufaciwojtqpuvmpxz',
            updated=datetime.datetime.now(datetime.timezone.utc),
            source_url='qosvtimvbvtukijpemyk'
        )
        return instance

    
    def test_incident_id_property(self):
        """
        Test incident_id property
        """
        test_value = 'qfswdcbxnlfbiwqavrxp'
        self.instance.incident_id = test_value
        self.assertEqual(self.instance.incident_id, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'ggjeuhlfqcpwwbtzabsy'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'lhncjnoznfiqmlaxgjfd'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_alert_level_property(self):
        """
        Test alert_level property
        """
        test_value = 'wzeimsrjtvivznuxxbfq'
        self.instance.alert_level = test_value
        self.assertEqual(self.instance.alert_level, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'nmvckjyozqphxyidzgte'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_location_property(self):
        """
        Test location property
        """
        test_value = 'cyxhjcdsrwlvntpjvbsc'
        self.instance.location = test_value
        self.assertEqual(self.instance.location, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(77.23411198588978)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(43.655104617444884)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_size_hectares_property(self):
        """
        Test size_hectares property
        """
        test_value = float(97.54792733834306)
        self.instance.size_hectares = test_value
        self.assertEqual(self.instance.size_hectares, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'eechprvjlpybfacetjcz'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_responsible_agency_property(self):
        """
        Test responsible_agency property
        """
        test_value = 'ehrufaciwojtqpuvmpxz'
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
        test_value = 'qosvtimvbvtukijpemyk'
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

