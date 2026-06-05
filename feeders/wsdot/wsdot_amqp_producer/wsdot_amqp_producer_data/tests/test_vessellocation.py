"""
Test case for VesselLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_amqp_producer_data.us.wa.wsdot.ferries.vessellocation import VesselLocation


class Test_VesselLocation(unittest.TestCase):
    """
    Test case for VesselLocation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VesselLocation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VesselLocation for testing
        """
        instance = VesselLocation(
            vessel_id='idjhpubswezwwxeqmuvl',
            vessel_name='kpmeqdddcllphzsoucsl',
            mmsi=int(82),
            in_service=False,
            at_dock=True,
            latitude=float(46.309492039808084),
            longitude=float(2.7634451571707963),
            speed=float(94.23073082030213),
            heading=int(79),
            departing_terminal_id=int(82),
            departing_terminal_name='rqbcghlzoxytazlrrrlm',
            departing_terminal_abbrev='imexpwaiwgyexpgiuwkv',
            arriving_terminal_id=int(6),
            arriving_terminal_name='wfrlxdlvbmgklxwkqjpi',
            arriving_terminal_abbrev='mbydwvqcqdxewdsjmiyz',
            scheduled_departure='dsfntbmbgdskgwvemhvx',
            left_dock='uznxdwcrgsbraseavokt',
            eta='ukpweeslxibwaouymiax',
            eta_basis='dzfmivjvwtugtqnjwuth',
            route_abbreviation='rrbjovkfeedgcnxesxrb',
            timestamp='jsuogpuwmjhxyxnrolge'
        )
        return instance

    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = 'idjhpubswezwwxeqmuvl'
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'kpmeqdddcllphzsoucsl'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(82)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_in_service_property(self):
        """
        Test in_service property
        """
        test_value = False
        self.instance.in_service = test_value
        self.assertEqual(self.instance.in_service, test_value)
    
    def test_at_dock_property(self):
        """
        Test at_dock property
        """
        test_value = True
        self.instance.at_dock = test_value
        self.assertEqual(self.instance.at_dock, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(46.309492039808084)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(2.7634451571707963)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(94.23073082030213)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(79)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_departing_terminal_id_property(self):
        """
        Test departing_terminal_id property
        """
        test_value = int(82)
        self.instance.departing_terminal_id = test_value
        self.assertEqual(self.instance.departing_terminal_id, test_value)
    
    def test_departing_terminal_name_property(self):
        """
        Test departing_terminal_name property
        """
        test_value = 'rqbcghlzoxytazlrrrlm'
        self.instance.departing_terminal_name = test_value
        self.assertEqual(self.instance.departing_terminal_name, test_value)
    
    def test_departing_terminal_abbrev_property(self):
        """
        Test departing_terminal_abbrev property
        """
        test_value = 'imexpwaiwgyexpgiuwkv'
        self.instance.departing_terminal_abbrev = test_value
        self.assertEqual(self.instance.departing_terminal_abbrev, test_value)
    
    def test_arriving_terminal_id_property(self):
        """
        Test arriving_terminal_id property
        """
        test_value = int(6)
        self.instance.arriving_terminal_id = test_value
        self.assertEqual(self.instance.arriving_terminal_id, test_value)
    
    def test_arriving_terminal_name_property(self):
        """
        Test arriving_terminal_name property
        """
        test_value = 'wfrlxdlvbmgklxwkqjpi'
        self.instance.arriving_terminal_name = test_value
        self.assertEqual(self.instance.arriving_terminal_name, test_value)
    
    def test_arriving_terminal_abbrev_property(self):
        """
        Test arriving_terminal_abbrev property
        """
        test_value = 'mbydwvqcqdxewdsjmiyz'
        self.instance.arriving_terminal_abbrev = test_value
        self.assertEqual(self.instance.arriving_terminal_abbrev, test_value)
    
    def test_scheduled_departure_property(self):
        """
        Test scheduled_departure property
        """
        test_value = 'dsfntbmbgdskgwvemhvx'
        self.instance.scheduled_departure = test_value
        self.assertEqual(self.instance.scheduled_departure, test_value)
    
    def test_left_dock_property(self):
        """
        Test left_dock property
        """
        test_value = 'uznxdwcrgsbraseavokt'
        self.instance.left_dock = test_value
        self.assertEqual(self.instance.left_dock, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'ukpweeslxibwaouymiax'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_eta_basis_property(self):
        """
        Test eta_basis property
        """
        test_value = 'dzfmivjvwtugtqnjwuth'
        self.instance.eta_basis = test_value
        self.assertEqual(self.instance.eta_basis, test_value)
    
    def test_route_abbreviation_property(self):
        """
        Test route_abbreviation property
        """
        test_value = 'rrbjovkfeedgcnxesxrb'
        self.instance.route_abbreviation = test_value
        self.assertEqual(self.instance.route_abbreviation, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'jsuogpuwmjhxyxnrolge'
        self.instance.timestamp = test_value
        self.assertEqual(self.instance.timestamp, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VesselLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VesselLocation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

