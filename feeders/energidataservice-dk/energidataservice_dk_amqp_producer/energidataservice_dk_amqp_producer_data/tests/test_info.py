"""
Test case for Info
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from energidataservice_dk_amqp_producer_data.dk.energinet.energidataservice.info import Info


class Test_Info(unittest.TestCase):
    """
    Test case for Info
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Info.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Info for testing
        """
        instance = Info(
            info_id='dnddswjbyjrbotviitlf',
            name='ewsberudzkegbxxvlant',
            country='rxqjnpqdhekrgilllmfu',
            city='haovgfkpaqpwprsgevae',
            category='mwmsprtpzhsjecumwotd',
            price_area='bvcnyxrxnuanvemmxocz',
            settlement_date='iypkevchztxvadpqtiwt',
            settlement_period=int(98),
            area_code='filqhlqmdcctaptputha',
            segment='jehzmojhxhdceamjyhbw',
            entity_id='deoecuuxlujtjfqpfbzg',
            event_id='nuetzfbtvcjwfunwnpbj',
            venue_id='rmzvmmwcdcgnynbfceaq'
        )
        return instance

    
    def test_info_id_property(self):
        """
        Test info_id property
        """
        test_value = 'dnddswjbyjrbotviitlf'
        self.instance.info_id = test_value
        self.assertEqual(self.instance.info_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'ewsberudzkegbxxvlant'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_country_property(self):
        """
        Test country property
        """
        test_value = 'rxqjnpqdhekrgilllmfu'
        self.instance.country = test_value
        self.assertEqual(self.instance.country, test_value)
    
    def test_city_property(self):
        """
        Test city property
        """
        test_value = 'haovgfkpaqpwprsgevae'
        self.instance.city = test_value
        self.assertEqual(self.instance.city, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = 'mwmsprtpzhsjecumwotd'
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_price_area_property(self):
        """
        Test price_area property
        """
        test_value = 'bvcnyxrxnuanvemmxocz'
        self.instance.price_area = test_value
        self.assertEqual(self.instance.price_area, test_value)
    
    def test_settlement_date_property(self):
        """
        Test settlement_date property
        """
        test_value = 'iypkevchztxvadpqtiwt'
        self.instance.settlement_date = test_value
        self.assertEqual(self.instance.settlement_date, test_value)
    
    def test_settlement_period_property(self):
        """
        Test settlement_period property
        """
        test_value = int(98)
        self.instance.settlement_period = test_value
        self.assertEqual(self.instance.settlement_period, test_value)
    
    def test_area_code_property(self):
        """
        Test area_code property
        """
        test_value = 'filqhlqmdcctaptputha'
        self.instance.area_code = test_value
        self.assertEqual(self.instance.area_code, test_value)
    
    def test_segment_property(self):
        """
        Test segment property
        """
        test_value = 'jehzmojhxhdceamjyhbw'
        self.instance.segment = test_value
        self.assertEqual(self.instance.segment, test_value)
    
    def test_entity_id_property(self):
        """
        Test entity_id property
        """
        test_value = 'deoecuuxlujtjfqpfbzg'
        self.instance.entity_id = test_value
        self.assertEqual(self.instance.entity_id, test_value)
    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = 'nuetzfbtvcjwfunwnpbj'
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_venue_id_property(self):
        """
        Test venue_id property
        """
        test_value = 'rmzvmmwcdcgnynbfceaq'
        self.instance.venue_id = test_value
        self.assertEqual(self.instance.venue_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Info.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Info.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

