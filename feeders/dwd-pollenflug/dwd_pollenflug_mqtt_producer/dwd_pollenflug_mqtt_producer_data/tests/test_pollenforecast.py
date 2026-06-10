"""
Test case for PollenForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_pollenflug_mqtt_producer_data.pollenforecast import PollenForecast


class Test_PollenForecast(unittest.TestCase):
    """
    Test case for PollenForecast
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PollenForecast.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PollenForecast for testing
        """
        instance = PollenForecast(
            region_id='doxuiquxojqmsuqllibb',
            region_name='jttaddplnpgfgzupeyyd',
            last_update='xxxvtcqeycxmjulrmmop',
            next_update='xpmggvldoelpsyrtlupy',
            sender='rerzviupcefdnkbskoun',
            hazel_today='evobqcgbsmduevhyemxt',
            hazel_tomorrow='ukpdcgwulqjdqxgttyeb',
            hazel_dayafter_to='zogbhsjnvrsffbenhfqs',
            alder_today='zhenribcapntcjxudbsn',
            alder_tomorrow='exwxgsmvdnlumlbtfred',
            alder_dayafter_to='zaoafoiqekhipfxhklkr',
            birch_today='magraastndwadoozogji',
            birch_tomorrow='caocwqstrzwyvimrnhoo',
            birch_dayafter_to='vznhxosbzwpzvhubyhwo',
            ash_today='zbcvstkyhmaaqewyaqrx',
            ash_tomorrow='wolhaalyznnptzwjufrf',
            ash_dayafter_to='surfdpogaouhgotcqjhd',
            grasses_today='dbtvjnecosenyqbudpae',
            grasses_tomorrow='qnuyozquygybuqpnjqst',
            grasses_dayafter_to='kaempdgwegalszkkqkkp',
            rye_today='hpjczxthyimmaeqjuwsn',
            rye_tomorrow='rwofvqsyacfjcehbmimm',
            rye_dayafter_to='azxbmmixdlnyiuljtxay',
            mugwort_today='eyrogkckidtywfdlhfdj',
            mugwort_tomorrow='kkldfjnnukgqzdfctlgo',
            mugwort_dayafter_to='rgnortrbkhzyqmcoapzc',
            ragweed_today='nymcftouopavkjfncypq',
            ragweed_tomorrow='jufcdxwjvpfjyajobqrz',
            ragweed_dayafter_to='jpfyiukvaprsgkvvojej',
            pollen_type='gmccshvnahqdrnzzlkcg'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'doxuiquxojqmsuqllibb'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'jttaddplnpgfgzupeyyd'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_last_update_property(self):
        """
        Test last_update property
        """
        test_value = 'xxxvtcqeycxmjulrmmop'
        self.instance.last_update = test_value
        self.assertEqual(self.instance.last_update, test_value)
    
    def test_next_update_property(self):
        """
        Test next_update property
        """
        test_value = 'xpmggvldoelpsyrtlupy'
        self.instance.next_update = test_value
        self.assertEqual(self.instance.next_update, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'rerzviupcefdnkbskoun'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_hazel_today_property(self):
        """
        Test hazel_today property
        """
        test_value = 'evobqcgbsmduevhyemxt'
        self.instance.hazel_today = test_value
        self.assertEqual(self.instance.hazel_today, test_value)
    
    def test_hazel_tomorrow_property(self):
        """
        Test hazel_tomorrow property
        """
        test_value = 'ukpdcgwulqjdqxgttyeb'
        self.instance.hazel_tomorrow = test_value
        self.assertEqual(self.instance.hazel_tomorrow, test_value)
    
    def test_hazel_dayafter_to_property(self):
        """
        Test hazel_dayafter_to property
        """
        test_value = 'zogbhsjnvrsffbenhfqs'
        self.instance.hazel_dayafter_to = test_value
        self.assertEqual(self.instance.hazel_dayafter_to, test_value)
    
    def test_alder_today_property(self):
        """
        Test alder_today property
        """
        test_value = 'zhenribcapntcjxudbsn'
        self.instance.alder_today = test_value
        self.assertEqual(self.instance.alder_today, test_value)
    
    def test_alder_tomorrow_property(self):
        """
        Test alder_tomorrow property
        """
        test_value = 'exwxgsmvdnlumlbtfred'
        self.instance.alder_tomorrow = test_value
        self.assertEqual(self.instance.alder_tomorrow, test_value)
    
    def test_alder_dayafter_to_property(self):
        """
        Test alder_dayafter_to property
        """
        test_value = 'zaoafoiqekhipfxhklkr'
        self.instance.alder_dayafter_to = test_value
        self.assertEqual(self.instance.alder_dayafter_to, test_value)
    
    def test_birch_today_property(self):
        """
        Test birch_today property
        """
        test_value = 'magraastndwadoozogji'
        self.instance.birch_today = test_value
        self.assertEqual(self.instance.birch_today, test_value)
    
    def test_birch_tomorrow_property(self):
        """
        Test birch_tomorrow property
        """
        test_value = 'caocwqstrzwyvimrnhoo'
        self.instance.birch_tomorrow = test_value
        self.assertEqual(self.instance.birch_tomorrow, test_value)
    
    def test_birch_dayafter_to_property(self):
        """
        Test birch_dayafter_to property
        """
        test_value = 'vznhxosbzwpzvhubyhwo'
        self.instance.birch_dayafter_to = test_value
        self.assertEqual(self.instance.birch_dayafter_to, test_value)
    
    def test_ash_today_property(self):
        """
        Test ash_today property
        """
        test_value = 'zbcvstkyhmaaqewyaqrx'
        self.instance.ash_today = test_value
        self.assertEqual(self.instance.ash_today, test_value)
    
    def test_ash_tomorrow_property(self):
        """
        Test ash_tomorrow property
        """
        test_value = 'wolhaalyznnptzwjufrf'
        self.instance.ash_tomorrow = test_value
        self.assertEqual(self.instance.ash_tomorrow, test_value)
    
    def test_ash_dayafter_to_property(self):
        """
        Test ash_dayafter_to property
        """
        test_value = 'surfdpogaouhgotcqjhd'
        self.instance.ash_dayafter_to = test_value
        self.assertEqual(self.instance.ash_dayafter_to, test_value)
    
    def test_grasses_today_property(self):
        """
        Test grasses_today property
        """
        test_value = 'dbtvjnecosenyqbudpae'
        self.instance.grasses_today = test_value
        self.assertEqual(self.instance.grasses_today, test_value)
    
    def test_grasses_tomorrow_property(self):
        """
        Test grasses_tomorrow property
        """
        test_value = 'qnuyozquygybuqpnjqst'
        self.instance.grasses_tomorrow = test_value
        self.assertEqual(self.instance.grasses_tomorrow, test_value)
    
    def test_grasses_dayafter_to_property(self):
        """
        Test grasses_dayafter_to property
        """
        test_value = 'kaempdgwegalszkkqkkp'
        self.instance.grasses_dayafter_to = test_value
        self.assertEqual(self.instance.grasses_dayafter_to, test_value)
    
    def test_rye_today_property(self):
        """
        Test rye_today property
        """
        test_value = 'hpjczxthyimmaeqjuwsn'
        self.instance.rye_today = test_value
        self.assertEqual(self.instance.rye_today, test_value)
    
    def test_rye_tomorrow_property(self):
        """
        Test rye_tomorrow property
        """
        test_value = 'rwofvqsyacfjcehbmimm'
        self.instance.rye_tomorrow = test_value
        self.assertEqual(self.instance.rye_tomorrow, test_value)
    
    def test_rye_dayafter_to_property(self):
        """
        Test rye_dayafter_to property
        """
        test_value = 'azxbmmixdlnyiuljtxay'
        self.instance.rye_dayafter_to = test_value
        self.assertEqual(self.instance.rye_dayafter_to, test_value)
    
    def test_mugwort_today_property(self):
        """
        Test mugwort_today property
        """
        test_value = 'eyrogkckidtywfdlhfdj'
        self.instance.mugwort_today = test_value
        self.assertEqual(self.instance.mugwort_today, test_value)
    
    def test_mugwort_tomorrow_property(self):
        """
        Test mugwort_tomorrow property
        """
        test_value = 'kkldfjnnukgqzdfctlgo'
        self.instance.mugwort_tomorrow = test_value
        self.assertEqual(self.instance.mugwort_tomorrow, test_value)
    
    def test_mugwort_dayafter_to_property(self):
        """
        Test mugwort_dayafter_to property
        """
        test_value = 'rgnortrbkhzyqmcoapzc'
        self.instance.mugwort_dayafter_to = test_value
        self.assertEqual(self.instance.mugwort_dayafter_to, test_value)
    
    def test_ragweed_today_property(self):
        """
        Test ragweed_today property
        """
        test_value = 'nymcftouopavkjfncypq'
        self.instance.ragweed_today = test_value
        self.assertEqual(self.instance.ragweed_today, test_value)
    
    def test_ragweed_tomorrow_property(self):
        """
        Test ragweed_tomorrow property
        """
        test_value = 'jufcdxwjvpfjyajobqrz'
        self.instance.ragweed_tomorrow = test_value
        self.assertEqual(self.instance.ragweed_tomorrow, test_value)
    
    def test_ragweed_dayafter_to_property(self):
        """
        Test ragweed_dayafter_to property
        """
        test_value = 'jpfyiukvaprsgkvvojej'
        self.instance.ragweed_dayafter_to = test_value
        self.assertEqual(self.instance.ragweed_dayafter_to, test_value)
    
    def test_pollen_type_property(self):
        """
        Test pollen_type property
        """
        test_value = 'gmccshvnahqdrnzzlkcg'
        self.instance.pollen_type = test_value
        self.assertEqual(self.instance.pollen_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PollenForecast.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PollenForecast.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

