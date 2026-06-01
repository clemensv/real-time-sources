"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ticketmaster_mqtt_producer_data.ticketmaster.events.event import Event


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
            event_id='jkenwahvsaurswizchdz',
            name='lfonfxifqxorlqjxjahx',
            type='mlkgjqcyxekcapwzciry',
            url='drzoxkfxppvfrualiyla',
            locale='hqpmfvdwxkmopiduoitd',
            start_date='yyyoypaoljtvtxlvpdwj',
            start_time='bwpurylnoupsxtzvgalk',
            start_datetime_local='kkzdokmypmwekjmxtuxf',
            start_datetime_utc='mknwyswfexyhmchjsnfm',
            status='bnmtchivmodzdhjttxeb',
            segment_id='dzwtcesurqvqcbiygrrd',
            segment_name='pbsuczsttolvfjhlmlor',
            genre_id='kmnznkqltapzkncnkdjh',
            genre_name='gyenaatjusfqvqgrobgv',
            subgenre_id='teplfutvmgrbteuuqsmr',
            subgenre_name='sdfkctlfgbjnnlynhmfg',
            venue_id='dldjwvxblqzivbepmnoq',
            venue_name='vmaoquqpeihfyeghidrs',
            venue_city='udqghagatzuvyfvrdbhr',
            venue_state_code='qogwytkhnalwvumpydjd',
            venue_country_code='njlsbwyjotdgmyxczkwb',
            venue_latitude=float(22.287147999887413),
            venue_longitude=float(31.616574426338463),
            price_min=float(87.34521388987434),
            price_max=float(73.86910717638786),
            currency='bfiijcygzjvkgtvxpvjf',
            attraction_ids='myswbdluppugfexccgoe',
            attraction_names='thysxzbopmqyjvwgygnf',
            onsale_start_datetime='xafirldseenimoaomwdi',
            onsale_end_datetime='fixakozipcredtyhlfxj',
            info='ofryswcbpsxjdhuztion',
            please_note='ivmdnitiqeayuyomlncc'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'jkenwahvsaurswizchdz'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'lfonfxifqxorlqjxjahx'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'mlkgjqcyxekcapwzciry'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'drzoxkfxppvfrualiyla'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'hqpmfvdwxkmopiduoitd'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'yyyoypaoljtvtxlvpdwj'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'bwpurylnoupsxtzvgalk'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_start_datetime_local_property(self):
        """
        Test start_datetime_local property
        """
        test_value = 'kkzdokmypmwekjmxtuxf'
        self.instance.start_datetime_local = test_value
        self.assertEqual(self.instance.start_datetime_local, test_value)
    
    def test_start_datetime_utc_property(self):
        """
        Test start_datetime_utc property
        """
        test_value = 'mknwyswfexyhmchjsnfm'
        self.instance.start_datetime_utc = test_value
        self.assertEqual(self.instance.start_datetime_utc, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'bnmtchivmodzdhjttxeb'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'dzwtcesurqvqcbiygrrd'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)
    
    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'pbsuczsttolvfjhlmlor'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)
    
    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'kmnznkqltapzkncnkdjh'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)
    
    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'gyenaatjusfqvqgrobgv'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)
    
    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'teplfutvmgrbteuuqsmr'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)
    
    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'sdfkctlfgbjnnlynhmfg'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'dldjwvxblqzivbepmnoq'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'vmaoquqpeihfyeghidrs'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'udqghagatzuvyfvrdbhr'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_state_code_property(self):
        """
        Test venue_state_code property
        """
        test_value = 'qogwytkhnalwvumpydjd'
        self.instance.venue_state_code = test_value
        self.assertEqual(self.instance.venue_state_code, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'njlsbwyjotdgmyxczkwb'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)
    
    def test_venue_latitude_property(self):
        """
        Test venue_latitude property
        """
        test_value = float(22.287147999887413)
        self.instance.venue_latitude = test_value
        self.assertEqual(self.instance.venue_latitude, test_value)
    
    def test_venue_longitude_property(self):
        """
        Test venue_longitude property
        """
        test_value = float(31.616574426338463)
        self.instance.venue_longitude = test_value
        self.assertEqual(self.instance.venue_longitude, test_value)
    
    def test_price_min_property(self):
        """
        Test price_min property
        """
        test_value = float(87.34521388987434)
        self.instance.price_min = test_value
        self.assertEqual(self.instance.price_min, test_value)
    
    def test_price_max_property(self):
        """
        Test price_max property
        """
        test_value = float(73.86910717638786)
        self.instance.price_max = test_value
        self.assertEqual(self.instance.price_max, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'bfiijcygzjvkgtvxpvjf'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_attraction_ids_property(self):
        """
        Test attraction_ids property
        """
        test_value = 'myswbdluppugfexccgoe'
        self.instance.attraction_ids = test_value
        self.assertEqual(self.instance.attraction_ids, test_value)
    
    def test_attraction_names_property(self):
        """
        Test attraction_names property
        """
        test_value = 'thysxzbopmqyjvwgygnf'
        self.instance.attraction_names = test_value
        self.assertEqual(self.instance.attraction_names, test_value)
    
    def test_onsale_start_datetime_property(self):
        """
        Test onsale_start_datetime property
        """
        test_value = 'xafirldseenimoaomwdi'
        self.instance.onsale_start_datetime = test_value
        self.assertEqual(self.instance.onsale_start_datetime, test_value)
    
    def test_onsale_end_datetime_property(self):
        """
        Test onsale_end_datetime property
        """
        test_value = 'fixakozipcredtyhlfxj'
        self.instance.onsale_end_datetime = test_value
        self.assertEqual(self.instance.onsale_end_datetime, test_value)
    
    def test_info_property(self):
        """
        Test info property
        """
        test_value = 'ofryswcbpsxjdhuztion'
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)
    
    def test_please_note_property(self):
        """
        Test please_note property
        """
        test_value = 'ivmdnitiqeayuyomlncc'
        self.instance.please_note = test_value
        self.assertEqual(self.instance.please_note, test_value)
    
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

