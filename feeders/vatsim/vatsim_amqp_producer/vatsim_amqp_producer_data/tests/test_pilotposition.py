"""
Test case for PilotPosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from vatsim_amqp_producer_data.net.vatsim.pilotposition import PilotPosition


class Test_PilotPosition(unittest.TestCase):
    """
    Test case for PilotPosition
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PilotPosition.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PilotPosition for testing
        """
        instance = PilotPosition(
            cid=int(35),
            callsign='otcxbniadolberqwrsuw',
            latitude=float(22.847745806696807),
            longitude=float(35.77089157916934),
            altitude=int(75),
            groundspeed=int(18),
            heading=int(76),
            transponder='wqzwwbgmfbywuslpdmyp',
            qnh_mb=int(36),
            flight_rules='snrvpncmopgkzlzblcww',
            aircraft_short='buqndlxiktklgskgfylz',
            departure='azmmansvqfmapszbnoqm',
            arrival='lmchwuimftclxxlqokwx',
            route='vkhatwifmppitwhlfpax',
            cruise_altitude='ajlzflcbnrubqpxsvsva',
            pilot_rating=int(34),
            last_updated='jrmbmvlqppoxzscrdzej'
        )
        return instance

    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = int(35)
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'otcxbniadolberqwrsuw'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(22.847745806696807)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(35.77089157916934)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = int(75)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_groundspeed_property(self):
        """
        Test groundspeed property
        """
        test_value = int(18)
        self.instance.groundspeed = test_value
        self.assertEqual(self.instance.groundspeed, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(76)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_transponder_property(self):
        """
        Test transponder property
        """
        test_value = 'wqzwwbgmfbywuslpdmyp'
        self.instance.transponder = test_value
        self.assertEqual(self.instance.transponder, test_value)
    
    def test_qnh_mb_property(self):
        """
        Test qnh_mb property
        """
        test_value = int(36)
        self.instance.qnh_mb = test_value
        self.assertEqual(self.instance.qnh_mb, test_value)
    
    def test_flight_rules_property(self):
        """
        Test flight_rules property
        """
        test_value = 'snrvpncmopgkzlzblcww'
        self.instance.flight_rules = test_value
        self.assertEqual(self.instance.flight_rules, test_value)
    
    def test_aircraft_short_property(self):
        """
        Test aircraft_short property
        """
        test_value = 'buqndlxiktklgskgfylz'
        self.instance.aircraft_short = test_value
        self.assertEqual(self.instance.aircraft_short, test_value)
    
    def test_departure_property(self):
        """
        Test departure property
        """
        test_value = 'azmmansvqfmapszbnoqm'
        self.instance.departure = test_value
        self.assertEqual(self.instance.departure, test_value)
    
    def test_arrival_property(self):
        """
        Test arrival property
        """
        test_value = 'lmchwuimftclxxlqokwx'
        self.instance.arrival = test_value
        self.assertEqual(self.instance.arrival, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'vkhatwifmppitwhlfpax'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_cruise_altitude_property(self):
        """
        Test cruise_altitude property
        """
        test_value = 'ajlzflcbnrubqpxsvsva'
        self.instance.cruise_altitude = test_value
        self.assertEqual(self.instance.cruise_altitude, test_value)
    
    def test_pilot_rating_property(self):
        """
        Test pilot_rating property
        """
        test_value = int(34)
        self.instance.pilot_rating = test_value
        self.assertEqual(self.instance.pilot_rating, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = 'jrmbmvlqppoxzscrdzej'
        self.instance.last_updated = test_value
        self.assertEqual(self.instance.last_updated, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PilotPosition.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PilotPosition.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

