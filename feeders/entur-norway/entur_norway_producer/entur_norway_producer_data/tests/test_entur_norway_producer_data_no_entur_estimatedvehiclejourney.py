"""
Test case for EstimatedVehicleJourney
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.estimatedvehiclejourney import EstimatedVehicleJourney
from test_entur_norway_producer_data_no_entur_estimatedcall import Test_EstimatedCall


class Test_EstimatedVehicleJourney(unittest.TestCase):
    """
    Test case for EstimatedVehicleJourney
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_EstimatedVehicleJourney.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of EstimatedVehicleJourney for testing
        """
        instance = EstimatedVehicleJourney(
            service_journey_id='hxmtlawvjnjwsxtohjwy',
            operating_day='yoznyaziytlookokzpkv',
            line_ref='voirnzljhsayqtmuhubd',
            operator_ref='qmmjlefolkoaxbrqnkzb',
            direction_ref='cmajryuzalyhfkdqcegz',
            vehicle_mode='rvstaafbadhnikjslzmr',
            published_line_name='qppvrowttbvchxhlhgvi',
            route_ref='weudinnldqyibycmkuuy',
            origin_name='kmauiazabjeucnovwknr',
            destination_name='hbakpsxigxhapdnvbvsd',
            is_cancellation=False,
            is_extra_journey=True,
            is_complete_stop_sequence=True,
            monitored=True,
            data_source='xihqwinmvxzwglmdnsis',
            recorded_at_time='emquybqgeavjejqiebbe',
            estimated_calls=[Test_EstimatedCall.create_instance(), Test_EstimatedCall.create_instance()]
        )
        return instance

    
    def test_service_journey_id_property(self):
        """
        Test service_journey_id property
        """
        test_value = 'hxmtlawvjnjwsxtohjwy'
        self.instance.service_journey_id = test_value
        self.assertEqual(self.instance.service_journey_id, test_value)
    
    def test_operating_day_property(self):
        """
        Test operating_day property
        """
        test_value = 'yoznyaziytlookokzpkv'
        self.instance.operating_day = test_value
        self.assertEqual(self.instance.operating_day, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'voirnzljhsayqtmuhubd'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'qmmjlefolkoaxbrqnkzb'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'cmajryuzalyhfkdqcegz'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_vehicle_mode_property(self):
        """
        Test vehicle_mode property
        """
        test_value = 'rvstaafbadhnikjslzmr'
        self.instance.vehicle_mode = test_value
        self.assertEqual(self.instance.vehicle_mode, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'qppvrowttbvchxhlhgvi'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_route_ref_property(self):
        """
        Test route_ref property
        """
        test_value = 'weudinnldqyibycmkuuy'
        self.instance.route_ref = test_value
        self.assertEqual(self.instance.route_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'kmauiazabjeucnovwknr'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'hbakpsxigxhapdnvbvsd'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_is_cancellation_property(self):
        """
        Test is_cancellation property
        """
        test_value = False
        self.instance.is_cancellation = test_value
        self.assertEqual(self.instance.is_cancellation, test_value)
    
    def test_is_extra_journey_property(self):
        """
        Test is_extra_journey property
        """
        test_value = True
        self.instance.is_extra_journey = test_value
        self.assertEqual(self.instance.is_extra_journey, test_value)
    
    def test_is_complete_stop_sequence_property(self):
        """
        Test is_complete_stop_sequence property
        """
        test_value = True
        self.instance.is_complete_stop_sequence = test_value
        self.assertEqual(self.instance.is_complete_stop_sequence, test_value)
    
    def test_monitored_property(self):
        """
        Test monitored property
        """
        test_value = True
        self.instance.monitored = test_value
        self.assertEqual(self.instance.monitored, test_value)
    
    def test_data_source_property(self):
        """
        Test data_source property
        """
        test_value = 'xihqwinmvxzwglmdnsis'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_recorded_at_time_property(self):
        """
        Test recorded_at_time property
        """
        test_value = 'emquybqgeavjejqiebbe'
        self.instance.recorded_at_time = test_value
        self.assertEqual(self.instance.recorded_at_time, test_value)
    
    def test_estimated_calls_property(self):
        """
        Test estimated_calls property
        """
        test_value = [Test_EstimatedCall.create_instance(), Test_EstimatedCall.create_instance()]
        self.instance.estimated_calls = test_value
        self.assertEqual(self.instance.estimated_calls, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EstimatedVehicleJourney.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
