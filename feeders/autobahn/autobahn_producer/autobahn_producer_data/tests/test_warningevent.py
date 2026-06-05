"""
Test case for WarningEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.warningevent import WarningEvent
from autobahn_producer_data.displaytypeenum import DisplayTypeenum
from typing import Any
import datetime


class Test_WarningEvent(unittest.TestCase):
    """
    Test case for WarningEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WarningEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WarningEvent for testing
        """
        instance = WarningEvent(
            identifier='raxrrhqmsqyducvzawvc',
            road='yiddylwipjalfetqnrgg',
            road_ids=['xivdfoeyrfzobfrobnjl'],
            event_time=datetime.datetime.now(datetime.timezone.utc),
            display_type=DisplayTypeenum.WARNING,
            title='sfwtcpnruknuuweknnqo',
            subtitle='iousrgglolkzazkdpard',
            description_lines=None,
            future=True,
            is_blocked=True,
            icon='lsswhnohrynlkvprnmts',
            start_lc_position=int(75),
            start_timestamp=datetime.datetime.now(datetime.timezone.utc),
            extent='lmbnzhykjoqcfhlexbol',
            point='tymlejqfpwrnhxqkkmtd',
            coordinate_lat=float(9.617093556609667),
            coordinate_lon=float(85.2954756531973),
            geometry_json='uovzjlwufavmbfameikf',
            impact_lower='hagkhknmnsphcvylwcit',
            impact_upper='qugrspkhxvwgshlqsryd',
            impact_symbols=None,
            route_recommendation_json='sbjceyvausbzlqpcnezs',
            footer_lines=None,
            delay_minutes=int(20),
            average_speed_kmh=int(25),
            abnormal_traffic_type='cxqswabattgnlpvlonsx',
            source_name='nadqgxomfkgufubpuntf'
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'raxrrhqmsqyducvzawvc'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'yiddylwipjalfetqnrgg'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['xivdfoeyrfzobfrobnjl']
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
        test_value = 'sfwtcpnruknuuweknnqo'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'iousrgglolkzazkdpard'
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
        test_value = 'lsswhnohrynlkvprnmts'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(75)
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
        test_value = 'lmbnzhykjoqcfhlexbol'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'tymlejqfpwrnhxqkkmtd'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(9.617093556609667)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(85.2954756531973)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_geometry_json_property(self):
        """
        Test geometry_json property
        """
        test_value = 'uovzjlwufavmbfameikf'
        self.instance.geometry_json = test_value
        self.assertEqual(self.instance.geometry_json, test_value)
    
    def test_impact_lower_property(self):
        """
        Test impact_lower property
        """
        test_value = 'hagkhknmnsphcvylwcit'
        self.instance.impact_lower = test_value
        self.assertEqual(self.instance.impact_lower, test_value)
    
    def test_impact_upper_property(self):
        """
        Test impact_upper property
        """
        test_value = 'qugrspkhxvwgshlqsryd'
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
        test_value = 'sbjceyvausbzlqpcnezs'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = None
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_delay_minutes_property(self):
        """
        Test delay_minutes property
        """
        test_value = int(20)
        self.instance.delay_minutes = test_value
        self.assertEqual(self.instance.delay_minutes, test_value)
    
    def test_average_speed_kmh_property(self):
        """
        Test average_speed_kmh property
        """
        test_value = int(25)
        self.instance.average_speed_kmh = test_value
        self.assertEqual(self.instance.average_speed_kmh, test_value)
    
    def test_abnormal_traffic_type_property(self):
        """
        Test abnormal_traffic_type property
        """
        test_value = 'cxqswabattgnlpvlonsx'
        self.instance.abnormal_traffic_type = test_value
        self.assertEqual(self.instance.abnormal_traffic_type, test_value)
    
    def test_source_name_property(self):
        """
        Test source_name property
        """
        test_value = 'nadqgxomfkgufubpuntf'
        self.instance.source_name = test_value
        self.assertEqual(self.instance.source_name, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WarningEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WarningEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

