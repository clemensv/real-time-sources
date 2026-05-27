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
            event_id='oatulgbjvdwciarojpct',
            name='secpmslwpvdvulkfscdx',
            type='mbiaegmtfcdicdnxvezs',
            url='tifthihejgqleiunuqsx',
            locale='erexaamvwscmopqgvbzk',
            start_date='olgqjmkopidbfgcuxfwp',
            start_time='hgwqzgyxhzgrvurcgyii',
            start_datetime_local='ucocaqjprrnxsleyfyso',
            start_datetime_utc='vztsoggacczrsgexwyev',
            status='hayaqjzcrqkiwboailvn',
            segment_id='mlomhwjlwqvwzzgbosul',
            segment_name='dvvfpjicuorhnhtrkfho',
            genre_id='fzuhlmfpixjtdskqfgao',
            genre_name='frlheieeqjmjfrvvhpvx',
            subgenre_id='aclwidwpjepjhpicpttd',
            subgenre_name='rjybwatgjazsszgrjqau',
            venue_id='umlzygbtlgyaxjgwatit',
            venue_name='hmflmkirwpvdvvfgslgk',
            venue_city='kzkzpknoouoeansluews',
            venue_state_code='njvkqrmhqcppkmspswec',
            venue_country_code='nrkxmbovqijncaaarjas',
            venue_latitude=float(84.16199084528114),
            venue_longitude=float(61.29147660639873),
            price_min=float(90.11689938541436),
            price_max=float(77.61775090876682),
            currency='omluthuzlyydtmpffdyj',
            attraction_ids='vsrntmrpgkoewtmymgpa',
            attraction_names='cfodqibwonzphcvyjoud',
            onsale_start_datetime='ucctsahwdhdakbcqkcez',
            onsale_end_datetime='kinonyymomhxswuedbwb',
            info='hkpfgicpuftjhvkhdqrf',
            please_note='bwzpmnxzyeeewpmugmcv'
        )
        return instance


    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'oatulgbjvdwciarojpct'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)

    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'secpmslwpvdvulkfscdx'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)

    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'mbiaegmtfcdicdnxvezs'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)

    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'tifthihejgqleiunuqsx'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)

    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'erexaamvwscmopqgvbzk'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)

    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'olgqjmkopidbfgcuxfwp'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)

    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'hgwqzgyxhzgrvurcgyii'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)

    def test_start_datetime_local_property(self):
        """
        Test start_datetime_local property
        """
        test_value = 'ucocaqjprrnxsleyfyso'
        self.instance.start_datetime_local = test_value
        self.assertEqual(self.instance.start_datetime_local, test_value)

    def test_start_datetime_utc_property(self):
        """
        Test start_datetime_utc property
        """
        test_value = 'vztsoggacczrsgexwyev'
        self.instance.start_datetime_utc = test_value
        self.assertEqual(self.instance.start_datetime_utc, test_value)

    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'hayaqjzcrqkiwboailvn'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)

    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'mlomhwjlwqvwzzgbosul'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)

    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'dvvfpjicuorhnhtrkfho'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)

    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'fzuhlmfpixjtdskqfgao'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)

    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'frlheieeqjmjfrvvhpvx'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)

    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'aclwidwpjepjhpicpttd'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)

    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'rjybwatgjazsszgrjqau'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)

    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'umlzygbtlgyaxjgwatit'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)

    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'hmflmkirwpvdvvfgslgk'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)

    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'kzkzpknoouoeansluews'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)

    def test_venue_state_code_property(self):
        """
        Test venue_state_code property
        """
        test_value = 'njvkqrmhqcppkmspswec'
        self.instance.venue_state_code = test_value
        self.assertEqual(self.instance.venue_state_code, test_value)

    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'nrkxmbovqijncaaarjas'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)

    def test_venue_latitude_property(self):
        """
        Test venue_latitude property
        """
        test_value = float(84.16199084528114)
        self.instance.venue_latitude = test_value
        self.assertEqual(self.instance.venue_latitude, test_value)

    def test_venue_longitude_property(self):
        """
        Test venue_longitude property
        """
        test_value = float(61.29147660639873)
        self.instance.venue_longitude = test_value
        self.assertEqual(self.instance.venue_longitude, test_value)

    def test_price_min_property(self):
        """
        Test price_min property
        """
        test_value = float(90.11689938541436)
        self.instance.price_min = test_value
        self.assertEqual(self.instance.price_min, test_value)

    def test_price_max_property(self):
        """
        Test price_max property
        """
        test_value = float(77.61775090876682)
        self.instance.price_max = test_value
        self.assertEqual(self.instance.price_max, test_value)

    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'omluthuzlyydtmpffdyj'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)

    def test_attraction_ids_property(self):
        """
        Test attraction_ids property
        """
        test_value = 'vsrntmrpgkoewtmymgpa'
        self.instance.attraction_ids = test_value
        self.assertEqual(self.instance.attraction_ids, test_value)

    def test_attraction_names_property(self):
        """
        Test attraction_names property
        """
        test_value = 'cfodqibwonzphcvyjoud'
        self.instance.attraction_names = test_value
        self.assertEqual(self.instance.attraction_names, test_value)

    def test_onsale_start_datetime_property(self):
        """
        Test onsale_start_datetime property
        """
        test_value = 'ucctsahwdhdakbcqkcez'
        self.instance.onsale_start_datetime = test_value
        self.assertEqual(self.instance.onsale_start_datetime, test_value)

    def test_onsale_end_datetime_property(self):
        """
        Test onsale_end_datetime property
        """
        test_value = 'kinonyymomhxswuedbwb'
        self.instance.onsale_end_datetime = test_value
        self.assertEqual(self.instance.onsale_end_datetime, test_value)

    def test_info_property(self):
        """
        Test info property
        """
        test_value = 'hkpfgicpuftjhvkhdqrf'
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)

    def test_please_note_property(self):
        """
        Test please_note property
        """
        test_value = 'bwzpmnxzyeeewpmugmcv'
        self.instance.please_note = test_value
        self.assertEqual(self.instance.please_note, test_value)

    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Event.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
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

