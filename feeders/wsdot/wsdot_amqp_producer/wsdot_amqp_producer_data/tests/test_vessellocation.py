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
            vessel_id='vqdidhxkhpypvwwargsq',
            vessel_name='jndlariguvwvxgrgirdq',
            mmsi=int(89),
            in_service=False,
            at_dock=True,
            latitude=float(53.425719689877674),
            longitude=float(74.62352721623233),
            speed=float(53.35616948321902),
            heading=int(33),
            departing_terminal_id=int(44),
            departing_terminal_name='jlteukyonymmkuawgube',
            departing_terminal_abbrev='tklipkcelnhywmadwjgm',
            arriving_terminal_id=int(38),
            arriving_terminal_name='johopkcbyutdytbaqiry',
            arriving_terminal_abbrev='glnjhklmrylnqewgqjjt',
            scheduled_departure='sbtqneunbqnjxxzsvrfv',
            left_dock='exgqwmbnaeylaruuimjy',
            eta='qchpetmppyckrizrbndh',
            eta_basis='uhexnpllrwyccetkoiwh',
            route_abbreviation='yzlfyqefvuwhvclxwurb',
            timestamp='iktokvjrgywttygprevy'
        )
        return instance

    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = 'vqdidhxkhpypvwwargsq'
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'jndlariguvwvxgrgirdq'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(89)
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
        test_value = float(53.425719689877674)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(74.62352721623233)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(53.35616948321902)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(33)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_departing_terminal_id_property(self):
        """
        Test departing_terminal_id property
        """
        test_value = int(44)
        self.instance.departing_terminal_id = test_value
        self.assertEqual(self.instance.departing_terminal_id, test_value)
    
    def test_departing_terminal_name_property(self):
        """
        Test departing_terminal_name property
        """
        test_value = 'jlteukyonymmkuawgube'
        self.instance.departing_terminal_name = test_value
        self.assertEqual(self.instance.departing_terminal_name, test_value)
    
    def test_departing_terminal_abbrev_property(self):
        """
        Test departing_terminal_abbrev property
        """
        test_value = 'tklipkcelnhywmadwjgm'
        self.instance.departing_terminal_abbrev = test_value
        self.assertEqual(self.instance.departing_terminal_abbrev, test_value)
    
    def test_arriving_terminal_id_property(self):
        """
        Test arriving_terminal_id property
        """
        test_value = int(38)
        self.instance.arriving_terminal_id = test_value
        self.assertEqual(self.instance.arriving_terminal_id, test_value)
    
    def test_arriving_terminal_name_property(self):
        """
        Test arriving_terminal_name property
        """
        test_value = 'johopkcbyutdytbaqiry'
        self.instance.arriving_terminal_name = test_value
        self.assertEqual(self.instance.arriving_terminal_name, test_value)
    
    def test_arriving_terminal_abbrev_property(self):
        """
        Test arriving_terminal_abbrev property
        """
        test_value = 'glnjhklmrylnqewgqjjt'
        self.instance.arriving_terminal_abbrev = test_value
        self.assertEqual(self.instance.arriving_terminal_abbrev, test_value)
    
    def test_scheduled_departure_property(self):
        """
        Test scheduled_departure property
        """
        test_value = 'sbtqneunbqnjxxzsvrfv'
        self.instance.scheduled_departure = test_value
        self.assertEqual(self.instance.scheduled_departure, test_value)
    
    def test_left_dock_property(self):
        """
        Test left_dock property
        """
        test_value = 'exgqwmbnaeylaruuimjy'
        self.instance.left_dock = test_value
        self.assertEqual(self.instance.left_dock, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'qchpetmppyckrizrbndh'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_eta_basis_property(self):
        """
        Test eta_basis property
        """
        test_value = 'uhexnpllrwyccetkoiwh'
        self.instance.eta_basis = test_value
        self.assertEqual(self.instance.eta_basis, test_value)
    
    def test_route_abbreviation_property(self):
        """
        Test route_abbreviation property
        """
        test_value = 'yzlfyqefvuwhvclxwurb'
        self.instance.route_abbreviation = test_value
        self.assertEqual(self.instance.route_abbreviation, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'iktokvjrgywttygprevy'
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

