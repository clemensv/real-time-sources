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
            region_id=int(44),
            region_name='leilugoopnzptipkyduw',
            last_update='xoavtcfrzkrwbojhcqbx',
            next_update='gsmamtihuunaxwbbwski',
            sender='gxrfyatkpyundppmhvzm',
            hazel_today='nabhlpsccbpoykxozata',
            hazel_tomorrow='tvazzpiwdbbhppmtqmni',
            hazel_dayafter_to='ilrgljxlvikxsvxmbdqr',
            alder_today='pbqlurudklpnzocndphu',
            alder_tomorrow='dtdmisrfncbyqrcchttm',
            alder_dayafter_to='vayxnrswxlzazzhpyebn',
            birch_today='yrdlvrtoxwjcqntnhzrt',
            birch_tomorrow='exzctmcsrjxatjpvezgi',
            birch_dayafter_to='fpipsralplrzrmndptnv',
            ash_today='kaghstrhbpfwgrexwdzr',
            ash_tomorrow='fueellutcqkpkhozmzsz',
            ash_dayafter_to='zjcffhybjdtzjujllwrb',
            grasses_today='xlbzdmcrzheyaxngbrnt',
            grasses_tomorrow='prbrywmozqdgddcltnvt',
            grasses_dayafter_to='cgxjpvcqquigbnewzjjt',
            rye_today='tyksfvltckjdebfdwxbj',
            rye_tomorrow='tlhwwcnablnaadongfmc',
            rye_dayafter_to='ydevcpxefilnujtdbmbm',
            mugwort_today='glqjhsyvbpsuzchdmtcj',
            mugwort_tomorrow='opuqrghcvyirltbyzjeh',
            mugwort_dayafter_to='tiaudftqkdkffhmswnex',
            ragweed_today='eciaarcmuhniqagpdtfq',
            ragweed_tomorrow='vnnwvlumesnsmecvbuqe',
            ragweed_dayafter_to='ixvkilrkpugxzyognteq',
            pollen_type='yvrqzoagmphazechbgsw'
        )
        return instance

    
    def test_region_id_property(self):
        """
        Test region_id property
        """
        test_value = int(44)
        self.instance.region_id = test_value
        self.assertEqual(self.instance.region_id, test_value)
    
    def test_region_name_property(self):
        """
        Test region_name property
        """
        test_value = 'leilugoopnzptipkyduw'
        self.instance.region_name = test_value
        self.assertEqual(self.instance.region_name, test_value)
    
    def test_last_update_property(self):
        """
        Test last_update property
        """
        test_value = 'xoavtcfrzkrwbojhcqbx'
        self.instance.last_update = test_value
        self.assertEqual(self.instance.last_update, test_value)
    
    def test_next_update_property(self):
        """
        Test next_update property
        """
        test_value = 'gsmamtihuunaxwbbwski'
        self.instance.next_update = test_value
        self.assertEqual(self.instance.next_update, test_value)
    
    def test_sender_property(self):
        """
        Test sender property
        """
        test_value = 'gxrfyatkpyundppmhvzm'
        self.instance.sender = test_value
        self.assertEqual(self.instance.sender, test_value)
    
    def test_hazel_today_property(self):
        """
        Test hazel_today property
        """
        test_value = 'nabhlpsccbpoykxozata'
        self.instance.hazel_today = test_value
        self.assertEqual(self.instance.hazel_today, test_value)
    
    def test_hazel_tomorrow_property(self):
        """
        Test hazel_tomorrow property
        """
        test_value = 'tvazzpiwdbbhppmtqmni'
        self.instance.hazel_tomorrow = test_value
        self.assertEqual(self.instance.hazel_tomorrow, test_value)
    
    def test_hazel_dayafter_to_property(self):
        """
        Test hazel_dayafter_to property
        """
        test_value = 'ilrgljxlvikxsvxmbdqr'
        self.instance.hazel_dayafter_to = test_value
        self.assertEqual(self.instance.hazel_dayafter_to, test_value)
    
    def test_alder_today_property(self):
        """
        Test alder_today property
        """
        test_value = 'pbqlurudklpnzocndphu'
        self.instance.alder_today = test_value
        self.assertEqual(self.instance.alder_today, test_value)
    
    def test_alder_tomorrow_property(self):
        """
        Test alder_tomorrow property
        """
        test_value = 'dtdmisrfncbyqrcchttm'
        self.instance.alder_tomorrow = test_value
        self.assertEqual(self.instance.alder_tomorrow, test_value)
    
    def test_alder_dayafter_to_property(self):
        """
        Test alder_dayafter_to property
        """
        test_value = 'vayxnrswxlzazzhpyebn'
        self.instance.alder_dayafter_to = test_value
        self.assertEqual(self.instance.alder_dayafter_to, test_value)
    
    def test_birch_today_property(self):
        """
        Test birch_today property
        """
        test_value = 'yrdlvrtoxwjcqntnhzrt'
        self.instance.birch_today = test_value
        self.assertEqual(self.instance.birch_today, test_value)
    
    def test_birch_tomorrow_property(self):
        """
        Test birch_tomorrow property
        """
        test_value = 'exzctmcsrjxatjpvezgi'
        self.instance.birch_tomorrow = test_value
        self.assertEqual(self.instance.birch_tomorrow, test_value)
    
    def test_birch_dayafter_to_property(self):
        """
        Test birch_dayafter_to property
        """
        test_value = 'fpipsralplrzrmndptnv'
        self.instance.birch_dayafter_to = test_value
        self.assertEqual(self.instance.birch_dayafter_to, test_value)
    
    def test_ash_today_property(self):
        """
        Test ash_today property
        """
        test_value = 'kaghstrhbpfwgrexwdzr'
        self.instance.ash_today = test_value
        self.assertEqual(self.instance.ash_today, test_value)
    
    def test_ash_tomorrow_property(self):
        """
        Test ash_tomorrow property
        """
        test_value = 'fueellutcqkpkhozmzsz'
        self.instance.ash_tomorrow = test_value
        self.assertEqual(self.instance.ash_tomorrow, test_value)
    
    def test_ash_dayafter_to_property(self):
        """
        Test ash_dayafter_to property
        """
        test_value = 'zjcffhybjdtzjujllwrb'
        self.instance.ash_dayafter_to = test_value
        self.assertEqual(self.instance.ash_dayafter_to, test_value)
    
    def test_grasses_today_property(self):
        """
        Test grasses_today property
        """
        test_value = 'xlbzdmcrzheyaxngbrnt'
        self.instance.grasses_today = test_value
        self.assertEqual(self.instance.grasses_today, test_value)
    
    def test_grasses_tomorrow_property(self):
        """
        Test grasses_tomorrow property
        """
        test_value = 'prbrywmozqdgddcltnvt'
        self.instance.grasses_tomorrow = test_value
        self.assertEqual(self.instance.grasses_tomorrow, test_value)
    
    def test_grasses_dayafter_to_property(self):
        """
        Test grasses_dayafter_to property
        """
        test_value = 'cgxjpvcqquigbnewzjjt'
        self.instance.grasses_dayafter_to = test_value
        self.assertEqual(self.instance.grasses_dayafter_to, test_value)
    
    def test_rye_today_property(self):
        """
        Test rye_today property
        """
        test_value = 'tyksfvltckjdebfdwxbj'
        self.instance.rye_today = test_value
        self.assertEqual(self.instance.rye_today, test_value)
    
    def test_rye_tomorrow_property(self):
        """
        Test rye_tomorrow property
        """
        test_value = 'tlhwwcnablnaadongfmc'
        self.instance.rye_tomorrow = test_value
        self.assertEqual(self.instance.rye_tomorrow, test_value)
    
    def test_rye_dayafter_to_property(self):
        """
        Test rye_dayafter_to property
        """
        test_value = 'ydevcpxefilnujtdbmbm'
        self.instance.rye_dayafter_to = test_value
        self.assertEqual(self.instance.rye_dayafter_to, test_value)
    
    def test_mugwort_today_property(self):
        """
        Test mugwort_today property
        """
        test_value = 'glqjhsyvbpsuzchdmtcj'
        self.instance.mugwort_today = test_value
        self.assertEqual(self.instance.mugwort_today, test_value)
    
    def test_mugwort_tomorrow_property(self):
        """
        Test mugwort_tomorrow property
        """
        test_value = 'opuqrghcvyirltbyzjeh'
        self.instance.mugwort_tomorrow = test_value
        self.assertEqual(self.instance.mugwort_tomorrow, test_value)
    
    def test_mugwort_dayafter_to_property(self):
        """
        Test mugwort_dayafter_to property
        """
        test_value = 'tiaudftqkdkffhmswnex'
        self.instance.mugwort_dayafter_to = test_value
        self.assertEqual(self.instance.mugwort_dayafter_to, test_value)
    
    def test_ragweed_today_property(self):
        """
        Test ragweed_today property
        """
        test_value = 'eciaarcmuhniqagpdtfq'
        self.instance.ragweed_today = test_value
        self.assertEqual(self.instance.ragweed_today, test_value)
    
    def test_ragweed_tomorrow_property(self):
        """
        Test ragweed_tomorrow property
        """
        test_value = 'vnnwvlumesnsmecvbuqe'
        self.instance.ragweed_tomorrow = test_value
        self.assertEqual(self.instance.ragweed_tomorrow, test_value)
    
    def test_ragweed_dayafter_to_property(self):
        """
        Test ragweed_dayafter_to property
        """
        test_value = 'ixvkilrkpugxzyognteq'
        self.instance.ragweed_dayafter_to = test_value
        self.assertEqual(self.instance.ragweed_dayafter_to, test_value)
    
    def test_pollen_type_property(self):
        """
        Test pollen_type property
        """
        test_value = 'yvrqzoagmphazechbgsw'
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

