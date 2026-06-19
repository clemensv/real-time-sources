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
            event_id='vgkrvbnofjdefxmitfld',
            name='lwxxrokhpkegmudcxdes',
            type='tomyuumnkgowdpfqeogp',
            url='qtcoathypuqbkdmnnwer',
            locale='ohaasxlwdhehqgqjhoja',
            start_date='ydueoshecbobfooilnph',
            start_time='jlcesdgdzdbstccdinqk',
            start_datetime_local='ceznntwlyvsjhvwfdlyh',
            start_datetime_utc='kiqwessqkyxjvgypgwzz',
            status='mgnvgcoqjivogyxtmqdk',
            segment_id='mdowdoljloatjzlhfxlm',
            segment_name='sbbpizeeiacoqguyufqv',
            genre_id='orziwabvswbrqftydmoq',
            genre_name='rmlwpifozkuluqroqxkb',
            subgenre_id='zsgfkpoprqcvlxxwsbdb',
            subgenre_name='yqouzsmhnqhtrpfjizoe',
            venue_id='saoayalhrurdwykxyzuk',
            venue_name='ipbctymcwcojtckndchr',
            venue_city='wutlnmkfsdctxlpzgbfp',
            venue_state_code='zlnszspqwtoxzmlomwiz',
            venue_country_code='paqhuovohbsadlsozclq',
            venue_latitude=float(74.64153530051708),
            venue_longitude=float(14.349624452022736),
            price_min=float(69.41983800415973),
            price_max=float(60.86624191040811),
            currency='ztzjsbuuzjouaolxrlkg',
            attraction_ids='ijvwlomkgaembixngjyy',
            attraction_names='qrctbyqlnhedeufttfvq',
            onsale_start_datetime='vomkdcckmgtkkfjfyrdr',
            onsale_end_datetime='xwvnlljunurhdwjgxyge',
            info='wbileafkmcegwixjvssr',
            please_note='hscinhdcjomwgwcveuog'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'vgkrvbnofjdefxmitfld'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'lwxxrokhpkegmudcxdes'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_type_property(self):
        """
        Test type property
        """
        test_value = 'tomyuumnkgowdpfqeogp'
        self.instance.type = test_value
        self.assertEqual(self.instance.type, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'qtcoathypuqbkdmnnwer'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_locale_property(self):
        """
        Test locale property
        """
        test_value = 'ohaasxlwdhehqgqjhoja'
        self.instance.locale = test_value
        self.assertEqual(self.instance.locale, test_value)
    
    def test_start_date_property(self):
        """
        Test start_date property
        """
        test_value = 'ydueoshecbobfooilnph'
        self.instance.start_date = test_value
        self.assertEqual(self.instance.start_date, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'jlcesdgdzdbstccdinqk'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_start_datetime_local_property(self):
        """
        Test start_datetime_local property
        """
        test_value = 'ceznntwlyvsjhvwfdlyh'
        self.instance.start_datetime_local = test_value
        self.assertEqual(self.instance.start_datetime_local, test_value)
    
    def test_start_datetime_utc_property(self):
        """
        Test start_datetime_utc property
        """
        test_value = 'kiqwessqkyxjvgypgwzz'
        self.instance.start_datetime_utc = test_value
        self.assertEqual(self.instance.start_datetime_utc, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'mgnvgcoqjivogyxtmqdk'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_segment_id_property(self):
        """
        Test segment_id property
        """
        test_value = 'mdowdoljloatjzlhfxlm'
        self.instance.segment_id = test_value
        self.assertEqual(self.instance.segment_id, test_value)
    
    def test_segment_name_property(self):
        """
        Test segment_name property
        """
        test_value = 'sbbpizeeiacoqguyufqv'
        self.instance.segment_name = test_value
        self.assertEqual(self.instance.segment_name, test_value)
    
    def test_genre_id_property(self):
        """
        Test genre_id property
        """
        test_value = 'orziwabvswbrqftydmoq'
        self.instance.genre_id = test_value
        self.assertEqual(self.instance.genre_id, test_value)
    
    def test_genre_name_property(self):
        """
        Test genre_name property
        """
        test_value = 'rmlwpifozkuluqroqxkb'
        self.instance.genre_name = test_value
        self.assertEqual(self.instance.genre_name, test_value)
    
    def test_subgenre_id_property(self):
        """
        Test subgenre_id property
        """
        test_value = 'zsgfkpoprqcvlxxwsbdb'
        self.instance.subgenre_id = test_value
        self.assertEqual(self.instance.subgenre_id, test_value)
    
    def test_subgenre_name_property(self):
        """
        Test subgenre_name property
        """
        test_value = 'yqouzsmhnqhtrpfjizoe'
        self.instance.subgenre_name = test_value
        self.assertEqual(self.instance.subgenre_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'saoayalhrurdwykxyzuk'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'ipbctymcwcojtckndchr'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_city_property(self):
        """
        Test venue_city property
        """
        test_value = 'wutlnmkfsdctxlpzgbfp'
        self.instance.venue_city = test_value
        self.assertEqual(self.instance.venue_city, test_value)
    
    def test_venue_state_code_property(self):
        """
        Test venue_state_code property
        """
        test_value = 'zlnszspqwtoxzmlomwiz'
        self.instance.venue_state_code = test_value
        self.assertEqual(self.instance.venue_state_code, test_value)
    
    def test_venue_country_code_property(self):
        """
        Test venue_country_code property
        """
        test_value = 'paqhuovohbsadlsozclq'
        self.instance.venue_country_code = test_value
        self.assertEqual(self.instance.venue_country_code, test_value)
    
    def test_venue_latitude_property(self):
        """
        Test venue_latitude property
        """
        test_value = float(74.64153530051708)
        self.instance.venue_latitude = test_value
        self.assertEqual(self.instance.venue_latitude, test_value)
    
    def test_venue_longitude_property(self):
        """
        Test venue_longitude property
        """
        test_value = float(14.349624452022736)
        self.instance.venue_longitude = test_value
        self.assertEqual(self.instance.venue_longitude, test_value)
    
    def test_price_min_property(self):
        """
        Test price_min property
        """
        test_value = float(69.41983800415973)
        self.instance.price_min = test_value
        self.assertEqual(self.instance.price_min, test_value)
    
    def test_price_max_property(self):
        """
        Test price_max property
        """
        test_value = float(60.86624191040811)
        self.instance.price_max = test_value
        self.assertEqual(self.instance.price_max, test_value)
    
    def test_currency_property(self):
        """
        Test currency property
        """
        test_value = 'ztzjsbuuzjouaolxrlkg'
        self.instance.currency = test_value
        self.assertEqual(self.instance.currency, test_value)
    
    def test_attraction_ids_property(self):
        """
        Test attraction_ids property
        """
        test_value = 'ijvwlomkgaembixngjyy'
        self.instance.attraction_ids = test_value
        self.assertEqual(self.instance.attraction_ids, test_value)
    
    def test_attraction_names_property(self):
        """
        Test attraction_names property
        """
        test_value = 'qrctbyqlnhedeufttfvq'
        self.instance.attraction_names = test_value
        self.assertEqual(self.instance.attraction_names, test_value)
    
    def test_onsale_start_datetime_property(self):
        """
        Test onsale_start_datetime property
        """
        test_value = 'vomkdcckmgtkkfjfyrdr'
        self.instance.onsale_start_datetime = test_value
        self.assertEqual(self.instance.onsale_start_datetime, test_value)
    
    def test_onsale_end_datetime_property(self):
        """
        Test onsale_end_datetime property
        """
        test_value = 'xwvnlljunurhdwjgxyge'
        self.instance.onsale_end_datetime = test_value
        self.assertEqual(self.instance.onsale_end_datetime, test_value)
    
    def test_info_property(self):
        """
        Test info property
        """
        test_value = 'wbileafkmcegwixjvssr'
        self.instance.info = test_value
        self.assertEqual(self.instance.info, test_value)
    
    def test_please_note_property(self):
        """
        Test please_note property
        """
        test_value = 'hscinhdcjomwgwcveuog'
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

