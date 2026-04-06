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
            identifier='fmyiufqukrihiwotuqwi',
            road_ids=['bgjungtljvxwahihrwhg'],
            event_time='fotkbtxwbhnnonmxeefs',
            display_type='skktobuvlzkxqyadabrc',
            title='cnbcdlvaqmwjskqkskbp',
            subtitle='iyyrucpxsoynkqnqwogm',
            description_lines=['mgipdvtyshlqyrbpmxtl', 'mututozrxabnlcricajf', 'gtllnphwfmhzokwfgyhv', 'cpwnpmfkraariyegvimo'],
            future=False,
            is_blocked=False,
            icon='iveynkgxgwymsxlowznr',
            start_lc_position=int(57),
            start_timestamp='ztxcgcdwczhxlxmcocmt',
            extent='acmpfgnxxpdoqnmmuccy',
            point='slaurjwqrxrjabxsbkmg',
            coordinate_lat=float(3.6551352313334173),
            coordinate_lon=float(94.90911660858717),
            geometry_json='udjrpdqputwjvpnkowhd',
            impact_lower='kthttcrorqijyqdkijxj',
            impact_upper='ysbojomrzcnfnuordcqk',
            impact_symbols=['hghwdmlnmfyrchknatvz', 'zweiytwwmmnlpinhqbnm', 'ewlqemrobaggipsofcmm'],
            route_recommendation_json='llctjswlbpvxaqczoihw',
            footer_lines=['btwplfskwngiqsgjhjqf', 'bgaxpurakepquunirltm', 'bzcipwiyynlyafylnvna']
        )
        return instance

    
    def test_identifier_property(self):
        """
        Test identifier property
        """
        test_value = 'fmyiufqukrihiwotuqwi'
        self.instance.identifier = test_value
        self.assertEqual(self.instance.identifier, test_value)
    
    def test_road_ids_property(self):
        """
        Test road_ids property
        """
        test_value = ['bgjungtljvxwahihrwhg']
        self.instance.road_ids = test_value
        self.assertEqual(self.instance.road_ids, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'fotkbtxwbhnnonmxeefs'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_display_type_property(self):
        """
        Test display_type property
        """
        test_value = 'skktobuvlzkxqyadabrc'
        self.instance.display_type = test_value
        self.assertEqual(self.instance.display_type, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'cnbcdlvaqmwjskqkskbp'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_subtitle_property(self):
        """
        Test subtitle property
        """
        test_value = 'iyyrucpxsoynkqnqwogm'
        self.instance.subtitle = test_value
        self.assertEqual(self.instance.subtitle, test_value)
    
    def test_description_lines_property(self):
        """
        Test description_lines property
        """
        test_value = ['mgipdvtyshlqyrbpmxtl', 'mututozrxabnlcricajf', 'gtllnphwfmhzokwfgyhv', 'cpwnpmfkraariyegvimo']
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
        test_value = 'iveynkgxgwymsxlowznr'
        self.instance.icon = test_value
        self.assertEqual(self.instance.icon, test_value)
    
    def test_start_lc_position_property(self):
        """
        Test start_lc_position property
        """
        test_value = int(57)
        self.instance.start_lc_position = test_value
        self.assertEqual(self.instance.start_lc_position, test_value)
    
    def test_start_timestamp_property(self):
        """
        Test start_timestamp property
        """
        test_value = 'ztxcgcdwczhxlxmcocmt'
        self.instance.start_timestamp = test_value
        self.assertEqual(self.instance.start_timestamp, test_value)
    
    def test_extent_property(self):
        """
        Test extent property
        """
        test_value = 'acmpfgnxxpdoqnmmuccy'
        self.instance.extent = test_value
        self.assertEqual(self.instance.extent, test_value)
    
    def test_point_property(self):
        """
        Test point property
        """
        test_value = 'slaurjwqrxrjabxsbkmg'
        self.instance.point = test_value
        self.assertEqual(self.instance.point, test_value)
    
    def test_coordinate_lat_property(self):
        """
        Test coordinate_lat property
        """
        test_value = float(3.6551352313334173)
        self.instance.coordinate_lat = test_value
        self.assertEqual(self.instance.coordinate_lat, test_value)
    
    def test_coordinate_lon_property(self):
        """
        Test coordinate_lon property
        """
        test_value = float(94.90911660858717)
        self.instance.coordinate_lon = test_value
        self.assertEqual(self.instance.coordinate_lon, test_value)
    
    def test_geometry_json_property(self):
        """
        Test geometry_json property
        """
        test_value = 'udjrpdqputwjvpnkowhd'
        self.instance.geometry_json = test_value
        self.assertEqual(self.instance.geometry_json, test_value)
    
    def test_impact_lower_property(self):
        """
        Test impact_lower property
        """
        test_value = 'kthttcrorqijyqdkijxj'
        self.instance.impact_lower = test_value
        self.assertEqual(self.instance.impact_lower, test_value)
    
    def test_impact_upper_property(self):
        """
        Test impact_upper property
        """
        test_value = 'ysbojomrzcnfnuordcqk'
        self.instance.impact_upper = test_value
        self.assertEqual(self.instance.impact_upper, test_value)
    
    def test_impact_symbols_property(self):
        """
        Test impact_symbols property
        """
        test_value = ['hghwdmlnmfyrchknatvz', 'zweiytwwmmnlpinhqbnm', 'ewlqemrobaggipsofcmm']
        self.instance.impact_symbols = test_value
        self.assertEqual(self.instance.impact_symbols, test_value)
    
    def test_route_recommendation_json_property(self):
        """
        Test route_recommendation_json property
        """
        test_value = 'llctjswlbpvxaqczoihw'
        self.instance.route_recommendation_json = test_value
        self.assertEqual(self.instance.route_recommendation_json, test_value)
    
    def test_footer_lines_property(self):
        """
        Test footer_lines property
        """
        test_value = ['btwplfskwngiqsgjhjqf', 'bgaxpurakepquunirltm', 'bzcipwiyynlyafylnvna']
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
