"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from ticketmaster_producer_data.ticketmaster.events.event import Event


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
            event_id='avqgikcxmmhzrpyvzfqn',
            name='urxccgzovwamohbzagxb',
            type='qtwaazqookfiwrwpylvs',
            url='jhyqvczhplbrqrxsklsr',
            locale='uhbifljckkukqkldseni',
            start_date='cjabhomvsbjedahvduzc',
            start_time='gvtqbmpjdhhdufmifyci',
            start_datetime_local='iyglmnbitxrlrubfjsko',
            start_datetime_utc='cwbugrymajxnkelgjuip',
            status='tvkanykuauldtxdfbusb',
            segment_id='voacprchgonyuijczxgc',
            segment_name='brdciicxictbfxcbcpcl',
            genre_id='qswzfgialdtpvdgexaiq',
            genre_name='wcrbeycjcpdmcanmijve',
            subgenre_id='hbuscsrlcljhmwmaovbf',
            subgenre_name='frxdpbnfcguxdcvfeeia',
            venue_id='xyiobsrqfddvzycmscmt',
            venue_name='swjywexmupbsxaxmwshp',
            venue_city='blqxvijalbqgnrzwfxwi',
            venue_state_code='ihubmeinenmhdltugpop',
            venue_country_code='njmpmqzotlujnkabcqjn',
            venue_latitude=float(71.66058974522358),
            venue_longitude=float(74.61272902846719),
            price_min=float(72.56107294441185),
            price_max=float(22.13832233509204),
            currency='txczogkuamoziuwmqjxc',
            attraction_ids='yhsnghnzkuevpcrpmgrh',
            attraction_names='ejxeqbfgowlnomkboscz',
            onsale_start_datetime='mclwgeggqxlydgkliizq',
            onsale_end_datetime='vmkafbccspqifsimagcc',
            info='hjvckgodkhlydjhehduy',
            please_note='ormnlqxbiydeuntuaywg'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'avqgikcxmmhzrpyvzfqn'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'urxccgzovwamohbzagxb'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'qtwaazqookfiwrwpylvs'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'jhyqvczhplbrqrxsklsr'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'uhbifljckkukqkldseni'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'cjabhomvsbjedahvduzc'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'gvtqbmpjdhhdufmifyci'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_start_datetime_local_property(self):
        """
        Test start_datetime_local property
        """
        test_value = 'iyglmnbitxrlrubfjsko'
        self.instance.start_datetime_local = test_value
        self.assertEqual(self.instance.start_datetime_local, test_value)
    
    def test_start_datetime_utc_property(self):
        """
        Test start_datetime_utc property
        """
        test_value = 'cwbugrymajxnkelgjuip'
        self.instance.start_datetime_utc = test_value
        self.assertEqual(self.instance.start_datetime_utc, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'tvkanykuauldtxdfbusb'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'voacprchgonyuijczxgc'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)
    
    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'brdciicxictbfxcbcpcl'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)
    
    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'qswzfgialdtpvdgexaiq'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)
    
    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'wcrbeycjcpdmcanmijve'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)
    
    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'hbuscsrlcljhmwmaovbf'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)
    
    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'frxdpbnfcguxdcvfeeia'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'xyiobsrqfddvzycmscmt'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'swjywexmupbsxaxmwshp'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'blqxvijalbqgnrzwfxwi'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_state_code_property(self):
        """
        Test venue_state_code property
        """
        test_value = 'ihubmeinenmhdltugpop'
        self.instance.venue_state_code = test_value
        self.assertEqual(self.instance.venue_state_code, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'njmpmqzotlujnkabcqjn'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)
    
    def test_venue_latitude_property(self):
        """
        Test venue_latitude property
        """
        test_value = float(71.66058974522358)
        self.instance.venue_latitude = test_value
        self.assertEqual(self.instance.venue_latitude, test_value)
    
    def test_venue_longitude_property(self):
        """
        Test venue_longitude property
        """
        test_value = float(74.61272902846719)
        self.instance.venue_longitude = test_value
        self.assertEqual(self.instance.venue_longitude, test_value)
    
    def test_price_min_property(self):
        """
        Test price_min property
        """
        test_value = float(72.56107294441185)
        self.instance.price_min = test_value
        self.assertEqual(self.instance.price_min, test_value)
    
    def test_price_max_property(self):
        """
        Test price_max property
        """
        test_value = float(22.13832233509204)
        self.instance.price_max = test_value
        self.assertEqual(self.instance.price_max, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'txczogkuamoziuwmqjxc'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_attraction_ids_property(self):
        """
        Test attraction_ids property
        """
        test_value = 'yhsnghnzkuevpcrpmgrh'
        self.instance.attraction_ids = test_value
        self.assertEqual(self.instance.attraction_ids, test_value)
    
    def test_attraction_names_property(self):
        """
        Test attraction_names property
        """
        test_value = 'ejxeqbfgowlnomkboscz'
        self.instance.attraction_names = test_value
        self.assertEqual(self.instance.attraction_names, test_value)
    
    def test_onsale_start_datetime_property(self):
        """
        Test onsale_start_datetime property
        """
        test_value = 'mclwgeggqxlydgkliizq'
        self.instance.onsale_start_datetime = test_value
        self.assertEqual(self.instance.onsale_start_datetime, test_value)
    
    def test_onsale_end_datetime_property(self):
        """
        Test onsale_end_datetime property
        """
        test_value = 'vmkafbccspqifsimagcc'
        self.instance.onsale_end_datetime = test_value
        self.assertEqual(self.instance.onsale_end_datetime, test_value)
    
    def test_info_property(self):
        """
        Test info property
        """
        test_value = 'hjvckgodkhlydjhehduy'
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)
    
    def test_please_note_property(self):
        """
        Test please_note property
        """
        test_value = 'ormnlqxbiydeuntuaywg'
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

