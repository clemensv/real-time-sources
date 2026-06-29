"""
Test case for Volcano
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from jma_bosai_volcano_mqtt_producer_data.volcano import Volcano
from jma_bosai_volcano_mqtt_producer_data.volcanoeventenum import VolcanoEventEnum


class Test_Volcano(unittest.TestCase):
    """
    Test case for Volcano
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Volcano.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Volcano for testing
        """
        instance = Volcano(
            volcano_code='keukcwvumvvxhpsljbrl',
            name_jp='nnzpqkdiqqqocbywwnqc',
            name_en='juyhiykjlinjkfcgnjsf',
            latitude=float(83.03923005211018),
            longitude=float(2.2288719927787914),
            elevation_m=float(41.120767961770554),
            level_operation=True,
            prefecture='cwlayolmizrpneraclta',
            event=VolcanoEventEnum.info
        )
        return instance

    
    def test_volcano_code_property(self):
        """
        Test volcano_code property
        """
        test_value = 'keukcwvumvvxhpsljbrl'
        self.instance.volcano_code = test_value
        self.assertEqual(self.instance.volcano_code, test_value)
    
    def test_name_jp_property(self):
        """
        Test name_jp property
        """
        test_value = 'nnzpqkdiqqqocbywwnqc'
        self.instance.name_jp = test_value
        self.assertEqual(self.instance.name_jp, test_value)
    
    def test_name_en_property(self):
        """
        Test name_en property
        """
        test_value = 'juyhiykjlinjkfcgnjsf'
        self.instance.name_en = test_value
        self.assertEqual(self.instance.name_en, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(83.03923005211018)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(2.2288719927787914)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_elevation_m_property(self):
        """
        Test elevation_m property
        """
        test_value = float(41.120767961770554)
        self.instance.elevation_m = test_value
        self.assertEqual(self.instance.elevation_m, test_value)
    
    def test_level_operation_property(self):
        """
        Test level_operation property
        """
        test_value = True
        self.instance.level_operation = test_value
        self.assertEqual(self.instance.level_operation, test_value)
    
    def test_prefecture_property(self):
        """
        Test prefecture property
        """
        test_value = 'cwlayolmizrpneraclta'
        self.instance.prefecture = test_value
        self.assertEqual(self.instance.prefecture, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = VolcanoEventEnum.info
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Volcano.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Volcano.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

