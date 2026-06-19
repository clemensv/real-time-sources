"""
Test case for DatedServiceJourney
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.datedservicejourney import DatedServiceJourney


class Test_DatedServiceJourney(unittest.TestCase):
    """
    Test case for DatedServiceJourney
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_DatedServiceJourney.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of DatedServiceJourney for testing
        """
        instance = DatedServiceJourney(
            service_journey_id='cvmjvetmnwhtvqsmbqmj',
            operating_day='myoecsvfvfslscaqsbed',
            line_ref='vxizvnyeyvfppubdxqjv',
            operator_ref='hfatoybrktdctduyuoww',
            direction_ref='olyqwfytyzmccvxsvckd',
            vehicle_mode='wghbcygfrxhmtuzidsvv',
            route_ref='igedbkwyfawarekwbcnt',
            published_line_name='grunizrygifmxxitnesf',
            external_line_ref='vlzgtskxvqgtehjtriay',
            origin_name='afpfrexoqlwmwpcfspaa',
            destination_name='rwlifoepdtarburbqexv',
            data_source='wogupxplfibswqzthkab'
        )
        return instance

    
    def test_service_journey_id_property(self):
        """
        Test service_journey_id property
        """
        test_value = 'cvmjvetmnwhtvqsmbqmj'
        self.instance.service_journey_id = test_value
        self.assertEqual(self.instance.service_journey_id, test_value)
    
    def test_operating_day_property(self):
        """
        Test operating_day property
        """
        test_value = 'myoecsvfvfslscaqsbed'
        self.instance.operating_day = test_value
        self.assertEqual(self.instance.operating_day, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'vxizvnyeyvfppubdxqjv'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'hfatoybrktdctduyuoww'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'olyqwfytyzmccvxsvckd'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_vehicle_mode_property(self):
        """
        Test vehicle_mode property
        """
        test_value = 'wghbcygfrxhmtuzidsvv'
        self.instance.vehicle_mode = test_value
        self.assertEqual(self.instance.vehicle_mode, test_value)
    
    def test_route_ref_property(self):
        """
        Test route_ref property
        """
        test_value = 'igedbkwyfawarekwbcnt'
        self.instance.route_ref = test_value
        self.assertEqual(self.instance.route_ref, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'grunizrygifmxxitnesf'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_external_line_ref_property(self):
        """
        Test external_line_ref property
        """
        test_value = 'vlzgtskxvqgtehjtriay'
        self.instance.external_line_ref = test_value
        self.assertEqual(self.instance.external_line_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'afpfrexoqlwmwpcfspaa'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'rwlifoepdtarburbqexv'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'wogupxplfibswqzthkab'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = DatedServiceJourney.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = DatedServiceJourney.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

