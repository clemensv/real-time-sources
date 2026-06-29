"""
Test case for Stop
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_producer_data.fi.hsl.gtfs.stop import Stop


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
            stop_id='ayulgboyjfrhsbwibmcl',
            stop_code='pfbqfbsabqpqobzqfntq',
            stop_name='lsfycmzmqefqlgqejsks',
            stop_desc='pboylfdynebwojdvnsar',
            stop_lat=float(22.73080009355408),
            stop_lon=float(74.72234703784248),
            zone_id='orirmqleljbjvbnsciem',
            stop_url='analmrztkrrnksalbtih',
            location_type=int(51),
            parent_station='ayuohhlxedhokpfwofmp',
            platform_code='qecfuvmloxgidmkuxqpr',
            wheelchair_boarding=int(87),
            vehicle_type=int(95),
            digistop_id='kjyddfzzaydfuytffxez'
        )
        return instance

    
    def test_stop_id_property(self):
        """
        Test stop_id property
        """
        test_value = 'ayulgboyjfrhsbwibmcl'
        self.instance.stop_id = test_value
        self.assertEqual(self.instance.stop_id, test_value)
    
    def test_stop_code_property(self):
        """
        Test stop_code property
        """
        test_value = 'pfbqfbsabqpqobzqfntq'
        self.instance.stop_code = test_value
        self.assertEqual(self.instance.stop_code, test_value)
    
    def test_stop_name_property(self):
        """
        Test stop_name property
        """
        test_value = 'lsfycmzmqefqlgqejsks'
        self.instance.stop_name = test_value
        self.assertEqual(self.instance.stop_name, test_value)
    
    def test_stop_desc_property(self):
        """
        Test stop_desc property
        """
        test_value = 'pboylfdynebwojdvnsar'
        self.instance.stop_desc = test_value
        self.assertEqual(self.instance.stop_desc, test_value)
    
    def test_stop_lat_property(self):
        """
        Test stop_lat property
        """
        test_value = float(22.73080009355408)
        self.instance.stop_lat = test_value
        self.assertEqual(self.instance.stop_lat, test_value)
    
    def test_stop_lon_property(self):
        """
        Test stop_lon property
        """
        test_value = float(74.72234703784248)
        self.instance.stop_lon = test_value
        self.assertEqual(self.instance.stop_lon, test_value)
    
    def test_zone_id_property(self):
        """
        Test zone_id property
        """
        test_value = 'orirmqleljbjvbnsciem'
        self.instance.zone_id = test_value
        self.assertEqual(self.instance.zone_id, test_value)
    
    def test_stop_url_property(self):
        """
        Test stop_url property
        """
        test_value = 'analmrztkrrnksalbtih'
        self.instance.stop_url = test_value
        self.assertEqual(self.instance.stop_url, test_value)
    
    def test_location_type_property(self):
        """
        Test location_type property
        """
        test_value = int(51)
        self.instance.location_type = test_value
        self.assertEqual(self.instance.location_type, test_value)
    
    def test_parent_station_property(self):
        """
        Test parent_station property
        """
        test_value = 'ayuohhlxedhokpfwofmp'
        self.instance.parent_station = test_value
        self.assertEqual(self.instance.parent_station, test_value)
    
    def test_platform_code_property(self):
        """
        Test platform_code property
        """
        test_value = 'qecfuvmloxgidmkuxqpr'
        self.instance.platform_code = test_value
        self.assertEqual(self.instance.platform_code, test_value)
    
    def test_wheelchair_boarding_property(self):
        """
        Test wheelchair_boarding property
        """
        test_value = int(87)
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
        test_value = 'kjyddfzzaydfuytffxez'
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

