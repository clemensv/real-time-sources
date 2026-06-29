"""
Test case for TravelTimeRoute
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_producer_data.us.wa.wsdot.traveltimes.traveltimeroute import TravelTimeRoute


class Test_TravelTimeRoute(unittest.TestCase):
    """
    Test case for TravelTimeRoute
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_TravelTimeRoute.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of TravelTimeRoute for testing
        """
        instance = TravelTimeRoute(
            travel_time_id='qckryuynagcfxsojjmdx',
            name='xndbfmkuvymgaiggxohd',
            description='psmsrlejeldhwcyjihbj',
            distance=float(11.87099895465752),
            average_time=int(28),
            current_time=int(27),
            time_updated='hqcavemjplxwsdvcsutn',
            start_description='qvwugafqonfkpolfxfbq',
            start_road_name='jmqdoeureeipwnotbjbr',
            start_direction='bkopcjwcelaxeaubuxah',
            start_milepost=float(98.16451530273753),
            start_latitude=float(12.474305158713939),
            start_longitude=float(37.62540904126326),
            end_description='fqycgdhdcvlialveqifm',
            end_road_name='mfajjtgogrmkfsimmmrn',
            end_direction='mxgtbqjogigcitffqfjg',
            end_milepost=float(36.448472663010826),
            end_latitude=float(49.1991413557518),
            end_longitude=float(40.87901219179665)
        )
        return instance

    
    def test_travel_time_id_property(self):
        """
        Test travel_time_id property
        """
        test_value = 'qckryuynagcfxsojjmdx'
        self.instance.travel_time_id = test_value
        self.assertEqual(self.instance.travel_time_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'xndbfmkuvymgaiggxohd'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'psmsrlejeldhwcyjihbj'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_distance_property(self):
        """
        Test distance property
        """
        test_value = float(11.87099895465752)
        self.instance.distance = test_value
        self.assertEqual(self.instance.distance, test_value)
    
    def test_average_time_property(self):
        """
        Test average_time property
        """
        test_value = int(28)
        self.instance.average_time = test_value
        self.assertEqual(self.instance.average_time, test_value)
    
    def test_current_time_property(self):
        """
        Test current_time property
        """
        test_value = int(27)
        self.instance.current_time = test_value
        self.assertEqual(self.instance.current_time, test_value)
    
    def test_time_updated_property(self):
        """
        Test time_updated property
        """
        test_value = 'hqcavemjplxwsdvcsutn'
        self.instance.time_updated = test_value
        self.assertEqual(self.instance.time_updated, test_value)
    
    def test_start_description_property(self):
        """
        Test start_description property
        """
        test_value = 'qvwugafqonfkpolfxfbq'
        self.instance.start_description = test_value
        self.assertEqual(self.instance.start_description, test_value)
    
    def test_start_road_name_property(self):
        """
        Test start_road_name property
        """
        test_value = 'jmqdoeureeipwnotbjbr'
        self.instance.start_road_name = test_value
        self.assertEqual(self.instance.start_road_name, test_value)
    
    def test_start_direction_property(self):
        """
        Test start_direction property
        """
        test_value = 'bkopcjwcelaxeaubuxah'
        self.instance.start_direction = test_value
        self.assertEqual(self.instance.start_direction, test_value)
    
    def test_start_milepost_property(self):
        """
        Test start_milepost property
        """
        test_value = float(98.16451530273753)
        self.instance.start_milepost = test_value
        self.assertEqual(self.instance.start_milepost, test_value)
    
    def test_start_latitude_property(self):
        """
        Test start_latitude property
        """
        test_value = float(12.474305158713939)
        self.instance.start_latitude = test_value
        self.assertEqual(self.instance.start_latitude, test_value)
    
    def test_start_longitude_property(self):
        """
        Test start_longitude property
        """
        test_value = float(37.62540904126326)
        self.instance.start_longitude = test_value
        self.assertEqual(self.instance.start_longitude, test_value)
    
    def test_end_description_property(self):
        """
        Test end_description property
        """
        test_value = 'fqycgdhdcvlialveqifm'
        self.instance.end_description = test_value
        self.assertEqual(self.instance.end_description, test_value)
    
    def test_end_road_name_property(self):
        """
        Test end_road_name property
        """
        test_value = 'mfajjtgogrmkfsimmmrn'
        self.instance.end_road_name = test_value
        self.assertEqual(self.instance.end_road_name, test_value)
    
    def test_end_direction_property(self):
        """
        Test end_direction property
        """
        test_value = 'mxgtbqjogigcitffqfjg'
        self.instance.end_direction = test_value
        self.assertEqual(self.instance.end_direction, test_value)
    
    def test_end_milepost_property(self):
        """
        Test end_milepost property
        """
        test_value = float(36.448472663010826)
        self.instance.end_milepost = test_value
        self.assertEqual(self.instance.end_milepost, test_value)
    
    def test_end_latitude_property(self):
        """
        Test end_latitude property
        """
        test_value = float(49.1991413557518)
        self.instance.end_latitude = test_value
        self.assertEqual(self.instance.end_latitude, test_value)
    
    def test_end_longitude_property(self):
        """
        Test end_longitude property
        """
        test_value = float(40.87901219179665)
        self.instance.end_longitude = test_value
        self.assertEqual(self.instance.end_longitude, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = TravelTimeRoute.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = TravelTimeRoute.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

