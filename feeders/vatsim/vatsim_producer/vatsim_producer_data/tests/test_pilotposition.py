"""
Test case for PilotPosition
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from vatsim_producer_data.net.vatsim.pilotposition import PilotPosition


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
            cid=int(52),
            callsign='irgwgfpwosknllvazdfp',
            latitude=float(15.233600753856413),
            longitude=float(7.694630203741404),
            altitude=int(66),
            groundspeed=int(26),
            heading=int(71),
            transponder='iolejhmqznahagycilno',
            qnh_mb=int(4),
            flight_rules='xrhoekwobehjtbrwgncy',
            aircraft_short='mwdieoeyjqnefgkmnbin',
            departure='sxbpeqgsagayhsraeefk',
            arrival='xveatrkyjisqfmzmjhyi',
            route='edsqhmktuksbpvfzxura',
            cruise_altitude='zfszwbdtwgjtzpryjlyr',
            pilot_rating=int(80),
            last_updated='ijfndecmitcqvdzhobrr'
        )
        return instance

    
    def test_cid_property(self):
        """
        Test cid property
        """
        test_value = int(52)
        self.instance.cid = test_value
        self.assertEqual(self.instance.cid, test_value)
    
    def test_callsign_property(self):
        """
        Test callsign property
        """
        test_value = 'irgwgfpwosknllvazdfp'
        self.instance.callsign = test_value
        self.assertEqual(self.instance.callsign, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(15.233600753856413)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(7.694630203741404)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = int(66)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_groundspeed_property(self):
        """
        Test groundspeed property
        """
        test_value = int(26)
        self.instance.groundspeed = test_value
        self.assertEqual(self.instance.groundspeed, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(71)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_transponder_property(self):
        """
        Test transponder property
        """
        test_value = 'iolejhmqznahagycilno'
        self.instance.transponder = test_value
        self.assertEqual(self.instance.transponder, test_value)
    
    def test_qnh_mb_property(self):
        """
        Test qnh_mb property
        """
        test_value = int(4)
        self.instance.qnh_mb = test_value
        self.assertEqual(self.instance.qnh_mb, test_value)
    
    def test_flight_rules_property(self):
        """
        Test flight_rules property
        """
        test_value = 'xrhoekwobehjtbrwgncy'
        self.instance.flight_rules = test_value
        self.assertEqual(self.instance.flight_rules, test_value)
    
    def test_aircraft_short_property(self):
        """
        Test aircraft_short property
        """
        test_value = 'mwdieoeyjqnefgkmnbin'
        self.instance.aircraft_short = test_value
        self.assertEqual(self.instance.aircraft_short, test_value)
    
    def test_departure_property(self):
        """
        Test departure property
        """
        test_value = 'sxbpeqgsagayhsraeefk'
        self.instance.departure = test_value
        self.assertEqual(self.instance.departure, test_value)
    
    def test_arrival_property(self):
        """
        Test arrival property
        """
        test_value = 'xveatrkyjisqfmzmjhyi'
        self.instance.arrival = test_value
        self.assertEqual(self.instance.arrival, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'edsqhmktuksbpvfzxura'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_cruise_altitude_property(self):
        """
        Test cruise_altitude property
        """
        test_value = 'zfszwbdtwgjtzpryjlyr'
        self.instance.cruise_altitude = test_value
        self.assertEqual(self.instance.cruise_altitude, test_value)
    
    def test_pilot_rating_property(self):
        """
        Test pilot_rating property
        """
        test_value = int(80)
        self.instance.pilot_rating = test_value
        self.assertEqual(self.instance.pilot_rating, test_value)
    
    def test_last_updated_property(self):
        """
        Test last_updated property
        """
        test_value = 'ijfndecmitcqvdzhobrr'
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

