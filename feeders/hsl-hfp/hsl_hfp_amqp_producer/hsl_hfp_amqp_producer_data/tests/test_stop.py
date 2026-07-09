"""
Test case for Stop
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_amqp_producer_data.fi.hsl.gtfs.stop import Stop


class Test_Stop(unittest.TestCase):
    """
    Test case for Stop
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Stop.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Stop for testing
        """
        instance = Stop(
            stop_id='whaxwbapypbbtlvoqkvj',
            stop_code='kpuvehjplbrswqnofrqi',
            stop_name='olprrhyptjswxxihiqbz',
            stop_desc='cruycahcufwxbvgmseqe',
            stop_lat=float(11.515290970394254),
            stop_lon=float(33.44540264506346),
            zone_id='rddllnneejobrovrbdig',
            stop_url='xjnfrtdydufarwliuicn',
            location_type=int(27),
            parent_station='rjlnlrugwkeaorgaidap',
            platform_code='dysexyftlfqynppgkmlg',
            wheelchair_boarding=int(73),
            vehicle_type=int(95),
            digistop_id='miyquoqycpbmjjqlpesb'
        )
        return instance

    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'whaxwbapypbbtlvoqkvj'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_stop_code_property(self):
        """
        Test stop_code property
        """
        test_value = 'kpuvehjplbrswqnofrqi'
        self.instance.stop_code = test_value
        self.assertEqual(self.instance.stop_code, test_value)
    
    def test_stop_name_property(self):
        """
        Test stop_name property
        """
        test_value = 'olprrhyptjswxxihiqbz'
        self.instance.stop_name = test_value
        self.assertEqual(self.instance.stop_name, test_value)
    
    def test_stop_desc_property(self):
        """
        Test stop_desc property
        """
        test_value = 'cruycahcufwxbvgmseqe'
        self.instance.stop_desc = test_value
        self.assertEqual(self.instance.stop_desc, test_value)
    
    def test_stop_lat_property(self):
        """
        Test stop_lat property
        """
        test_value = float(11.515290970394254)
        self.instance.stop_lat = test_value
        self.assertEqual(self.instance.stop_lat, test_value)
    
    def test_stop_lon_property(self):
        """
        Test stop_lon property
        """
        test_value = float(33.44540264506346)
        self.instance.stop_lon = test_value
        self.assertEqual(self.instance.stop_lon, test_value)
    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'rddllnneejobrovrbdig'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_stop_url_property(self):
        """
        Test stop_url property
        """
        test_value = 'xjnfrtdydufarwliuicn'
        self.instance.stop_url = test_value
        self.assertEqual(self.instance.stop_url, test_value)
    
    def test_location_type_property(self):
        """
        Test location_type property
        """
        test_value = int(27)
        self.instance.location_type = test_value
        self.assertEqual(self.instance.location_type, test_value)
    
    def test_parent_station_property(self):
        """
        Test parent_station property
        """
        test_value = 'rjlnlrugwkeaorgaidap'
        self.instance.parent_station = test_value
        self.assertEqual(self.instance.parent_station, test_value)
    
    def test_platform_code_property(self):
        """
        Test platform_code property
        """
        test_value = 'dysexyftlfqynppgkmlg'
        self.instance.platform_code = test_value
        self.assertEqual(self.instance.platform_code, test_value)
    
    def test_wheelchair_boarding_property(self):
        """
        Test wheelchair_boarding property
        """
        test_value = int(73)
        self.instance.wheelchair_boarding = test_value
        self.assertEqual(self.instance.wheelchair_boarding, test_value)
    
    def test_vehicle_type_property(self):
        """
        Test vehicle_type property
        """
        test_value = int(95)
        self.instance.vehicle_type = test_value
        self.assertEqual(self.instance.vehicle_type, test_value)
    
    def test_digistop_id_property(self):
        """
        Test digistop_id property
        """
        test_value = 'miyquoqycpbmjjqlpesb'
        self.instance.digistop_id = test_value
        self.assertEqual(self.instance.digistop_id, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Stop.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Stop.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

