"""
Test case for VesselLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.ferries.vessellocation import VesselLocation


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
            vessel_id='sefxprezyfocfnaangay',
            vessel_name='ptcmubxsssryraxzndbc',
            mmsi=int(24),
            in_service=False,
            at_dock=True,
            latitude=float(86.1015888167683),
            longitude=float(0.7705936530909341),
            speed=float(22.09378570224596),
            heading=int(76),
            departing_terminal_id=int(76),
            departing_terminal_name='gfdikrkdsptviwohpewd',
            departing_terminal_abbrev='zcjsfukeyolnjlyintwp',
            arriving_terminal_id=int(83),
            arriving_terminal_name='qmaozaaudvtrkrqlrvjp',
            arriving_terminal_abbrev='htjlzimferahuawraike',
            scheduled_departure='spbtrbjzttjxcxsrlpda',
            left_dock='vhsixbudecjxlkkdesit',
            eta='dispthepopbcqymktzyh',
            eta_basis='ofjmultrzbdcvrkgycst',
            route_abbreviation='zawjbxscohxqpjsoydov',
            timestamp='eevsnjzobrcvjvfjmqub'
        )
        return instance

    
    def test_vessel_id_property(self):
        """
        Test vessel_id property
        """
        test_value = 'sefxprezyfocfnaangay'
        self.instance.vessel_id = test_value
        self.assertEqual(self.instance.vessel_id, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'ptcmubxsssryraxzndbc'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(24)
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
        test_value = float(86.1015888167683)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(0.7705936530909341)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_speed_property(self):
        """
        Test speed property
        """
        test_value = float(22.09378570224596)
        self.instance.speed = test_value
        self.assertEqual(self.instance.speed, test_value)
    
    def test_heading_property(self):
        """
        Test heading property
        """
        test_value = int(76)
        self.instance.heading = test_value
        self.assertEqual(self.instance.heading, test_value)
    
    def test_departing_terminal_id_property(self):
        """
        Test departing_terminal_id property
        """
        test_value = int(76)
        self.instance.departing_terminal_id = test_value
        self.assertEqual(self.instance.departing_terminal_id, test_value)
    
    def test_departing_terminal_name_property(self):
        """
        Test departing_terminal_name property
        """
        test_value = 'gfdikrkdsptviwohpewd'
        self.instance.departing_terminal_name = test_value
        self.assertEqual(self.instance.departing_terminal_name, test_value)
    
    def test_departing_terminal_abbrev_property(self):
        """
        Test departing_terminal_abbrev property
        """
        test_value = 'zcjsfukeyolnjlyintwp'
        self.instance.departing_terminal_abbrev = test_value
        self.assertEqual(self.instance.departing_terminal_abbrev, test_value)
    
    def test_arriving_terminal_id_property(self):
        """
        Test arriving_terminal_id property
        """
        test_value = int(83)
        self.instance.arriving_terminal_id = test_value
        self.assertEqual(self.instance.arriving_terminal_id, test_value)
    
    def test_arriving_terminal_name_property(self):
        """
        Test arriving_terminal_name property
        """
        test_value = 'qmaozaaudvtrkrqlrvjp'
        self.instance.arriving_terminal_name = test_value
        self.assertEqual(self.instance.arriving_terminal_name, test_value)
    
    def test_arriving_terminal_abbrev_property(self):
        """
        Test arriving_terminal_abbrev property
        """
        test_value = 'htjlzimferahuawraike'
        self.instance.arriving_terminal_abbrev = test_value
        self.assertEqual(self.instance.arriving_terminal_abbrev, test_value)
    
    def test_scheduled_departure_property(self):
        """
        Test scheduled_departure property
        """
        test_value = 'spbtrbjzttjxcxsrlpda'
        self.instance.scheduled_departure = test_value
        self.assertEqual(self.instance.scheduled_departure, test_value)
    
    def test_left_dock_property(self):
        """
        Test left_dock property
        """
        test_value = 'vhsixbudecjxlkkdesit'
        self.instance.left_dock = test_value
        self.assertEqual(self.instance.left_dock, test_value)
    
    def test_eta_property(self):
        """
        Test eta property
        """
        test_value = 'dispthepopbcqymktzyh'
        self.instance.eta = test_value
        self.assertEqual(self.instance.eta, test_value)
    
    def test_eta_basis_property(self):
        """
        Test eta_basis property
        """
        test_value = 'ofjmultrzbdcvrkgycst'
        self.instance.eta_basis = test_value
        self.assertEqual(self.instance.eta_basis, test_value)
    
    def test_route_abbreviation_property(self):
        """
        Test route_abbreviation property
        """
        test_value = 'zawjbxscohxqpjsoydov'
        self.instance.route_abbreviation = test_value
        self.assertEqual(self.instance.route_abbreviation, test_value)
    
    def test_timestamp_property(self):
        """
        Test timestamp property
        """
        test_value = 'eevsnjzobrcvjvfjmqub'
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

