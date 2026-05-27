"""
Test case for WeatherAlert
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_nws_producer_data.microsoft.opendata.us.noaa.nws.weatheralert import WeatherAlert
import datetime


class Test_WeatherAlert(unittest.TestCase):
    """
    Test case for WeatherAlert
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WeatherAlert.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WeatherAlert for testing
        """
        instance = WeatherAlert(
            alert_id='gvvxdtjhhhtzrwceuwjk',
            area_desc='mbqwmxheolmegrpraamq',
            sent=datetime.datetime.now(datetime.timezone.utc),
            effective=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            status='vpgmlukxlrranyopojco',
            message_type='iauaagaooktmkfhtwrmb',
            category='vsskiibxjlcovqxfwqkg',
            severity='xqfhzjlcjnxffuhactly',
            certainty='ehrlourgcyqcrpvgnndl',
            urgency='etyqttmugjqevkstmerb',
            event='dssuvbcnpowkmjdzkyfj',
            sender_name='iytpdpbirylkhjqtoero',
            headline='inwzfyifeghfttwmqplu',
            description='cuwxilhduwstybgudzfp'
        )
        return instance

    
    def test_alert_id_property(self):
        """
        Test alert_id property
        """
        test_value = 'gvvxdtjhhhtzrwceuwjk'
        self.instance.alert_id = test_value
        self.assertEqual(self.instance.alert_id, test_value)
    
    def test_area_desc_property(self):
        """
        Test area_desc property
        """
        test_value = 'mbqwmxheolmegrpraamq'
        self.instance.area_desc = test_value
        self.assertEqual(self.instance.area_desc, test_value)
    
    def test_sent_property(self):
        """
        Test sent property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.sent = test_value
        self.assertEqual(self.instance.sent, test_value)
    
    def test_effective_property(self):
        """
        Test effective property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.effective = test_value
        self.assertEqual(self.instance.effective, test_value)
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'vpgmlukxlrranyopojco'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_message_type_property(self):
        """
        Test message_type property
        """
        test_value = 'iauaagaooktmkfhtwrmb'
        self.instance.message_type = test_value
        self.assertEqual(self.instance.message_type, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'vsskiibxjlcovqxfwqkg'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = 'xqfhzjlcjnxffuhactly'
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = 'ehrlourgcyqcrpvgnndl'
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = 'etyqttmugjqevkstmerb'
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'dssuvbcnpowkmjdzkyfj'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'iytpdpbirylkhjqtoero'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'inwzfyifeghfttwmqplu'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'cuwxilhduwstybgudzfp'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WeatherAlert.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
