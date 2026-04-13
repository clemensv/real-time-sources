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
            event_id='abfbusokmwpnebnizxea',
            name='lqtfsdkfgdizyqclutmt',
            type='jdmezazaqgnksrxpytwb',
            url='vzowzigakzcwsmuavrir',
            locale='iadhxuwdzymhpjqeqdmb',
            start_date='jmtlevgglvcihznpxphf',
            start_time='ihwufkcmuxpmvhadyzwo',
            start_datetime_local='hudfvoqvtyrfgrvrtbny',
            start_datetime_utc='ugwbswcwynkzsbsydcij',
            status='bvqwxssdpovwzrssmvkj',
            segment_id='eawqmrneobhnccwgsazv',
            segment_name='ehcqhlhjqcwdgkphuoku',
            genre_id='jdaiyrodlfcnqtbgyofo',
            genre_name='sutcffhioktxczkfgnpa',
            subgenre_id='zljrqzpwduhzruvwehbc',
            subgenre_name='upbrsrbqvmltkuqizmad',
            venue_id='kunyarbptdreqmqrvnfv',
            venue_name='uifalcaygbbladgdmwyt',
            venue_city='tfdvmfsxmzvyrhsvlnua',
            venue_state_code='wdxbhxhfprgaalxlzsef',
            venue_country_code='ujshyxljddqmpzoidasr',
            venue_latitude=float(79.44932089373728),
            venue_longitude=float(22.62185428085497),
            price_min=float(1.435436150177849),
            price_max=float(13.034062412872949),
            currency='xsslkrfdnsnanjoxnold',
            attraction_ids='zgnzhfrfaulvwoakdmwy',
            attraction_names='aopdrzlhyryjczrjzdvz',
            onsale_start_datetime='qyljhzibkdpmryxrpbvm',
            onsale_end_datetime='argebrzyyypwrsavrpjd',
            info='zayrywqhbtsajnejuunt',
            please_note='hmgbopfebzziirchxhag'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'abfbusokmwpnebnizxea'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'lqtfsdkfgdizyqclutmt'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'jdmezazaqgnksrxpytwb'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'vzowzigakzcwsmuavrir'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'iadhxuwdzymhpjqeqdmb'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'jmtlevgglvcihznpxphf'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'ihwufkcmuxpmvhadyzwo'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_start_datetime_local_property(self):
        """
        Test start_datetime_local property
        """
        test_value = 'hudfvoqvtyrfgrvrtbny'
        self.instance.start_datetime_local = test_value
        self.assertEqual(self.instance.start_datetime_local, test_value)
    
    def test_start_datetime_utc_property(self):
        """
        Test start_datetime_utc property
        """
        test_value = 'ugwbswcwynkzsbsydcij'
        self.instance.start_datetime_utc = test_value
        self.assertEqual(self.instance.start_datetime_utc, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'bvqwxssdpovwzrssmvkj'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'eawqmrneobhnccwgsazv'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)
    
    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'ehcqhlhjqcwdgkphuoku'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)
    
    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'jdaiyrodlfcnqtbgyofo'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)
    
    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'sutcffhioktxczkfgnpa'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)
    
    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'zljrqzpwduhzruvwehbc'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)
    
    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'upbrsrbqvmltkuqizmad'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'kunyarbptdreqmqrvnfv'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'uifalcaygbbladgdmwyt'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'tfdvmfsxmzvyrhsvlnua'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_state_code_property(self):
        """
        Test venue_state_code property
        """
        test_value = 'wdxbhxhfprgaalxlzsef'
        self.instance.venue_state_code = test_value
        self.assertEqual(self.instance.venue_state_code, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'ujshyxljddqmpzoidasr'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)
    
    def test_venue_latitude_property(self):
        """
        Test venue_latitude property
        """
        test_value = float(79.44932089373728)
        self.instance.venue_latitude = test_value
        self.assertEqual(self.instance.venue_latitude, test_value)
    
    def test_venue_longitude_property(self):
        """
        Test venue_longitude property
        """
        test_value = float(22.62185428085497)
        self.instance.venue_longitude = test_value
        self.assertEqual(self.instance.venue_longitude, test_value)
    
    def test_price_min_property(self):
        """
        Test price_min property
        """
        test_value = float(1.435436150177849)
        self.instance.price_min = test_value
        self.assertEqual(self.instance.price_min, test_value)
    
    def test_price_max_property(self):
        """
        Test price_max property
        """
        test_value = float(13.034062412872949)
        self.instance.price_max = test_value
        self.assertEqual(self.instance.price_max, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'xsslkrfdnsnanjoxnold'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_attraction_ids_property(self):
        """
        Test attraction_ids property
        """
        test_value = 'zgnzhfrfaulvwoakdmwy'
        self.instance.attraction_ids = test_value
        self.assertEqual(self.instance.attraction_ids, test_value)
    
    def test_attraction_names_property(self):
        """
        Test attraction_names property
        """
        test_value = 'aopdrzlhyryjczrjzdvz'
        self.instance.attraction_names = test_value
        self.assertEqual(self.instance.attraction_names, test_value)
    
    def test_onsale_start_datetime_property(self):
        """
        Test onsale_start_datetime property
        """
        test_value = 'qyljhzibkdpmryxrpbvm'
        self.instance.onsale_start_datetime = test_value
        self.assertEqual(self.instance.onsale_start_datetime, test_value)
    
    def test_onsale_end_datetime_property(self):
        """
        Test onsale_end_datetime property
        """
        test_value = 'argebrzyyypwrsavrpjd'
        self.instance.onsale_end_datetime = test_value
        self.assertEqual(self.instance.onsale_end_datetime, test_value)
    
    def test_info_property(self):
        """
        Test info property
        """
        test_value = 'zayrywqhbtsajnejuunt'
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)
    
    def test_please_note_property(self):
        """
        Test please_note property
        """
        test_value = 'hmgbopfebzziirchxhag'
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
