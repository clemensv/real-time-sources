"""
Test case for RoadEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_amqp_producer_data.roadevent import RoadEvent
from typing import Any
from autobahn_amqp_producer_data.displaytypeenum import DisplayTypeenum
import datetime


class Test_RoadEvent(unittest.TestCase):
    """
    Test case for RoadEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_RoadEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of RoadEvent for testing
        """
        instance = RoadEvent(
            identifier='vuyqcxgouwnykfmnpqcq',
            road='xdjtsmiwaypssdifigpe',
            road_ids=['csvojolvaomldnwldqca', 'gckrwnreskuxsgsmukwq', 'hpyzvqnvlkhqdhxufaiz'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.ROADWORKS,
            title='gkmwizdyohzhcrjmlbiu',
            subtitle='vcvumnaecksplekqavrf',
            description_lines=None,
            future=False,
            is_blocked=True,
            icon='ikrojgyejwcnikiqmalw',
            start_lc_position=int(11),
            start_timestamp=datetime.datetime.now(datetime.timezone.utc),
            extent='bpnsfxrgxpknzprtgovv',
            point='wakduwgjeocbgwhccrdq',
            coordinate_lat=float(51.227109860749124),
            coordinate_lon=float(86.43348839476911),
            geometry_json='vmainhajlngstigzurzq',
            impact_lower='kptgujibuatjdrxpooxk',
            impact_upper='rghbmeeadvutfovqmucz',
            impact_symbols=None,
            route_recommendation_json='vdcunoxxnifawrornwpx',
            footer_lines=None
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'vuyqcxgouwnykfmnpqcq'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'xdjtsmiwaypssdifigpe'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['csvojolvaomldnwldqca', 'gckrwnreskuxsgsmukwq', 'hpyzvqnvlkhqdhxufaiz']
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
        test_value = 'gkmwizdyohzhcrjmlbiu'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'vcvumnaecksplekqavrf'
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
        test_value = True
        self.instance.is_blocked = test_value
        self.assertEqual(self.instance.is_blocked, test_value)
    
    def test_icon_property(self):
        """
        Test icon property
        """
        test_value = 'ikrojgyejwcnikiqmalw'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(11)
        self.instance.start_lc_position = test_value
        self.assertEqual(self.instance.start_lc_position, test_value)
    
    def test_start_timestamp_property(self):
        """
        Test start_timestamp property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.start_timestamp = test_value
        self.assertEqual(self.instance.start_timestamp, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'bpnsfxrgxpknzprtgovv'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'wakduwgjeocbgwhccrdq'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(51.227109860749124)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(86.43348839476911)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_geometry_json_property(self):
        """
        Test geometry_json property
        """
        test_value = 'vmainhajlngstigzurzq'
        self.instance.geometry_json = test_value
        self.assertEqual(self.instance.geometry_json, test_value)
    
    def test_impact_lower_property(self):
        """
        Test impact_lower property
        """
        test_value = 'kptgujibuatjdrxpooxk'
        self.instance.impact_lower = test_value
        self.assertEqual(self.instance.impact_lower, test_value)
    
    def test_impact_upper_property(self):
        """
        Test impact_upper property
        """
        test_value = 'rghbmeeadvutfovqmucz'
        self.instance.impact_upper = test_value
        self.assertEqual(self.instance.impact_upper, test_value)
    
    def test_impact_symbols_property(self):
        """
        Test impact_symbols property
        """
        test_value = None
        self.instance.impact_symbols = test_value
        self.assertEqual(self.instance.impact_symbols, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'vdcunoxxnifawrornwpx'
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
        new_instance = RoadEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = RoadEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

