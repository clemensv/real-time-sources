"""
Test case for ParkingLorry
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.de.autobahn.parkinglorry import ParkingLorry


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
            identifier='quwsuakogipbnquyjtnd',
            road='qkycetuygfwmxpqhufqi',
            road_ids=['ymlhqczbhzoeifzzbexq'],
            event_time='tmsfxtdgnghbyjcqvksn',
            display_type='plirjiwdnbekxwpkllvq',
            title='nxsafxxhqkywguesvaxq',
            subtitle='eabpvpwqaccxaopwptrc',
            description_lines=['tryjuiythhwvnoopnrry', 'mqahcrnccvgkwjekmjjt'],
            future=False,
            is_blocked=True,
            icon='fwltjiecrkmruaffijdw',
            start_lc_position=int(68),
            extent='jecbqzpkfizdbpwddlkq',
            point='rwxphpoakfwthmxvpmvp',
            coordinate_lat=float(41.92128362599878),
            coordinate_lon=float(64.32292287619569),
            route_recommendation_json='btumwgixpvznqcpxsxiv',
            footer_lines=['gwvrxtuwzfkzxcxfpmme', 'sdccszdkvetsrvamzbuy', 'snwsrqymduhtxmbsfmbb', 'efzujlrajkyswwdbiysb'],
            amenity_descriptions=['kcnsaccsmhyrbocdsrjf', 'gzabieuofvznyfcsjwvv'],
            car_space_count=int(70),
            lorry_space_count=int(41)
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'quwsuakogipbnquyjtnd'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'qkycetuygfwmxpqhufqi'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['ymlhqczbhzoeifzzbexq']
        self.instance.road_ids = test_value
        self.assertEqual(self.instance.road_ids, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'tmsfxtdgnghbyjcqvksn'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_display_type_property(self):
        """
        Test display_type property
        """
        test_value = 'plirjiwdnbekxwpkllvq'
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'nxsafxxhqkywguesvaxq'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'eabpvpwqaccxaopwptrc'
        self.instance.subtitle = test_value
        self.assertEqual(self.instance.subtitle, test_value)
    
    def test_description_lines_property(self):
        """
        Test description_lines property
        """
        test_value = ['tryjuiythhwvnoopnrry', 'mqahcrnccvgkwjekmjjt']
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
        test_value = 'fwltjiecrkmruaffijdw'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(68)
        self.instance.start_lc_position = test_value
        self.assertEqual(self.instance.start_lc_position, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'jecbqzpkfizdbpwddlkq'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'rwxphpoakfwthmxvpmvp'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(41.92128362599878)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(64.32292287619569)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'btumwgixpvznqcpxsxiv'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = ['gwvrxtuwzfkzxcxfpmme', 'sdccszdkvetsrvamzbuy', 'snwsrqymduhtxmbsfmbb', 'efzujlrajkyswwdbiysb']
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_amenity_descriptions_property(self):
        """
        Test amenity_descriptions property
        """
        test_value = ['kcnsaccsmhyrbocdsrjf', 'gzabieuofvznyfcsjwvv']
        self.instance.amenity_descriptions = test_value
        self.assertEqual(self.instance.amenity_descriptions, test_value)
    
    def test_car_space_count_property(self):
        """
        Test car_space_count property
        """
        test_value = int(70)
        self.instance.car_space_count = test_value
        self.assertEqual(self.instance.car_space_count, test_value)
    
    def test_lorry_space_count_property(self):
        """
        Test lorry_space_count property
        """
        test_value = int(41)
        self.instance.lorry_space_count = test_value
        self.assertEqual(self.instance.lorry_space_count, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ParkingLorry.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
