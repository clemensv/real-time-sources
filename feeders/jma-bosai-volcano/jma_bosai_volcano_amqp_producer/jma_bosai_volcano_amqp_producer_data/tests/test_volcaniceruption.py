"""
Test case for VolcanicEruption
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_amqp_producer_data.volcaniceruption import VolcanicEruption
from jma_bosai_volcano_amqp_producer_data.eruptiontypeenum import EruptionTypeenum
from jma_bosai_volcano_amqp_producer_data.volcaniceruptioneventenum import VolcanicEruptionEventEnum
import datetime


class Test_VolcanicEruption(unittest.TestCase):
    """
    Test case for VolcanicEruption
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VolcanicEruption.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VolcanicEruption for testing
        """
        instance = VolcanicEruption(
            volcano_code='gwostyteecjcanqkicpm',
            event_id='nthwzkvgjzjwlefliwat',
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            eruption_datetime=datetime.datetime.now(datetime.timezone.utc),
            eruption_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            eruption_type=EruptionTypeenum.ERUPTION,
            crater_name='efjqugzcqfkyxhjvlsff',
            colored_plume_height_m=float(81.35288274473344),
            white_plume_height_m=float(55.52621753715996),
            maximum_plume_height_since_start_m=float(89.79918639370979),
            plume_direction='iflxdjqddkewebzulokj',
            ash_dispersal_direction='kbdypsyzwbnzqgofzxfc',
            pyroclastic_flow_observed=False,
            plume_amount_jp='gwcvjqgwwadgzshzjgdi',
            description='thbksyxdygcpvdsvsszp',
            info_type_jp='nocqkjhkehxfwglvfwjw',
            area_codes=['myoqaedsgmvzsgpbsyfy', 'akhdyciyoftqhlabkfsg', 'whevnhtfxwhkxwmbrrrz'],
            prefecture='bmfzwsawmyleiqohlgxw',
            event=VolcanicEruptionEventEnum.eruption
        )
        return instance

    
    def test_volcano_code_property(self):
        """
        Test volcano_code property
        """
        test_value = 'gwostyteecjcanqkicpm'
        self.instance.volcano_code = test_value
        self.assertEqual(self.instance.volcano_code, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'nthwzkvgjzjwlefliwat'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_report_datetime_property(self):
        """
        Test report_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime = test_value
        self.assertEqual(self.instance.report_datetime, test_value)
    
    def test_report_datetime_local_property(self):
        """
        Test report_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.report_datetime_local = test_value
        self.assertEqual(self.instance.report_datetime_local, test_value)
    
    def test_eruption_datetime_property(self):
        """
        Test eruption_datetime property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.eruption_datetime = test_value
        self.assertEqual(self.instance.eruption_datetime, test_value)
    
    def test_eruption_datetime_local_property(self):
        """
        Test eruption_datetime_local property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.eruption_datetime_local = test_value
        self.assertEqual(self.instance.eruption_datetime_local, test_value)
    
    def test_eruption_type_property(self):
        """
        Test eruption_type property
        """
        test_value = EruptionTypeenum.ERUPTION
        self.instance.eruption_type = test_value
        self.assertEqual(self.instance.eruption_type, test_value)
    
    def test_crater_name_property(self):
        """
        Test crater_name property
        """
        test_value = 'efjqugzcqfkyxhjvlsff'
        self.instance.crater_name = test_value
        self.assertEqual(self.instance.crater_name, test_value)
    
    def test_colored_plume_height_m_property(self):
        """
        Test colored_plume_height_m property
        """
        test_value = float(81.35288274473344)
        self.instance.colored_plume_height_m = test_value
        self.assertEqual(self.instance.colored_plume_height_m, test_value)
    
    def test_white_plume_height_m_property(self):
        """
        Test white_plume_height_m property
        """
        test_value = float(55.52621753715996)
        self.instance.white_plume_height_m = test_value
        self.assertEqual(self.instance.white_plume_height_m, test_value)
    
    def test_maximum_plume_height_since_start_m_property(self):
        """
        Test maximum_plume_height_since_start_m property
        """
        test_value = float(89.79918639370979)
        self.instance.maximum_plume_height_since_start_m = test_value
        self.assertEqual(self.instance.maximum_plume_height_since_start_m, test_value)
    
    def test_plume_direction_property(self):
        """
        Test plume_direction property
        """
        test_value = 'iflxdjqddkewebzulokj'
        self.instance.plume_direction = test_value
        self.assertEqual(self.instance.plume_direction, test_value)
    
    def test_ash_dispersal_direction_property(self):
        """
        Test ash_dispersal_direction property
        """
        test_value = 'kbdypsyzwbnzqgofzxfc'
        self.instance.ash_dispersal_direction = test_value
        self.assertEqual(self.instance.ash_dispersal_direction, test_value)
    
    def test_pyroclastic_flow_observed_property(self):
        """
        Test pyroclastic_flow_observed property
        """
        test_value = False
        self.instance.pyroclastic_flow_observed = test_value
        self.assertEqual(self.instance.pyroclastic_flow_observed, test_value)
    
    def test_plume_amount_jp_property(self):
        """
        Test plume_amount_jp property
        """
        test_value = 'gwcvjqgwwadgzshzjgdi'
        self.instance.plume_amount_jp = test_value
        self.assertEqual(self.instance.plume_amount_jp, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'thbksyxdygcpvdsvsszp'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_info_type_jp_property(self):
        """
        Test info_type_jp property
        """
        test_value = 'nocqkjhkehxfwglvfwjw'
        self.instance.info_type_jp = test_value
        self.assertEqual(self.instance.info_type_jp, test_value)
    
    def test_area_codes_property(self):
        """
        Test area_codes property
        """
        test_value = ['myoqaedsgmvzsgpbsyfy', 'akhdyciyoftqhlabkfsg', 'whevnhtfxwhkxwmbrrrz']
        self.instance.area_codes = test_value
        self.assertEqual(self.instance.area_codes, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'bmfzwsawmyleiqohlgxw'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = VolcanicEruptionEventEnum.eruption
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VolcanicEruption.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VolcanicEruption.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

