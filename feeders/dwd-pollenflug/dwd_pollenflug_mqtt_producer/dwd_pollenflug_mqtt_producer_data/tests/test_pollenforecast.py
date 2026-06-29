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
            region_id='guugmhgpyyqmvlpftdnb',
            region_name='ottqsdezejaxgflgaskz',
            last_update='jbgsvzipauksoznmktod',
            next_update='jzannjvbuqtxnlukizyi',
            sender='xnlscukybsaumlaugcfg',
            hazel_today='bpnizhburtnrwtgdlsvk',
            hazel_tomorrow='kpstmaoyukivqrjobczr',
            hazel_dayafter_to='zidovwfogzeloyhkrqzw',
            alder_today='xabnmrcvkxetvgakoflw',
            alder_tomorrow='oxqhlztplkompkanuthx',
            alder_dayafter_to='wzmhbrvhuzjhbowxkhis',
            birch_today='lnwpsazeismzlecpeinf',
            birch_tomorrow='swaqsihbcezvlrjaktzv',
            birch_dayafter_to='rnehsdsisdoqexsqqacp',
            ash_today='eqipsxnbetejblicupxd',
            ash_tomorrow='enunvohopkpnvsjtvkqv',
            ash_dayafter_to='mkcvoxvsvogpbydknarh',
            grasses_today='kzyethddxtvwqtchxhqw',
            grasses_tomorrow='ywrfggycnoyvzjpumkcf',
            grasses_dayafter_to='mytzfscdbegmwkojyajd',
            rye_today='vucivtbqhowztfvsuqhd',
            rye_tomorrow='uswahrfbvumszvguokjr',
            rye_dayafter_to='xkrhtsrqbixrsrzfmgea',
            mugwort_today='ukeakfuyrogezlvxyded',
            mugwort_tomorrow='fzojawirhqkcnizipqet',
            mugwort_dayafter_to='twipbwztgccyvfioljjv',
            ragweed_today='lzxcksdvdvvktzbpeedw',
            ragweed_tomorrow='laqnwhwtwvxgspmvydmh',
            ragweed_dayafter_to='wypzzzchnjsorhhobrzk',
            pollen_type='wmnbdjjdqyuofawjxpad'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'guugmhgpyyqmvlpftdnb'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'ottqsdezejaxgflgaskz'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_last_update_property(self):
        """
        Test last_update property
        """
        test_value = 'jbgsvzipauksoznmktod'
        self.instance.last_update = test_value
        self.assertEqual(self.instance.last_update, test_value)
    
    def test_next_update_property(self):
        """
        Test next_update property
        """
        test_value = 'jzannjvbuqtxnlukizyi'
        self.instance.next_update = test_value
        self.assertEqual(self.instance.next_update, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'xnlscukybsaumlaugcfg'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_hazel_today_property(self):
        """
        Test hazel_today property
        """
        test_value = 'bpnizhburtnrwtgdlsvk'
        self.instance.hazel_today = test_value
        self.assertEqual(self.instance.hazel_today, test_value)
    
    def test_hazel_tomorrow_property(self):
        """
        Test hazel_tomorrow property
        """
        test_value = 'kpstmaoyukivqrjobczr'
        self.instance.hazel_tomorrow = test_value
        self.assertEqual(self.instance.hazel_tomorrow, test_value)
    
    def test_hazel_dayafter_to_property(self):
        """
        Test hazel_dayafter_to property
        """
        test_value = 'zidovwfogzeloyhkrqzw'
        self.instance.hazel_dayafter_to = test_value
        self.assertEqual(self.instance.hazel_dayafter_to, test_value)
    
    def test_alder_today_property(self):
        """
        Test alder_today property
        """
        test_value = 'xabnmrcvkxetvgakoflw'
        self.instance.alder_today = test_value
        self.assertEqual(self.instance.alder_today, test_value)
    
    def test_alder_tomorrow_property(self):
        """
        Test alder_tomorrow property
        """
        test_value = 'oxqhlztplkompkanuthx'
        self.instance.alder_tomorrow = test_value
        self.assertEqual(self.instance.alder_tomorrow, test_value)
    
    def test_alder_dayafter_to_property(self):
        """
        Test alder_dayafter_to property
        """
        test_value = 'wzmhbrvhuzjhbowxkhis'
        self.instance.alder_dayafter_to = test_value
        self.assertEqual(self.instance.alder_dayafter_to, test_value)
    
    def test_birch_today_property(self):
        """
        Test birch_today property
        """
        test_value = 'lnwpsazeismzlecpeinf'
        self.instance.birch_today = test_value
        self.assertEqual(self.instance.birch_today, test_value)
    
    def test_birch_tomorrow_property(self):
        """
        Test birch_tomorrow property
        """
        test_value = 'swaqsihbcezvlrjaktzv'
        self.instance.birch_tomorrow = test_value
        self.assertEqual(self.instance.birch_tomorrow, test_value)
    
    def test_birch_dayafter_to_property(self):
        """
        Test birch_dayafter_to property
        """
        test_value = 'rnehsdsisdoqexsqqacp'
        self.instance.birch_dayafter_to = test_value
        self.assertEqual(self.instance.birch_dayafter_to, test_value)
    
    def test_ash_today_property(self):
        """
        Test ash_today property
        """
        test_value = 'eqipsxnbetejblicupxd'
        self.instance.ash_today = test_value
        self.assertEqual(self.instance.ash_today, test_value)
    
    def test_ash_tomorrow_property(self):
        """
        Test ash_tomorrow property
        """
        test_value = 'enunvohopkpnvsjtvkqv'
        self.instance.ash_tomorrow = test_value
        self.assertEqual(self.instance.ash_tomorrow, test_value)
    
    def test_ash_dayafter_to_property(self):
        """
        Test ash_dayafter_to property
        """
        test_value = 'mkcvoxvsvogpbydknarh'
        self.instance.ash_dayafter_to = test_value
        self.assertEqual(self.instance.ash_dayafter_to, test_value)
    
    def test_grasses_today_property(self):
        """
        Test grasses_today property
        """
        test_value = 'kzyethddxtvwqtchxhqw'
        self.instance.grasses_today = test_value
        self.assertEqual(self.instance.grasses_today, test_value)
    
    def test_grasses_tomorrow_property(self):
        """
        Test grasses_tomorrow property
        """
        test_value = 'ywrfggycnoyvzjpumkcf'
        self.instance.grasses_tomorrow = test_value
        self.assertEqual(self.instance.grasses_tomorrow, test_value)
    
    def test_grasses_dayafter_to_property(self):
        """
        Test grasses_dayafter_to property
        """
        test_value = 'mytzfscdbegmwkojyajd'
        self.instance.grasses_dayafter_to = test_value
        self.assertEqual(self.instance.grasses_dayafter_to, test_value)
    
    def test_rye_today_property(self):
        """
        Test rye_today property
        """
        test_value = 'vucivtbqhowztfvsuqhd'
        self.instance.rye_today = test_value
        self.assertEqual(self.instance.rye_today, test_value)
    
    def test_rye_tomorrow_property(self):
        """
        Test rye_tomorrow property
        """
        test_value = 'uswahrfbvumszvguokjr'
        self.instance.rye_tomorrow = test_value
        self.assertEqual(self.instance.rye_tomorrow, test_value)
    
    def test_rye_dayafter_to_property(self):
        """
        Test rye_dayafter_to property
        """
        test_value = 'xkrhtsrqbixrsrzfmgea'
        self.instance.rye_dayafter_to = test_value
        self.assertEqual(self.instance.rye_dayafter_to, test_value)
    
    def test_mugwort_today_property(self):
        """
        Test mugwort_today property
        """
        test_value = 'ukeakfuyrogezlvxyded'
        self.instance.mugwort_today = test_value
        self.assertEqual(self.instance.mugwort_today, test_value)
    
    def test_mugwort_tomorrow_property(self):
        """
        Test mugwort_tomorrow property
        """
        test_value = 'fzojawirhqkcnizipqet'
        self.instance.mugwort_tomorrow = test_value
        self.assertEqual(self.instance.mugwort_tomorrow, test_value)
    
    def test_mugwort_dayafter_to_property(self):
        """
        Test mugwort_dayafter_to property
        """
        test_value = 'twipbwztgccyvfioljjv'
        self.instance.mugwort_dayafter_to = test_value
        self.assertEqual(self.instance.mugwort_dayafter_to, test_value)
    
    def test_ragweed_today_property(self):
        """
        Test ragweed_today property
        """
        test_value = 'lzxcksdvdvvktzbpeedw'
        self.instance.ragweed_today = test_value
        self.assertEqual(self.instance.ragweed_today, test_value)
    
    def test_ragweed_tomorrow_property(self):
        """
        Test ragweed_tomorrow property
        """
        test_value = 'laqnwhwtwvxgspmvydmh'
        self.instance.ragweed_tomorrow = test_value
        self.assertEqual(self.instance.ragweed_tomorrow, test_value)
    
    def test_ragweed_dayafter_to_property(self):
        """
        Test ragweed_dayafter_to property
        """
        test_value = 'wypzzzchnjsorhhobrzk'
        self.instance.ragweed_dayafter_to = test_value
        self.assertEqual(self.instance.ragweed_dayafter_to, test_value)
    
    def test_pollen_type_property(self):
        """
        Test pollen_type property
        """
        test_value = 'wmnbdjjdqyuofawjxpad'
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

