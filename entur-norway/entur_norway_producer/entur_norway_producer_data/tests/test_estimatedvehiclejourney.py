"""
Test case for EstimatedVehicleJourney
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.estimatedvehiclejourney import EstimatedVehicleJourney
from entur_norway_producer_data.no.entur.estimatedcall import EstimatedCall
import datetime


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
            service_journey_id='aajghwhkmqlslkpyaats',
            operating_day='rmfpdqpwzhpjtxizevhk',
            line_ref='vjthpnascubrkrrjqvck',
            operator_ref='dqshzyttlnjaoieldfyz',
            direction_ref='ntzbgkuwbuvtrjuglpri',
            vehicle_mode='pdcbobizdithnstduknc',
            published_line_name='kyxpfjonzwjddaxljplu',
            route_ref='iuteivxwjglfmvfpqgvm',
            origin_name='ukrxxanljgdnhcaabsyg',
            destination_name='edfwurwltigluqgejjhq',
            is_cancellation=False,
            is_extra_journey=True,
            is_complete_stop_sequence=False,
            monitored=True,
            data_source='lkkgbpdtoqquahoxlroh',
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            estimated_calls=[EstimatedCall(stop_point_ref='NSR:Quay:1', order=1, stop_point_name=None, aimed_arrival_time=None, expected_arrival_time=None, aimed_departure_time=None, expected_departure_time=None, arrival_status=None, departure_status=None, departure_platform_name=None, arrival_boarding_activity=None, departure_boarding_activity=None, is_cancellation=None, is_extra_stop=None)]
        )
        return instance

    
    def test_service_journey_id_property(self):
        """
        Test service_journey_id property
        """
        test_value = 'aajghwhkmqlslkpyaats'
        self.instance.service_journey_id = test_value
        self.assertEqual(self.instance.service_journey_id, test_value)
    
    def test_operating_day_property(self):
        """
        Test operating_day property
        """
        test_value = 'rmfpdqpwzhpjtxizevhk'
        self.instance.operating_day = test_value
        self.assertEqual(self.instance.operating_day, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'vjthpnascubrkrrjqvck'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'dqshzyttlnjaoieldfyz'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'ntzbgkuwbuvtrjuglpri'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_vehicle_mode_property(self):
        """
        Test vehicle_mode property
        """
        test_value = 'pdcbobizdithnstduknc'
        self.instance.vehicle_mode = test_value
        self.assertEqual(self.instance.vehicle_mode, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'kyxpfjonzwjddaxljplu'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_route_ref_property(self):
        """
        Test route_ref property
        """
        test_value = 'iuteivxwjglfmvfpqgvm'
        self.instance.route_ref = test_value
        self.assertEqual(self.instance.route_ref, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'ukrxxanljgdnhcaabsyg'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'edfwurwltigluqgejjhq'
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
        test_value = False
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
        test_value = 'lkkgbpdtoqquahoxlroh'
        self.instance.data_source = test_value
        self.assertEqual(self.instance.data_source, test_value)
    
    def test_recorded_at_time_property(self):
        """
        Test recorded_at_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.recorded_at_time = test_value
        self.assertEqual(self.instance.recorded_at_time, test_value)
    
    def test_estimated_calls_property(self):
        """
        Test estimated_calls property
        """
        test_value = [None]
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
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = EstimatedVehicleJourney.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = EstimatedVehicleJourney.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

