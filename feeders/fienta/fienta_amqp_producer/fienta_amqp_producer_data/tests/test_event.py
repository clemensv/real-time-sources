"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_amqp_producer_data.event import Event


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
            event_id='zshgiwcqhmzyyaixachj',
            name='hrgfxwbiwdruzajxiyrq',
            start='owogcqzdnfsehqhqdmxj',
            end='nghrzbwemvnwrfwdqyxm',
            duration_text='svpcxynkukhqqdvbkxag',
            time_notes='owdniymymjvtsxorhqst',
            event_status='ivvltjzjbzfnwfmjdntg',
            sale_status='cgbbrdixeeepsnrnhqhm',
            attendance_mode='uffrsmlgxnvsxeqyzfiu',
            venue_name='teeluhzrzakwjwgppofm',
            venue_id='pwdqqyoilvfuwkysjvay',
            address='cjvdnkhymkganbjnmfsm',
            postal_code='atpqiwwmwprndhrvontu',
            description='svhvpkrogzmotbkvydsr',
            url='fzfuhujjcgzkslgssuoh',
            buy_tickets_url='jwtqjwsmlhrebzcbmebx',
            image_url='airpnlhjrarxptgudcdf',
            image_small_url='vbjrmyadlejypzagzhpz',
            series_id='vcznbdfmhdbavtzsfopi',
            organizer_name='aaxdeluefvpfsyxasgwb',
            organizer_phone='msfeigslqennjnifewgl',
            organizer_email='bktjtdnccunyfczeqiir',
            organizer_id=int(76),
            categories=['eukhjghtygsrstilowfq', 'jxdsiieyvnhzuvzspqvk', 'tzrhkoxaaznadfzqrrwj']
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'zshgiwcqhmzyyaixachj'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'hrgfxwbiwdruzajxiyrq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'owogcqzdnfsehqhqdmxj'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'nghrzbwemvnwrfwdqyxm'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_duration_text_property(self):
        """
        Test duration_text property
        """
        test_value = 'svpcxynkukhqqdvbkxag'
        self.instance.duration_text = test_value
        self.assertEqual(self.instance.duration_text, test_value)
    
    def test_time_notes_property(self):
        """
        Test time_notes property
        """
        test_value = 'owdniymymjvtsxorhqst'
        self.instance.time_notes = test_value
        self.assertEqual(self.instance.time_notes, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = 'ivvltjzjbzfnwfmjdntg'
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'cgbbrdixeeepsnrnhqhm'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_attendance_mode_property(self):
        """
        Test attendance_mode property
        """
        test_value = 'uffrsmlgxnvsxeqyzfiu'
        self.instance.attendance_mode = test_value
        self.assertEqual(self.instance.attendance_mode, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'teeluhzrzakwjwgppofm'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'pwdqqyoilvfuwkysjvay'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'cjvdnkhymkganbjnmfsm'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'atpqiwwmwprndhrvontu'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'svhvpkrogzmotbkvydsr'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'fzfuhujjcgzkslgssuoh'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_buy_tickets_url_property(self):
        """
        Test buy_tickets_url property
        """
        test_value = 'jwtqjwsmlhrebzcbmebx'
        self.instance.buy_tickets_url = test_value
        self.assertEqual(self.instance.buy_tickets_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'airpnlhjrarxptgudcdf'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_small_url_property(self):
        """
        Test image_small_url property
        """
        test_value = 'vbjrmyadlejypzagzhpz'
        self.instance.image_small_url = test_value
        self.assertEqual(self.instance.image_small_url, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'vcznbdfmhdbavtzsfopi'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'aaxdeluefvpfsyxasgwb'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_phone_property(self):
        """
        Test organizer_phone property
        """
        test_value = 'msfeigslqennjnifewgl'
        self.instance.organizer_phone = test_value
        self.assertEqual(self.instance.organizer_phone, test_value)
    
    def test_organizer_email_property(self):
        """
        Test organizer_email property
        """
        test_value = 'bktjtdnccunyfczeqiir'
        self.instance.organizer_email = test_value
        self.assertEqual(self.instance.organizer_email, test_value)
    
    def test_organizer_id_property(self):
        """
        Test organizer_id property
        """
        test_value = int(76)
        self.instance.organizer_id = test_value
        self.assertEqual(self.instance.organizer_id, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = ['eukhjghtygsrstilowfq', 'jxdsiieyvnhzuvzspqvk', 'tzrhkoxaaznadfzqrrwj']
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

