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
            event_id='ykxonaxovkiezlkqlgee',
            name='qasljfqbolsbocbwtklc',
            start='anrtocqcgxobjyxxlgta',
            end='elctiejdruqmoglfjaxv',
            duration_text='fehxtrpxydsemvpxghol',
            time_notes='cswcwrdgzyfzypedkluh',
            event_status='mkfaglfglillmefzjlmw',
            sale_status='vikfioegqpecweptaglw',
            attendance_mode='jcdiljdojcwojzggebdq',
            venue_name='fqklfgnaewbynulqhibb',
            venue_id='wdjcnzufssbbjciemisd',
            address='eylmbotltcecbsyzalyo',
            postal_code='kfflrgzaewwzqujjttam',
            description='hxgslyoyuenvakhemhtd',
            url='pyqswwkislsvwyijargd',
            buy_tickets_url='elmuezyutcxrizropzvq',
            image_url='gvajafnrhvdikyurzxmn',
            image_small_url='hihymjgoqqszlyickvhh',
            series_id='ckrpusxwjpobosactsuy',
            organizer_name='ttbixalbmddewhaqkkwy',
            organizer_phone='daowwhugulwqlbeibzhg',
            organizer_email='zeoaiiozijoyzbdsdwqb',
            organizer_id=int(95),
            categories=['vlezhcrftuqmsmirmrxy', 'gputgdzxomztetaamcdg', 'ewprpqtwkzdsimbzdvat', 'gqbpsizvexxvamaefouk', 'uyyyycgtltczymtfoihp']
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'ykxonaxovkiezlkqlgee'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'qasljfqbolsbocbwtklc'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'anrtocqcgxobjyxxlgta'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_end_property(self):
        """
        Test end property
        """
        test_value = 'elctiejdruqmoglfjaxv'
        self.instance.end = test_value
        self.assertEqual(self.instance.end, test_value)
    
    def test_duration_text_property(self):
        """
        Test duration_text property
        """
        test_value = 'fehxtrpxydsemvpxghol'
        self.instance.duration_text = test_value
        self.assertEqual(self.instance.duration_text, test_value)
    
    def test_time_notes_property(self):
        """
        Test time_notes property
        """
        test_value = 'cswcwrdgzyfzypedkluh'
        self.instance.time_notes = test_value
        self.assertEqual(self.instance.time_notes, test_value)
    
    def test_event_status_property(self):
        """
        Test event_status property
        """
        test_value = 'mkfaglfglillmefzjlmw'
        self.instance.event_status = test_value
        self.assertEqual(self.instance.event_status, test_value)
    
    def test_sale_status_property(self):
        """
        Test sale_status property
        """
        test_value = 'vikfioegqpecweptaglw'
        self.instance.sale_status = test_value
        self.assertEqual(self.instance.sale_status, test_value)
    
    def test_attendance_mode_property(self):
        """
        Test attendance_mode property
        """
        test_value = 'jcdiljdojcwojzggebdq'
        self.instance.attendance_mode = test_value
        self.assertEqual(self.instance.attendance_mode, test_value)
    
    def test_venue_name_property(self):
        """
        Test venue_name property
        """
        test_value = 'fqklfgnaewbynulqhibb'
        self.instance.venue_name = test_value
        self.assertEqual(self.instance.venue_name, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'wdjcnzufssbbjciemisd'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_address_property(self):
        """
        Test address property
        """
        test_value = 'eylmbotltcecbsyzalyo'
        self.instance.address = test_value
        self.assertEqual(self.instance.address, test_value)
    
    def test_postal_code_property(self):
        """
        Test postal_code property
        """
        test_value = 'kfflrgzaewwzqujjttam'
        self.instance.postal_code = test_value
        self.assertEqual(self.instance.postal_code, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'hxgslyoyuenvakhemhtd'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'pyqswwkislsvwyijargd'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_buy_tickets_url_property(self):
        """
        Test buy_tickets_url property
        """
        test_value = 'elmuezyutcxrizropzvq'
        self.instance.buy_tickets_url = test_value
        self.assertEqual(self.instance.buy_tickets_url, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'gvajafnrhvdikyurzxmn'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_image_small_url_property(self):
        """
        Test image_small_url property
        """
        test_value = 'hihymjgoqqszlyickvhh'
        self.instance.image_small_url = test_value
        self.assertEqual(self.instance.image_small_url, test_value)
    
    def test_series_id_property(self):
        """
        Test series_id property
        """
        test_value = 'ckrpusxwjpobosactsuy'
        self.instance.series_id = test_value
        self.assertEqual(self.instance.series_id, test_value)
    
    def test_organizer_name_property(self):
        """
        Test organizer_name property
        """
        test_value = 'ttbixalbmddewhaqkkwy'
        self.instance.organizer_name = test_value
        self.assertEqual(self.instance.organizer_name, test_value)
    
    def test_organizer_phone_property(self):
        """
        Test organizer_phone property
        """
        test_value = 'daowwhugulwqlbeibzhg'
        self.instance.organizer_phone = test_value
        self.assertEqual(self.instance.organizer_phone, test_value)
    
    def test_organizer_email_property(self):
        """
        Test organizer_email property
        """
        test_value = 'zeoaiiozijoyzbdsdwqb'
        self.instance.organizer_email = test_value
        self.assertEqual(self.instance.organizer_email, test_value)
    
    def test_organizer_id_property(self):
        """
        Test organizer_id property
        """
        test_value = int(95)
        self.instance.organizer_id = test_value
        self.assertEqual(self.instance.organizer_id, test_value)
    
    def test_categories_property(self):
        """
        Test categories property
        """
        test_value = ['vlezhcrftuqmsmirmrxy', 'gputgdzxomztetaamcdg', 'ewprpqtwkzdsimbzdvat', 'gqbpsizvexxvamaefouk', 'uyyyycgtltczymtfoihp']
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

