"""
Test case for MonitoredVehicleJourney
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from entur_norway_producer_data.no.entur.monitoredvehiclejourney import MonitoredVehicleJourney
import datetime


class Test_MonitoredVehicleJourney(unittest.TestCase):
    """
    Test case for MonitoredVehicleJourney
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MonitoredVehicleJourney.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MonitoredVehicleJourney for testing
        """
        instance = MonitoredVehicleJourney(
            service_journey_id='sqszbuyzlmagqolvukix',
            operating_day='xktzyvhpvocyebjiovev',
            recorded_at_time=datetime.datetime.now(datetime.timezone.utc),
            line_ref='edjlxwadbswhxtcvslfz',
            operator_ref='jrmuybsazpvzitnrstjx',
            direction_ref='izwtljqbwmoieoocikqq',
            vehicle_mode='dyfajbbuloeosxyrdzta',
            published_line_name='dyjfpqydckvebuyvlrrv',
            origin_name='njbeoamumkuogylplrew',
            destination_name='isuwxmbhcxzssjdpnged',
            vehicle_ref='kxvjunpvjmwfnwhjfcxu',
            latitude=float(6.070270598786987),
            longitude=float(84.98082129419286),
            bearing=float(74.4435005987535),
            delay_seconds=int(58),
            occupancy_status='kzgkqeyfwqyryshjvwus',
            progress_status='cfcbfrvegoparrjwlkhx',
            monitored=False
        )
        return instance

    
    def test_service_journey_id_property(self):
        """
        Test service_journey_id property
        """
        test_value = 'sqszbuyzlmagqolvukix'
        self.instance.service_journey_id = test_value
        self.assertEqual(self.instance.service_journey_id, test_value)
    
    def test_operating_day_property(self):
        """
        Test operating_day property
        """
        test_value = 'xktzyvhpvocyebjiovev'
        self.instance.operating_day = test_value
        self.assertEqual(self.instance.operating_day, test_value)
    
    def test_recorded_at_time_property(self):
        """
        Test recorded_at_time property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.recorded_at_time = test_value
        self.assertEqual(self.instance.recorded_at_time, test_value)
    
    def test_line_ref_property(self):
        """
        Test line_ref property
        """
        test_value = 'edjlxwadbswhxtcvslfz'
        self.instance.line_ref = test_value
        self.assertEqual(self.instance.line_ref, test_value)
    
    def test_operator_ref_property(self):
        """
        Test operator_ref property
        """
        test_value = 'jrmuybsazpvzitnrstjx'
        self.instance.operator_ref = test_value
        self.assertEqual(self.instance.operator_ref, test_value)
    
    def test_direction_ref_property(self):
        """
        Test direction_ref property
        """
        test_value = 'izwtljqbwmoieoocikqq'
        self.instance.direction_ref = test_value
        self.assertEqual(self.instance.direction_ref, test_value)
    
    def test_vehicle_mode_property(self):
        """
        Test vehicle_mode property
        """
        test_value = 'dyfajbbuloeosxyrdzta'
        self.instance.vehicle_mode = test_value
        self.assertEqual(self.instance.vehicle_mode, test_value)
    
    def test_published_line_name_property(self):
        """
        Test published_line_name property
        """
        test_value = 'dyjfpqydckvebuyvlrrv'
        self.instance.published_line_name = test_value
        self.assertEqual(self.instance.published_line_name, test_value)
    
    def test_origin_name_property(self):
        """
        Test origin_name property
        """
        test_value = 'njbeoamumkuogylplrew'
        self.instance.origin_name = test_value
        self.assertEqual(self.instance.origin_name, test_value)
    
    def test_destination_name_property(self):
        """
        Test destination_name property
        """
        test_value = 'isuwxmbhcxzssjdpnged'
        self.instance.destination_name = test_value
        self.assertEqual(self.instance.destination_name, test_value)
    
    def test_vehicle_ref_property(self):
        """
        Test vehicle_ref property
        """
        test_value = 'kxvjunpvjmwfnwhjfcxu'
        self.instance.vehicle_ref = test_value
        self.assertEqual(self.instance.vehicle_ref, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(6.070270598786987)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(84.98082129419286)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_bearing_property(self):
        """
        Test bearing property
        """
        test_value = float(74.4435005987535)
        self.instance.bearing = test_value
        self.assertEqual(self.instance.bearing, test_value)
    
    def test_delay_seconds_property(self):
        """
        Test delay_seconds property
        """
        test_value = int(58)
        self.instance.delay_seconds = test_value
        self.assertEqual(self.instance.delay_seconds, test_value)
    
    def test_occupancy_status_property(self):
        """
        Test occupancy_status property
        """
        test_value = 'kzgkqeyfwqyryshjvwus'
        self.instance.occupancy_status = test_value
        self.assertEqual(self.instance.occupancy_status, test_value)
    
    def test_progress_status_property(self):
        """
        Test progress_status property
        """
        test_value = 'cfcbfrvegoparrjwlkhx'
        self.instance.progress_status = test_value
        self.assertEqual(self.instance.progress_status, test_value)
    
    def test_monitored_property(self):
        """
        Test monitored property
        """
        test_value = False
        self.instance.monitored = test_value
        self.assertEqual(self.instance.monitored, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MonitoredVehicleJourney.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MonitoredVehicleJourney.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

