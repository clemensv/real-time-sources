"""
Test case for Webcam
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.webcam import Webcam
from typing import Any
from autobahn_producer_data.displaytypeenum import DisplayTypeenum
import datetime


class Test_Webcam(unittest.TestCase):
    """
    Test case for Webcam
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Webcam.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Webcam for testing
        """
        instance = Webcam(
            identifier='dkwzdxiuzqdyolnmsais',
            road_ids=['yyijgyjjmvimciplhipg', 'qlyxijxpypivbfzuvnmr'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.ROADWORKS,
            title='boieffpmsguvxfnfjqoo',
            subtitle='nitzirgucwyuqehpbobx',
            description_lines=None,
            future=True,
            is_blocked=True,
            icon='ynxypqwgzdapajkplrxk',
            extent='erfeojpaugwekhqilzhj',
            point='feghcmvglawjgesbnmpi',
            coordinate_lat=float(67.15100717234614),
            coordinate_lon=float(23.91409360767376),
            route_recommendation_json='ucyepdujmonlkeqjqftm',
            footer_lines=None,
            operator_name='gqasjpgvoxlornoprjqw',
            image_url='kywkgsdyvysigvbxsevu',
            stream_url='ilorimovpxeqawargevb'
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'dkwzdxiuzqdyolnmsais'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['yyijgyjjmvimciplhipg', 'qlyxijxpypivbfzuvnmr']
        self.instance.road_ids = test_value
        self.assertEqual(self.instance.road_ids, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_display_type_property(self):
        """
        Test display_type property
        """
        test_value = DisplayTypeenum.ROADWORKS
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'boieffpmsguvxfnfjqoo'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'nitzirgucwyuqehpbobx'
        self.instance.subtitle = test_value
        self.assertEqual(self.instance.subtitle, test_value)
    
    def test_description_lines_property(self):
        """
        Test description_lines property
        """
        test_value = None
        self.instance.description_lines = test_value
        self.assertEqual(self.instance.description_lines, test_value)
    
    def test_future_property(self):
        """
        Test future property
        """
        test_value = True
        self.instance.future = test_value
        self.assertEqual(self.instance.future, test_value)
    
    def test_is_blocked_property(self):
        """
        Test is_blocked property
        """
        test_value = True
        self.instance.is_blocked = test_value
        self.assertEqual(self.instance.is_blocked, test_value)
    
    def test_icon_property(self):
        """
        Test icon property
        """
        test_value = 'ynxypqwgzdapajkplrxk'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'erfeojpaugwekhqilzhj'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'feghcmvglawjgesbnmpi'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(67.15100717234614)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(23.91409360767376)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'ucyepdujmonlkeqjqftm'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = None
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_operator_name_property(self):
        """
        Test operator_name property
        """
        test_value = 'gqasjpgvoxlornoprjqw'
        self.instance.operator_name = test_value
        self.assertEqual(self.instance.operator_name, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'kywkgsdyvysigvbxsevu'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_stream_url_property(self):
        """
        Test stream_url property
        """
        test_value = 'ilorimovpxeqawargevb'
        self.instance.stream_url = test_value
        self.assertEqual(self.instance.stream_url, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Webcam.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Webcam.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

