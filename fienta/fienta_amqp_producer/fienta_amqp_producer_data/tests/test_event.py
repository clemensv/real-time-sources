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
            event_id='dcbybytxnkuouptcqbjg',
            name='vlabsisydakxvxfcftpe',
            start='gbbjufbkfnxtxxabjhgp',
            end='tirjskapxdeewjwppvnq',
            duration_text='vjllozmyduqqtclqphvj',
            time_notes='dilrmihtfxlnsxvmiqwt',
            event_status='juodczlnisgkiihzohnt',
            sale_status='hvhvnkjobmzeitlghyla',
            attendance_mode='xzsutadovqmgugokwczf',
            venue_name='gigtetvknmwdjakpxvoo',
            venue_id='tbttrzuiektxktmrtwol',
            address='iosuyqzbfunusntopblg',
            postal_code='rbjoewimpbckuxfiacnt',
            description='ubmdfwsvlmqzkrgpobbi',
            url='htvdgfrbrocjdnveqhvp',
            buy_tickets_url='khzbpsjqvjffrnydkyfl',
            image_url='nvieygyprclsqqcdosrs',
            image_small_url='ugowovcbeurmdegmjeba',
            series_id='bmndydjazrezlzqqddid',
            organizer_name='osrlrgnepdlzndsdevgp',
            organizer_phone='lmydffwedlffiiezpbje',
            organizer_email='yugwdcgagudftgdfsism',
            organizer_id=int(71),
            categories=['npwdvtgeksgiualpcsbk', 'hquqapfxacopkhzfhvgl']
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'dcbybytxnkuouptcqbjg'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'vlabsisydakxvxfcftpe'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'gbbjufbkfnxtxxabjhgp'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'tirjskapxdeewjwppvnq'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_duration_text_property(self):
        """
        Test duration_text property
        """
        test_value = 'vjllozmyduqqtclqphvj'
        self.instance.duration_text = test_value
        self.assertEqual(self.instance.duration_text, test_value)
    
    def test_time_notes_property(self):
        """
        Test time_notes property
        """
        test_value = 'dilrmihtfxlnsxvmiqwt'
        self.instance.time_notes = test_value
        self.assertEqual(self.instance.time_notes, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = 'juodczlnisgkiihzohnt'
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'hvhvnkjobmzeitlghyla'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_attendance_mode_property(self):
        """
        Test attendance_mode property
        """
        test_value = 'xzsutadovqmgugokwczf'
        self.instance.attendance_mode = test_value
        self.assertEqual(self.instance.attendance_mode, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'gigtetvknmwdjakpxvoo'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'tbttrzuiektxktmrtwol'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'iosuyqzbfunusntopblg'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'rbjoewimpbckuxfiacnt'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'ubmdfwsvlmqzkrgpobbi'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'htvdgfrbrocjdnveqhvp'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_buy_tickets_url_property(self):
        """
        Test buy_tickets_url property
        """
        test_value = 'khzbpsjqvjffrnydkyfl'
        self.instance.buy_tickets_url = test_value
        self.assertEqual(self.instance.buy_tickets_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'nvieygyprclsqqcdosrs'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_small_url_property(self):
        """
        Test image_small_url property
        """
        test_value = 'ugowovcbeurmdegmjeba'
        self.instance.image_small_url = test_value
        self.assertEqual(self.instance.image_small_url, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'bmndydjazrezlzqqddid'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'osrlrgnepdlzndsdevgp'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_phone_property(self):
        """
        Test organizer_phone property
        """
        test_value = 'lmydffwedlffiiezpbje'
        self.instance.organizer_phone = test_value
        self.assertEqual(self.instance.organizer_phone, test_value)
    
    def test_organizer_email_property(self):
        """
        Test organizer_email property
        """
        test_value = 'yugwdcgagudftgdfsism'
        self.instance.organizer_email = test_value
        self.assertEqual(self.instance.organizer_email, test_value)
    
    def test_organizer_id_property(self):
        """
        Test organizer_id property
        """
        test_value = int(71)
        self.instance.organizer_id = test_value
        self.assertEqual(self.instance.organizer_id, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = ['npwdvtgeksgiualpcsbk', 'hquqapfxacopkhzfhvgl']
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

