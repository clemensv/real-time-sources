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
            identifier='rxmvcayksycbzpxzapzx',
            road='ggrcvsshooxfwcihjdvg',
            road_ids=['fcgkjtwunggvkloggqcd', 'byykezbjpdkhvdaphcwt', 'thtgzmxsyejdywgyecbi', 'eiajahdtnjxdsvfcftwn'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.PARKING,
            title='nxbcsksacxjjyfplxkhw',
            subtitle='dwqwkmjyjchlytbkyprj',
            description_lines=None,
            future=False,
            is_blocked=False,
            icon='coewhhvyumjlppkpiqjs',
            extent='isdzehjpdmbkqtavuunj',
            point='naxlvvmlhdigpxiupuiu',
            coordinate_lat=float(92.93127539044296),
            coordinate_lon=float(77.83256186862575),
            route_recommendation_json='izgdfzmbqovkizqiodip',
            footer_lines=None,
            operator_name='hmkvbqflgiwummeoryvo',
            image_url='aamhoqqusebdothvsdpr',
            stream_url='sekynkmqcexizjwoayjg'
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'rxmvcayksycbzpxzapzx'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'ggrcvsshooxfwcihjdvg'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['fcgkjtwunggvkloggqcd', 'byykezbjpdkhvdaphcwt', 'thtgzmxsyejdywgyecbi', 'eiajahdtnjxdsvfcftwn']
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
        test_value = DisplayTypeenum.PARKING
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'nxbcsksacxjjyfplxkhw'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'dwqwkmjyjchlytbkyprj'
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
        test_value = False
        self.instance.future = test_value
        self.assertEqual(self.instance.future, test_value)
    
    def test_is_blocked_property(self):
        """
        Test is_blocked property
        """
        test_value = False
        self.instance.is_blocked = test_value
        self.assertEqual(self.instance.is_blocked, test_value)
    
    def test_icon_property(self):
        """
        Test icon property
        """
        test_value = 'coewhhvyumjlppkpiqjs'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'isdzehjpdmbkqtavuunj'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'naxlvvmlhdigpxiupuiu'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(92.93127539044296)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(77.83256186862575)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'izgdfzmbqovkizqiodip'
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
        test_value = 'hmkvbqflgiwummeoryvo'
        self.instance.operator_name = test_value
        self.assertEqual(self.instance.operator_name, test_value)
    
    def test_image_url_property(self):
        """
        Test image_url property
        """
        test_value = 'aamhoqqusebdothvsdpr'
        self.instance.image_url = test_value
        self.assertEqual(self.instance.image_url, test_value)
    
    def test_stream_url_property(self):
        """
        Test stream_url property
        """
        test_value = 'sekynkmqcexizjwoayjg'
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

