"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from fienta_producer_data.event import Event


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
            event_id='abtwayloqnroaraiodea',
            name='xmjjzqgmxyvnqxnumyyq',
            start='fflhnnlrslmvtmrixkau',
            end='usfjdemzkvokvbumyqyl',
            duration_text='wewzzgbaxwjhtffcolgp',
            time_notes='appuqzgdtbrscrnzgqho',
            event_status='ccuwluqjqtaorsvdyztw',
            sale_status='bglcyzeukxgbhkjphogc',
            attendance_mode='ksmjdrttdocfxdhbebjb',
            venue_name='ydrlzrwbcrqpqqqlatxt',
            venue_id='hpqijbiagfaujrfjieis',
            address='lyxmikikmznqiislqdok',
            postal_code='vnnicuzpexlegmvkpcrn',
            description='mtgwgrwnupuhttvahtrm',
            url='bqbabnhrgotsqbltcilo',
            buy_tickets_url='lcdrvmstxtrhsvjhjnkj',
            image_url='rtouzczcayvfiiewmaoy',
            image_small_url='lpukhlzofinjvfncnfen',
            series_id='bstfayfbedgumeqefecl',
            organizer_name='dflrpapuofldzgcoshtc',
            organizer_phone='fkatnfdisjiosxgprpkj',
            organizer_email='xgxgnypfrxcvrosnuvvz',
            organizer_id=int(3),
            categories=['qtuxkcrswshhfbncnocp', 'rpgigwixfgpiosdygfba', 'lrzueiazicmxsaxezzvu', 'nypicsrlsgmdandmpfzd']
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'abtwayloqnroaraiodea'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xmjjzqgmxyvnqxnumyyq'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'fflhnnlrslmvtmrixkau'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'usfjdemzkvokvbumyqyl'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_duration_text_property(self):
        """
        Test duration_text property
        """
        test_value = 'wewzzgbaxwjhtffcolgp'
        self.instance.duration_text = test_value
        self.assertEqual(self.instance.duration_text, test_value)
    
    def test_time_notes_property(self):
        """
        Test time_notes property
        """
        test_value = 'appuqzgdtbrscrnzgqho'
        self.instance.time_notes = test_value
        self.assertEqual(self.instance.time_notes, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = 'ccuwluqjqtaorsvdyztw'
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'bglcyzeukxgbhkjphogc'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_attendance_mode_property(self):
        """
        Test attendance_mode property
        """
        test_value = 'ksmjdrttdocfxdhbebjb'
        self.instance.attendance_mode = test_value
        self.assertEqual(self.instance.attendance_mode, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'ydrlzrwbcrqpqqqlatxt'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'hpqijbiagfaujrfjieis'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'lyxmikikmznqiislqdok'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'vnnicuzpexlegmvkpcrn'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'mtgwgrwnupuhttvahtrm'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'bqbabnhrgotsqbltcilo'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_buy_tickets_url_property(self):
        """
        Test buy_tickets_url property
        """
        test_value = 'lcdrvmstxtrhsvjhjnkj'
        self.instance.buy_tickets_url = test_value
        self.assertEqual(self.instance.buy_tickets_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'rtouzczcayvfiiewmaoy'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_small_url_property(self):
        """
        Test image_small_url property
        """
        test_value = 'lpukhlzofinjvfncnfen'
        self.instance.image_small_url = test_value
        self.assertEqual(self.instance.image_small_url, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'bstfayfbedgumeqefecl'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'dflrpapuofldzgcoshtc'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_phone_property(self):
        """
        Test organizer_phone property
        """
        test_value = 'fkatnfdisjiosxgprpkj'
        self.instance.organizer_phone = test_value
        self.assertEqual(self.instance.organizer_phone, test_value)
    
    def test_organizer_email_property(self):
        """
        Test organizer_email property
        """
        test_value = 'xgxgnypfrxcvrosnuvvz'
        self.instance.organizer_email = test_value
        self.assertEqual(self.instance.organizer_email, test_value)
    
    def test_organizer_id_property(self):
        """
        Test organizer_id property
        """
        test_value = int(3)
        self.instance.organizer_id = test_value
        self.assertEqual(self.instance.organizer_id, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = ['qtuxkcrswshhfbncnocp', 'rpgigwixfgpiosdygfba', 'lrzueiazicmxsaxezzvu', 'nypicsrlsgmdandmpfzd']
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

