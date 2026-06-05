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
            region_id='ynqleusshfslgegxffya',
            region_name='rmatyrxjhgqvyfrvbodz',
            last_update='dastidarmjieqqewmoqm',
            next_update='wugqvoblfheqqixlhvxr',
            sender='dsbpbnpyamizlwncgmbw',
            hazel_today='yyvergkhfqazrjoiuhih',
            hazel_tomorrow='zvsxsatsoiopfywpfxqe',
            hazel_dayafter_to='bhwszyshvdteowevjqxf',
            alder_today='xpxlcjooxucphgljsitx',
            alder_tomorrow='nlcscmffwtgonjgrsrqm',
            alder_dayafter_to='xsjolkbeppuwznxwudln',
            birch_today='xkfymmvsmwgefinodeoz',
            birch_tomorrow='ymllizkunawfumdiiqkq',
            birch_dayafter_to='naekakefawmxhpxjuyot',
            ash_today='tucyavfwwlvuuqfhuwuw',
            ash_tomorrow='jglbozkjojisxcmvmeca',
            ash_dayafter_to='cbconjmrvncmzhewkwtw',
            grasses_today='igmcnuydqbtblohbgcod',
            grasses_tomorrow='wchpzbjcbqycnzgxpulr',
            grasses_dayafter_to='rpdhfkfdyueyfblcjuqz',
            rye_today='ucctepgiuoohljixxhgt',
            rye_tomorrow='dkpwpqvjdvgqmyiendos',
            rye_dayafter_to='ovcqdwfttcinxapvcxyh',
            mugwort_today='oynilzweeptybrfzzkeb',
            mugwort_tomorrow='dswucixxjyszydwlloqx',
            mugwort_dayafter_to='pgntgvjiplgpsshshfqg',
            ragweed_today='hwecjaqnntahbeqxrrqq',
            ragweed_tomorrow='orsbutxibauhtvbwhsgh',
            ragweed_dayafter_to='gzmenoduxfxdwijdqedp',
            pollen_type='qrjpbmoxbhuakwvmbfsg'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = 'ynqleusshfslgegxffya'
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'rmatyrxjhgqvyfrvbodz'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_last_update_property(self):
        """
        Test last_update property
        """
        test_value = 'dastidarmjieqqewmoqm'
        self.instance.last_update = test_value
        self.assertEqual(self.instance.last_update, test_value)
    
    def test_next_update_property(self):
        """
        Test next_update property
        """
        test_value = 'wugqvoblfheqqixlhvxr'
        self.instance.next_update = test_value
        self.assertEqual(self.instance.next_update, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'dsbpbnpyamizlwncgmbw'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_hazel_today_property(self):
        """
        Test hazel_today property
        """
        test_value = 'yyvergkhfqazrjoiuhih'
        self.instance.hazel_today = test_value
        self.assertEqual(self.instance.hazel_today, test_value)
    
    def test_hazel_tomorrow_property(self):
        """
        Test hazel_tomorrow property
        """
        test_value = 'zvsxsatsoiopfywpfxqe'
        self.instance.hazel_tomorrow = test_value
        self.assertEqual(self.instance.hazel_tomorrow, test_value)
    
    def test_hazel_dayafter_to_property(self):
        """
        Test hazel_dayafter_to property
        """
        test_value = 'bhwszyshvdteowevjqxf'
        self.instance.hazel_dayafter_to = test_value
        self.assertEqual(self.instance.hazel_dayafter_to, test_value)
    
    def test_alder_today_property(self):
        """
        Test alder_today property
        """
        test_value = 'xpxlcjooxucphgljsitx'
        self.instance.alder_today = test_value
        self.assertEqual(self.instance.alder_today, test_value)
    
    def test_alder_tomorrow_property(self):
        """
        Test alder_tomorrow property
        """
        test_value = 'nlcscmffwtgonjgrsrqm'
        self.instance.alder_tomorrow = test_value
        self.assertEqual(self.instance.alder_tomorrow, test_value)
    
    def test_alder_dayafter_to_property(self):
        """
        Test alder_dayafter_to property
        """
        test_value = 'xsjolkbeppuwznxwudln'
        self.instance.alder_dayafter_to = test_value
        self.assertEqual(self.instance.alder_dayafter_to, test_value)
    
    def test_birch_today_property(self):
        """
        Test birch_today property
        """
        test_value = 'xkfymmvsmwgefinodeoz'
        self.instance.birch_today = test_value
        self.assertEqual(self.instance.birch_today, test_value)
    
    def test_birch_tomorrow_property(self):
        """
        Test birch_tomorrow property
        """
        test_value = 'ymllizkunawfumdiiqkq'
        self.instance.birch_tomorrow = test_value
        self.assertEqual(self.instance.birch_tomorrow, test_value)
    
    def test_birch_dayafter_to_property(self):
        """
        Test birch_dayafter_to property
        """
        test_value = 'naekakefawmxhpxjuyot'
        self.instance.birch_dayafter_to = test_value
        self.assertEqual(self.instance.birch_dayafter_to, test_value)
    
    def test_ash_today_property(self):
        """
        Test ash_today property
        """
        test_value = 'tucyavfwwlvuuqfhuwuw'
        self.instance.ash_today = test_value
        self.assertEqual(self.instance.ash_today, test_value)
    
    def test_ash_tomorrow_property(self):
        """
        Test ash_tomorrow property
        """
        test_value = 'jglbozkjojisxcmvmeca'
        self.instance.ash_tomorrow = test_value
        self.assertEqual(self.instance.ash_tomorrow, test_value)
    
    def test_ash_dayafter_to_property(self):
        """
        Test ash_dayafter_to property
        """
        test_value = 'cbconjmrvncmzhewkwtw'
        self.instance.ash_dayafter_to = test_value
        self.assertEqual(self.instance.ash_dayafter_to, test_value)
    
    def test_grasses_today_property(self):
        """
        Test grasses_today property
        """
        test_value = 'igmcnuydqbtblohbgcod'
        self.instance.grasses_today = test_value
        self.assertEqual(self.instance.grasses_today, test_value)
    
    def test_grasses_tomorrow_property(self):
        """
        Test grasses_tomorrow property
        """
        test_value = 'wchpzbjcbqycnzgxpulr'
        self.instance.grasses_tomorrow = test_value
        self.assertEqual(self.instance.grasses_tomorrow, test_value)
    
    def test_grasses_dayafter_to_property(self):
        """
        Test grasses_dayafter_to property
        """
        test_value = 'rpdhfkfdyueyfblcjuqz'
        self.instance.grasses_dayafter_to = test_value
        self.assertEqual(self.instance.grasses_dayafter_to, test_value)
    
    def test_rye_today_property(self):
        """
        Test rye_today property
        """
        test_value = 'ucctepgiuoohljixxhgt'
        self.instance.rye_today = test_value
        self.assertEqual(self.instance.rye_today, test_value)
    
    def test_rye_tomorrow_property(self):
        """
        Test rye_tomorrow property
        """
        test_value = 'dkpwpqvjdvgqmyiendos'
        self.instance.rye_tomorrow = test_value
        self.assertEqual(self.instance.rye_tomorrow, test_value)
    
    def test_rye_dayafter_to_property(self):
        """
        Test rye_dayafter_to property
        """
        test_value = 'ovcqdwfttcinxapvcxyh'
        self.instance.rye_dayafter_to = test_value
        self.assertEqual(self.instance.rye_dayafter_to, test_value)
    
    def test_mugwort_today_property(self):
        """
        Test mugwort_today property
        """
        test_value = 'oynilzweeptybrfzzkeb'
        self.instance.mugwort_today = test_value
        self.assertEqual(self.instance.mugwort_today, test_value)
    
    def test_mugwort_tomorrow_property(self):
        """
        Test mugwort_tomorrow property
        """
        test_value = 'dswucixxjyszydwlloqx'
        self.instance.mugwort_tomorrow = test_value
        self.assertEqual(self.instance.mugwort_tomorrow, test_value)
    
    def test_mugwort_dayafter_to_property(self):
        """
        Test mugwort_dayafter_to property
        """
        test_value = 'pgntgvjiplgpsshshfqg'
        self.instance.mugwort_dayafter_to = test_value
        self.assertEqual(self.instance.mugwort_dayafter_to, test_value)
    
    def test_ragweed_today_property(self):
        """
        Test ragweed_today property
        """
        test_value = 'hwecjaqnntahbeqxrrqq'
        self.instance.ragweed_today = test_value
        self.assertEqual(self.instance.ragweed_today, test_value)
    
    def test_ragweed_tomorrow_property(self):
        """
        Test ragweed_tomorrow property
        """
        test_value = 'orsbutxibauhtvbwhsgh'
        self.instance.ragweed_tomorrow = test_value
        self.assertEqual(self.instance.ragweed_tomorrow, test_value)
    
    def test_ragweed_dayafter_to_property(self):
        """
        Test ragweed_dayafter_to property
        """
        test_value = 'gzmenoduxfxdwijdqedp'
        self.instance.ragweed_dayafter_to = test_value
        self.assertEqual(self.instance.ragweed_dayafter_to, test_value)
    
    def test_pollen_type_property(self):
        """
        Test pollen_type property
        """
        test_value = 'qrjpbmoxbhuakwvmbfsg'
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

