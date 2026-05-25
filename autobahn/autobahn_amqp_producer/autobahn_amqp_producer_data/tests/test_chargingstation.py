"""
Test case for ChargingStation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_amqp_producer_data.chargingstation import ChargingStation
from autobahn_amqp_producer_data.displaytypeenum import DisplayTypeenum
from typing import Any
import datetime


class Test_ChargingStation(unittest.TestCase):
    """
    Test case for ChargingStation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChargingStation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChargingStation for testing
        """
        instance = ChargingStation(
            identifier='sontvzqymskthscenwkr',
            road='fuvrcpwozzbwmuiijuem',
            road_ids=['tjwactaopyrhnwhnmxzz', 'phlvbudcvqbzvwtvddbv', 'uidylqcklnqajfuymfzh', 'khkjvputjqllhrthaujv', 'tkjspgdeodtgxscplhyc'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.ROADWORKS,
            title='nwiehkjybnpiiydzxwwd',
            subtitle='gqhxbtwkdxzcsjemdhgo',
            description_lines=None,
            future=False,
            is_blocked=False,
            icon='jujhxwbmzabqipotaxuq',
            extent='qmxmbudlzxtjpwsyapgr',
            point='bmsgkuojjqaanmomzasv',
            coordinate_lat=float(41.99298345141946),
            coordinate_lon=float(4.057136892882607),
            address_line='bfcenuqavmzqyxpdhysi',
            charging_point_count=int(11),
            charging_points_json='njsgmkkmguebzwgicnpy',
            route_recommendation_json='fffibdjpjauwijtyuktt',
            footer_lines=None
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'sontvzqymskthscenwkr'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'fuvrcpwozzbwmuiijuem'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['tjwactaopyrhnwhnmxzz', 'phlvbudcvqbzvwtvddbv', 'uidylqcklnqajfuymfzh', 'khkjvputjqllhrthaujv', 'tkjspgdeodtgxscplhyc']
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
        test_value = 'nwiehkjybnpiiydzxwwd'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'gqhxbtwkdxzcsjemdhgo'
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
        test_value = 'jujhxwbmzabqipotaxuq'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'qmxmbudlzxtjpwsyapgr'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'bmsgkuojjqaanmomzasv'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(41.99298345141946)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(4.057136892882607)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_address_line_property(self):
        """
        Test address_line property
        """
        test_value = 'bfcenuqavmzqyxpdhysi'
        self.instance.address_line = test_value
        self.assertEqual(self.instance.address_line, test_value)
    
    def test_charging_point_count_property(self):
        """
        Test charging_point_count property
        """
        test_value = int(11)
        self.instance.charging_point_count = test_value
        self.assertEqual(self.instance.charging_point_count, test_value)
    
    def test_charging_points_json_property(self):
        """
        Test charging_points_json property
        """
        test_value = 'njsgmkkmguebzwgicnpy'
        self.instance.charging_points_json = test_value
        self.assertEqual(self.instance.charging_points_json, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'fffibdjpjauwijtyuktt'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = None
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChargingStation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChargingStation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

