"""
Test case for PollenForecast
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from dwd_pollenflug_amqp_producer_data.pollenforecast import PollenForecast


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
            region_id=int(81),
            region_name='nyngfuqscdfmpmdfoauz',
            last_update='dgzzsddbjqwdhkzohpyh',
            next_update='dbsvwjkjfvendhsfeiil',
            sender='quvbgxrkkjyxyymmkuur',
            hazel_today='dbwjgobbusrruhzzklnm',
            hazel_tomorrow='xtycssujvubhtmglequw',
            hazel_dayafter_to='cxwidyyenegtluuefvpp',
            alder_today='mcyzfnmcdyzcrxcsweiu',
            alder_tomorrow='bomcayztiodrxpowxgzf',
            alder_dayafter_to='lxsbhawudwfudvcpkkfk',
            birch_today='aalootjkspxnsbehwhld',
            birch_tomorrow='obaytspkyzhdhslcchzm',
            birch_dayafter_to='samljphvsapotmvfytxh',
            ash_today='tpqegpuqvahxpyhcznye',
            ash_tomorrow='lsrjzgkssongibbxkwoh',
            ash_dayafter_to='urmtjajffovlynwojagv',
            grasses_today='syptvxcibrpsludktqhr',
            grasses_tomorrow='kjahbhzwhrrnpbpmlbft',
            grasses_dayafter_to='jcqbwsczdcjxtqcwhznc',
            rye_today='xyyoacqifutppdrzxaqd',
            rye_tomorrow='gxfmfhzbvvdswopppcyk',
            rye_dayafter_to='qopmikadcqzsawhfgnfh',
            mugwort_today='rhhakzxgndhhoemdrucx',
            mugwort_tomorrow='nloqisotgszavdbgrawf',
            mugwort_dayafter_to='vbeotcwqjidaeblkbdtr',
            ragweed_today='cqehyggzyosutmnokgwf',
            ragweed_tomorrow='mslxrrifeabvzokqtzmb',
            ragweed_dayafter_to='bplqyrlsqbicdahoctzb',
            pollen_type='gfwrsazjwohpizrovfwq'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(81)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'nyngfuqscdfmpmdfoauz'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_last_update_property(self):
        """
        Test last_update property
        """
        test_value = 'dgzzsddbjqwdhkzohpyh'
        self.instance.last_update = test_value
        self.assertEqual(self.instance.last_update, test_value)
    
    def test_next_update_property(self):
        """
        Test next_update property
        """
        test_value = 'dbsvwjkjfvendhsfeiil'
        self.instance.next_update = test_value
        self.assertEqual(self.instance.next_update, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'quvbgxrkkjyxyymmkuur'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_hazel_today_property(self):
        """
        Test hazel_today property
        """
        test_value = 'dbwjgobbusrruhzzklnm'
        self.instance.hazel_today = test_value
        self.assertEqual(self.instance.hazel_today, test_value)
    
    def test_hazel_tomorrow_property(self):
        """
        Test hazel_tomorrow property
        """
        test_value = 'xtycssujvubhtmglequw'
        self.instance.hazel_tomorrow = test_value
        self.assertEqual(self.instance.hazel_tomorrow, test_value)
    
    def test_hazel_dayafter_to_property(self):
        """
        Test hazel_dayafter_to property
        """
        test_value = 'cxwidyyenegtluuefvpp'
        self.instance.hazel_dayafter_to = test_value
        self.assertEqual(self.instance.hazel_dayafter_to, test_value)
    
    def test_alder_today_property(self):
        """
        Test alder_today property
        """
        test_value = 'mcyzfnmcdyzcrxcsweiu'
        self.instance.alder_today = test_value
        self.assertEqual(self.instance.alder_today, test_value)
    
    def test_alder_tomorrow_property(self):
        """
        Test alder_tomorrow property
        """
        test_value = 'bomcayztiodrxpowxgzf'
        self.instance.alder_tomorrow = test_value
        self.assertEqual(self.instance.alder_tomorrow, test_value)
    
    def test_alder_dayafter_to_property(self):
        """
        Test alder_dayafter_to property
        """
        test_value = 'lxsbhawudwfudvcpkkfk'
        self.instance.alder_dayafter_to = test_value
        self.assertEqual(self.instance.alder_dayafter_to, test_value)
    
    def test_birch_today_property(self):
        """
        Test birch_today property
        """
        test_value = 'aalootjkspxnsbehwhld'
        self.instance.birch_today = test_value
        self.assertEqual(self.instance.birch_today, test_value)
    
    def test_birch_tomorrow_property(self):
        """
        Test birch_tomorrow property
        """
        test_value = 'obaytspkyzhdhslcchzm'
        self.instance.birch_tomorrow = test_value
        self.assertEqual(self.instance.birch_tomorrow, test_value)
    
    def test_birch_dayafter_to_property(self):
        """
        Test birch_dayafter_to property
        """
        test_value = 'samljphvsapotmvfytxh'
        self.instance.birch_dayafter_to = test_value
        self.assertEqual(self.instance.birch_dayafter_to, test_value)
    
    def test_ash_today_property(self):
        """
        Test ash_today property
        """
        test_value = 'tpqegpuqvahxpyhcznye'
        self.instance.ash_today = test_value
        self.assertEqual(self.instance.ash_today, test_value)
    
    def test_ash_tomorrow_property(self):
        """
        Test ash_tomorrow property
        """
        test_value = 'lsrjzgkssongibbxkwoh'
        self.instance.ash_tomorrow = test_value
        self.assertEqual(self.instance.ash_tomorrow, test_value)
    
    def test_ash_dayafter_to_property(self):
        """
        Test ash_dayafter_to property
        """
        test_value = 'urmtjajffovlynwojagv'
        self.instance.ash_dayafter_to = test_value
        self.assertEqual(self.instance.ash_dayafter_to, test_value)
    
    def test_grasses_today_property(self):
        """
        Test grasses_today property
        """
        test_value = 'syptvxcibrpsludktqhr'
        self.instance.grasses_today = test_value
        self.assertEqual(self.instance.grasses_today, test_value)
    
    def test_grasses_tomorrow_property(self):
        """
        Test grasses_tomorrow property
        """
        test_value = 'kjahbhzwhrrnpbpmlbft'
        self.instance.grasses_tomorrow = test_value
        self.assertEqual(self.instance.grasses_tomorrow, test_value)
    
    def test_grasses_dayafter_to_property(self):
        """
        Test grasses_dayafter_to property
        """
        test_value = 'jcqbwsczdcjxtqcwhznc'
        self.instance.grasses_dayafter_to = test_value
        self.assertEqual(self.instance.grasses_dayafter_to, test_value)
    
    def test_rye_today_property(self):
        """
        Test rye_today property
        """
        test_value = 'xyyoacqifutppdrzxaqd'
        self.instance.rye_today = test_value
        self.assertEqual(self.instance.rye_today, test_value)
    
    def test_rye_tomorrow_property(self):
        """
        Test rye_tomorrow property
        """
        test_value = 'gxfmfhzbvvdswopppcyk'
        self.instance.rye_tomorrow = test_value
        self.assertEqual(self.instance.rye_tomorrow, test_value)
    
    def test_rye_dayafter_to_property(self):
        """
        Test rye_dayafter_to property
        """
        test_value = 'qopmikadcqzsawhfgnfh'
        self.instance.rye_dayafter_to = test_value
        self.assertEqual(self.instance.rye_dayafter_to, test_value)
    
    def test_mugwort_today_property(self):
        """
        Test mugwort_today property
        """
        test_value = 'rhhakzxgndhhoemdrucx'
        self.instance.mugwort_today = test_value
        self.assertEqual(self.instance.mugwort_today, test_value)
    
    def test_mugwort_tomorrow_property(self):
        """
        Test mugwort_tomorrow property
        """
        test_value = 'nloqisotgszavdbgrawf'
        self.instance.mugwort_tomorrow = test_value
        self.assertEqual(self.instance.mugwort_tomorrow, test_value)
    
    def test_mugwort_dayafter_to_property(self):
        """
        Test mugwort_dayafter_to property
        """
        test_value = 'vbeotcwqjidaeblkbdtr'
        self.instance.mugwort_dayafter_to = test_value
        self.assertEqual(self.instance.mugwort_dayafter_to, test_value)
    
    def test_ragweed_today_property(self):
        """
        Test ragweed_today property
        """
        test_value = 'cqehyggzyosutmnokgwf'
        self.instance.ragweed_today = test_value
        self.assertEqual(self.instance.ragweed_today, test_value)
    
    def test_ragweed_tomorrow_property(self):
        """
        Test ragweed_tomorrow property
        """
        test_value = 'mslxrrifeabvzokqtzmb'
        self.instance.ragweed_tomorrow = test_value
        self.assertEqual(self.instance.ragweed_tomorrow, test_value)
    
    def test_ragweed_dayafter_to_property(self):
        """
        Test ragweed_dayafter_to property
        """
        test_value = 'bplqyrlsqbicdahoctzb'
        self.instance.ragweed_dayafter_to = test_value
        self.assertEqual(self.instance.ragweed_dayafter_to, test_value)
    
    def test_pollen_type_property(self):
        """
        Test pollen_type property
        """
        test_value = 'gfwrsazjwohpizrovfwq'
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

