"""
Test case for BridgeClearance
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from wsdot_mqtt_producer_data.us.wa.wsdot.bridgeclearances.bridgeclearance import BridgeClearance


class Test_BridgeClearance(unittest.TestCase):
    """
    Test case for BridgeClearance
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_BridgeClearance.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of BridgeClearance for testing
        """
        instance = BridgeClearance(
            crossing_location_id='vubsydqwhpfjwhbhwwqg',
            bridge_number='aadvnydsqagcynxvkigg',
            state_route_id='bpbrcvmzdwmcolrgcesz',
            state_structure_id='zneovxxhctohnomxtyct',
            crossing_description='kfhoseakwqrmwewcwlgv',
            inventory_direction='ozlwmudsvgybgggtoxlf',
            srmp=float(28.18387537738204),
            srmp_ahead_back_indicator='nbdcwtmlvlihmmpmcxfn',
            latitude=float(94.8390155492651),
            longitude=float(94.70785295293817),
            vertical_clearance_maximum_inches=int(37),
            vertical_clearance_maximum_feet_inch='ywstuafapfrpduxdbzsg',
            vertical_clearance_minimum_inches=int(68),
            vertical_clearance_minimum_feet_inch='gkopfoacabascggysnnu',
            control_entity_guid='jfdhydnhfpnjbeeyhapk',
            crossing_record_guid='aipjeiyerkucngwlnuov',
            location_guid='fjgmwsizfyhscdqduznb',
            route_date='mojmcsaxjwavjuzhqxgq',
            api_last_update='scjndlfkgycjyfkyvfvf'
        )
        return instance

    
    def test_crossing_location_id_property(self):
        """
        Test crossing_location_id property
        """
        test_value = 'vubsydqwhpfjwhbhwwqg'
        self.instance.crossing_location_id = test_value
        self.assertEqual(self.instance.crossing_location_id, test_value)
    
    def test_bridge_number_property(self):
        """
        Test bridge_number property
        """
        test_value = 'aadvnydsqagcynxvkigg'
        self.instance.bridge_number = test_value
        self.assertEqual(self.instance.bridge_number, test_value)
    
    def test_state_route_id_property(self):
        """
        Test state_route_id property
        """
        test_value = 'bpbrcvmzdwmcolrgcesz'
        self.instance.state_route_id = test_value
        self.assertEqual(self.instance.state_route_id, test_value)
    
    def test_state_structure_id_property(self):
        """
        Test state_structure_id property
        """
        test_value = 'zneovxxhctohnomxtyct'
        self.instance.state_structure_id = test_value
        self.assertEqual(self.instance.state_structure_id, test_value)
    
    def test_crossing_description_property(self):
        """
        Test crossing_description property
        """
        test_value = 'kfhoseakwqrmwewcwlgv'
        self.instance.crossing_description = test_value
        self.assertEqual(self.instance.crossing_description, test_value)
    
    def test_inventory_direction_property(self):
        """
        Test inventory_direction property
        """
        test_value = 'ozlwmudsvgybgggtoxlf'
        self.instance.inventory_direction = test_value
        self.assertEqual(self.instance.inventory_direction, test_value)
    
    def test_srmp_property(self):
        """
        Test srmp property
        """
        test_value = float(28.18387537738204)
        self.instance.srmp = test_value
        self.assertEqual(self.instance.srmp, test_value)
    
    def test_srmp_ahead_back_indicator_property(self):
        """
        Test srmp_ahead_back_indicator property
        """
        test_value = 'nbdcwtmlvlihmmpmcxfn'
        self.instance.srmp_ahead_back_indicator = test_value
        self.assertEqual(self.instance.srmp_ahead_back_indicator, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(94.8390155492651)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(94.70785295293817)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_vertical_clearance_maximum_inches_property(self):
        """
        Test vertical_clearance_maximum_inches property
        """
        test_value = int(37)
        self.instance.vertical_clearance_maximum_inches = test_value
        self.assertEqual(self.instance.vertical_clearance_maximum_inches, test_value)
    
    def test_vertical_clearance_maximum_feet_inch_property(self):
        """
        Test vertical_clearance_maximum_feet_inch property
        """
        test_value = 'ywstuafapfrpduxdbzsg'
        self.instance.vertical_clearance_maximum_feet_inch = test_value
        self.assertEqual(self.instance.vertical_clearance_maximum_feet_inch, test_value)
    
    def test_vertical_clearance_minimum_inches_property(self):
        """
        Test vertical_clearance_minimum_inches property
        """
        test_value = int(68)
        self.instance.vertical_clearance_minimum_inches = test_value
        self.assertEqual(self.instance.vertical_clearance_minimum_inches, test_value)
    
    def test_vertical_clearance_minimum_feet_inch_property(self):
        """
        Test vertical_clearance_minimum_feet_inch property
        """
        test_value = 'gkopfoacabascggysnnu'
        self.instance.vertical_clearance_minimum_feet_inch = test_value
        self.assertEqual(self.instance.vertical_clearance_minimum_feet_inch, test_value)
    
    def test_control_entity_guid_property(self):
        """
        Test control_entity_guid property
        """
        test_value = 'jfdhydnhfpnjbeeyhapk'
        self.instance.control_entity_guid = test_value
        self.assertEqual(self.instance.control_entity_guid, test_value)
    
    def test_crossing_record_guid_property(self):
        """
        Test crossing_record_guid property
        """
        test_value = 'aipjeiyerkucngwlnuov'
        self.instance.crossing_record_guid = test_value
        self.assertEqual(self.instance.crossing_record_guid, test_value)
    
    def test_location_guid_property(self):
        """
        Test location_guid property
        """
        test_value = 'fjgmwsizfyhscdqduznb'
        self.instance.location_guid = test_value
        self.assertEqual(self.instance.location_guid, test_value)
    
    def test_route_date_property(self):
        """
        Test route_date property
        """
        test_value = 'mojmcsaxjwavjuzhqxgq'
        self.instance.route_date = test_value
        self.assertEqual(self.instance.route_date, test_value)
    
    def test_api_last_update_property(self):
        """
        Test api_last_update property
        """
        test_value = 'scjndlfkgycjyfkyvfvf'
        self.instance.api_last_update = test_value
        self.assertEqual(self.instance.api_last_update, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = BridgeClearance.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = BridgeClearance.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

