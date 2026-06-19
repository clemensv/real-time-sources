"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_mqtt_producer_data.event import Event


class Test_Event(unittest.TestCase):
    """
    Test case for Event
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Event.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Event for testing
        """
        instance = Event(
            event_id='sdlhbjpatqptfjwpfiih',
            name='poxhseisxdvqyeqmacff',
            start='xfdtgjadvmxsbbztbuaw',
            end='irqvbnivjgvdddrdmyiq',
            duration_text='smbjsuaewrcjsoxhqper',
            time_notes='zopnbdwumynvijrsshyc',
            event_status='hwdyykjudmswfgrednke',
            sale_status='feusblugktzowhtyutdc',
            attendance_mode='skobeyfmxrtecqfabkom',
            venue_name='diadaknipxrnvawijgtv',
            venue_id='gcinaetutsdblledlyda',
            address='mqukhdylcypqrmrhnbrg',
            postal_code='fnyzfbywniojromjqoku',
            description='zdweianqurxashcoincw',
            url='yrtokkiwubglleftbagk',
            buy_tickets_url='qewnfofolwpjevdbzvsk',
            image_url='itvsfrsnqzabluezssql',
            image_small_url='ptnldqnqljmumgdcgvnn',
            series_id='niqsxaokkifxitzowpeb',
            organizer_name='rndljxuppabttaxfcbes',
            organizer_phone='zmyilxdhcdujczdtnrcf',
            organizer_email='gwzlrdjxtiewrhzlwptt',
            organizer_id=int(36),
            categories=['dgmhhjnphkxutflvknlu', 'muzvejwehleodvuhcjpz', 'mjoefljfhvzrjqezdluf', 'amukopmlspbvakduklpb', 'ahsbivhbtjaxspbvalpa']
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'sdlhbjpatqptfjwpfiih'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'poxhseisxdvqyeqmacff'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'xfdtgjadvmxsbbztbuaw'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'irqvbnivjgvdddrdmyiq'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_duration_text_property(self):
        """
        Test duration_text property
        """
        test_value = 'smbjsuaewrcjsoxhqper'
        self.instance.duration_text = test_value
        self.assertEqual(self.instance.duration_text, test_value)
    
    def test_time_notes_property(self):
        """
        Test time_notes property
        """
        test_value = 'zopnbdwumynvijrsshyc'
        self.instance.time_notes = test_value
        self.assertEqual(self.instance.time_notes, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = 'hwdyykjudmswfgrednke'
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'feusblugktzowhtyutdc'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_attendance_mode_property(self):
        """
        Test attendance_mode property
        """
        test_value = 'skobeyfmxrtecqfabkom'
        self.instance.attendance_mode = test_value
        self.assertEqual(self.instance.attendance_mode, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'diadaknipxrnvawijgtv'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'gcinaetutsdblledlyda'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'mqukhdylcypqrmrhnbrg'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'fnyzfbywniojromjqoku'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'zdweianqurxashcoincw'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'yrtokkiwubglleftbagk'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_buy_tickets_url_property(self):
        """
        Test buy_tickets_url property
        """
        test_value = 'qewnfofolwpjevdbzvsk'
        self.instance.buy_tickets_url = test_value
        self.assertEqual(self.instance.buy_tickets_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'itvsfrsnqzabluezssql'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_small_url_property(self):
        """
        Test image_small_url property
        """
        test_value = 'ptnldqnqljmumgdcgvnn'
        self.instance.image_small_url = test_value
        self.assertEqual(self.instance.image_small_url, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'niqsxaokkifxitzowpeb'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'rndljxuppabttaxfcbes'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_phone_property(self):
        """
        Test organizer_phone property
        """
        test_value = 'zmyilxdhcdujczdtnrcf'
        self.instance.organizer_phone = test_value
        self.assertEqual(self.instance.organizer_phone, test_value)
    
    def test_organizer_email_property(self):
        """
        Test organizer_email property
        """
        test_value = 'gwzlrdjxtiewrhzlwptt'
        self.instance.organizer_email = test_value
        self.assertEqual(self.instance.organizer_email, test_value)
    
    def test_organizer_id_property(self):
        """
        Test organizer_id property
        """
        test_value = int(36)
        self.instance.organizer_id = test_value
        self.assertEqual(self.instance.organizer_id, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = ['dgmhhjnphkxutflvknlu', 'muzvejwehleodvuhcjpz', 'mjoefljfhvzrjqezdluf', 'amukopmlspbvakduklpb', 'ahsbivhbtjaxspbvalpa']
        self.instance.categories = test_value
        self.assertEqual(self.instance.categories, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Event.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Event.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

