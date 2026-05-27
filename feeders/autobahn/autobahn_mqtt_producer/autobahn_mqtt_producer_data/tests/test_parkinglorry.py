"""
Test case for ParkingLorry
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_mqtt_producer_data.parkinglorry import ParkingLorry
from autobahn_mqtt_producer_data.displaytypeenum import DisplayTypeenum
from typing import Any
import datetime


class Test_ParkingLorry(unittest.TestCase):
    """
    Test case for ParkingLorry
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ParkingLorry.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ParkingLorry for testing
        """
        instance = ParkingLorry(
            identifier='mzunamhxvclipnjmdhle',
            road='edtlebhtnayqnwmvhwaa',
            road_ids=['lfjxnbpiewgfduwkzzpf', 'uxoopehqbamjinfjdiho'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.WARNING,
            title='wnjpgqfdaakfvgjnluan',
            subtitle='ueikgyfzcgjuxuxcjnzk',
            description_lines=None,
            future=True,
            is_blocked=True,
            icon='dqgbeevllaxgckgnfdft',
            start_lc_position=int(41),
            extent='bknyzjqdlitgphzacrhg',
            point='zozshyjhuouawinkghae',
            coordinate_lat=float(4.263027646682172),
            coordinate_lon=float(81.37912459042718),
            route_recommendation_json='hcjxqdarqjbvpxmzzxxv',
            footer_lines=None,
            amenity_descriptions=None,
            car_space_count=int(20),
            lorry_space_count=int(100)
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'mzunamhxvclipnjmdhle'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'edtlebhtnayqnwmvhwaa'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['lfjxnbpiewgfduwkzzpf', 'uxoopehqbamjinfjdiho']
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
        test_value = DisplayTypeenum.WARNING
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'wnjpgqfdaakfvgjnluan'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'ueikgyfzcgjuxuxcjnzk'
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
        test_value = 'dqgbeevllaxgckgnfdft'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(41)
        self.instance.start_lc_position = test_value
        self.assertEqual(self.instance.start_lc_position, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'bknyzjqdlitgphzacrhg'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'zozshyjhuouawinkghae'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(4.263027646682172)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(81.37912459042718)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'hcjxqdarqjbvpxmzzxxv'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = None
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_amenity_descriptions_property(self):
        """
        Test amenity_descriptions property
        """
        test_value = None
        self.instance.amenity_descriptions = test_value
        self.assertEqual(self.instance.amenity_descriptions, test_value)
    
    def test_car_space_count_property(self):
        """
        Test car_space_count property
        """
        test_value = int(20)
        self.instance.car_space_count = test_value
        self.assertEqual(self.instance.car_space_count, test_value)
    
    def test_lorry_space_count_property(self):
        """
        Test lorry_space_count property
        """
        test_value = int(100)
        self.instance.lorry_space_count = test_value
        self.assertEqual(self.instance.lorry_space_count, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ParkingLorry.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ParkingLorry.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

