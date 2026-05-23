"""
Test case for RoadEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from autobahn_producer_data.de.autobahn.roadevent import RoadEvent


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
            identifier='wcourdljqgxnxylnplsd',
            road='fcoyyrtlmjfqxvnogoqc',
            road_ids=['ilsdfchheptuonpdpilf', 'cagdrdhaynkdgjfpsihr'],
            event_time='wvgpkbignjqeglaiqmyw',
            display_type='pjrrxdggfneqcjlsjkgp',
            title='qltpcrosfunqtazjewep',
            subtitle='uxwdslyuvsejxejfvnbi',
            description_lines=['uhlswxkbycjvvfdcbhgv'],
            future=False,
            is_blocked=False,
            icon='anifrcezzlqiczanbygc',
            start_lc_position=int(34),
            start_timestamp='ljnllqhmgbrrevcruuvm',
            extent='twguppevkdrjxyirmtib',
            point='vvjlzfiiwbvdfemkhitg',
            coordinate_lat=float(36.66839098387326),
            coordinate_lon=float(11.677983239518008),
            geometry_json='xpynfockulklfnfazmjv',
            impact_lower='hhusenmgtzjmgxhwpioe',
            impact_upper='abnojyzprqcxxzyxrnlz',
            impact_symbols=['ghjdhhycuizhwltuffkj', 'nsqvutfibwgdqxypssdk'],
            route_recommendation_json='nasrnrssijbbqgnukjxj',
            footer_lines=['bwhrtkwqufytandxrwtb', 'qgxwnktbdlyrfrniwtft']
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'wcourdljqgxnxylnplsd'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_property(self):
        """
        Test road property
        """
        test_value = 'fcoyyrtlmjfqxvnogoqc'
        self.instance.road = test_value
        self.assertEqual(self.instance.road, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['ilsdfchheptuonpdpilf', 'cagdrdhaynkdgjfpsihr']
        self.instance.road_ids = test_value
        self.assertEqual(self.instance.road_ids, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'wvgpkbignjqeglaiqmyw'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_display_type_property(self):
        """
        Test display_type property
        """
        test_value = 'pjrrxdggfneqcjlsjkgp'
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'qltpcrosfunqtazjewep'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'uxwdslyuvsejxejfvnbi'
        self.instance.subtitle = test_value
        self.assertEqual(self.instance.subtitle, test_value)
    
    def test_description_lines_property(self):
        """
        Test description_lines property
        """
        test_value = ['uhlswxkbycjvvfdcbhgv']
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
        test_value = 'anifrcezzlqiczanbygc'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(34)
        self.instance.start_lc_position = test_value
        self.assertEqual(self.instance.start_lc_position, test_value)
    
    def test_start_timestamp_property(self):
        """
        Test start_timestamp property
        """
        test_value = 'ljnllqhmgbrrevcruuvm'
        self.instance.start_timestamp = test_value
        self.assertEqual(self.instance.start_timestamp, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'twguppevkdrjxyirmtib'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'vvjlzfiiwbvdfemkhitg'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(36.66839098387326)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(11.677983239518008)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_geometry_json_property(self):
        """
        Test geometry_json property
        """
        test_value = 'xpynfockulklfnfazmjv'
        self.instance.geometry_json = test_value
        self.assertEqual(self.instance.geometry_json, test_value)
    
    def test_impact_lower_property(self):
        """
        Test impact_lower property
        """
        test_value = 'hhusenmgtzjmgxhwpioe'
        self.instance.impact_lower = test_value
        self.assertEqual(self.instance.impact_lower, test_value)
    
    def test_impact_upper_property(self):
        """
        Test impact_upper property
        """
        test_value = 'abnojyzprqcxxzyxrnlz'
        self.instance.impact_upper = test_value
        self.assertEqual(self.instance.impact_upper, test_value)
    
    def test_impact_symbols_property(self):
        """
        Test impact_symbols property
        """
        test_value = ['ghjdhhycuizhwltuffkj', 'nsqvutfibwgdqxypssdk']
        self.instance.impact_symbols = test_value
        self.assertEqual(self.instance.impact_symbols, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'nasrnrssijbbqgnukjxj'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = ['bwhrtkwqufytandxrwtb', 'qgxwnktbdlyrfrniwtft']
        self.instance.footer_lines = test_value
        self.assertEqual(self.instance.footer_lines, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = RoadEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
