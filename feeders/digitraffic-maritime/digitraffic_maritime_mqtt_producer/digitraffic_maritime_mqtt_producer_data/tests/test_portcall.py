"""
Test case for PortCall
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from digitraffic_maritime_mqtt_producer_data.portcall import PortCall
from digitraffic_maritime_mqtt_producer_data.portcallareadetail import PortCallAreaDetail
from digitraffic_maritime_mqtt_producer_data.portcallagent import PortCallAgent
import datetime


class Test_PortCall(unittest.TestCase):
    """
    Test case for PortCall
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_PortCall.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of PortCall for testing
        """
        instance = PortCall(
            port_call_id=int(24),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            customs_reference='zhbzhradqpdfzklfdywk',
            port_to_visit='pszwrrqdlqdkqlkezvdx',
            previous_port='kpecikqdyaujkjozkqvq',
            next_port='eupjwcvfhxqgojpmvunm',
            mmsi=int(6),
            imo_lloyds=int(75),
            vessel_name='vmqnelutylqhktnehcvz',
            vessel_name_prefix='rkqozovvmfkcbiqmcewn',
            radio_call_sign='hxvkacnyznazdsrsesct',
            nationality='xfstlfmdrfuqkantxhzj',
            vessel_type_code=int(13),
            domestic_traffic_arrival=False,
            domestic_traffic_departure=False,
            arrival_with_cargo=True,
            not_loading=True,
            discharge=int(57),
            current_security_level=int(96),
            agents=[None],
            port_areas=[None, None, None, None]
        )
        return instance

    
    def test_port_call_id_property(self):
        """
        Test port_call_id property
        """
        test_value = int(24)
        self.instance.port_call_id = test_value
        self.assertEqual(self.instance.port_call_id, test_value)
    
    def test_updated_at_property(self):
        """
        Test updated_at property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.updated_at = test_value
        self.assertEqual(self.instance.updated_at, test_value)
    
    def test_customs_reference_property(self):
        """
        Test customs_reference property
        """
        test_value = 'zhbzhradqpdfzklfdywk'
        self.instance.customs_reference = test_value
        self.assertEqual(self.instance.customs_reference, test_value)
    
    def test_port_to_visit_property(self):
        """
        Test port_to_visit property
        """
        test_value = 'pszwrrqdlqdkqlkezvdx'
        self.instance.port_to_visit = test_value
        self.assertEqual(self.instance.port_to_visit, test_value)
    
    def test_previous_port_property(self):
        """
        Test previous_port property
        """
        test_value = 'kpecikqdyaujkjozkqvq'
        self.instance.previous_port = test_value
        self.assertEqual(self.instance.previous_port, test_value)
    
    def test_next_port_property(self):
        """
        Test next_port property
        """
        test_value = 'eupjwcvfhxqgojpmvunm'
        self.instance.next_port = test_value
        self.assertEqual(self.instance.next_port, test_value)
    
    def test_mmsi_property(self):
        """
        Test mmsi property
        """
        test_value = int(6)
        self.instance.mmsi = test_value
        self.assertEqual(self.instance.mmsi, test_value)
    
    def test_imo_lloyds_property(self):
        """
        Test imo_lloyds property
        """
        test_value = int(75)
        self.instance.imo_lloyds = test_value
        self.assertEqual(self.instance.imo_lloyds, test_value)
    
    def test_vessel_name_property(self):
        """
        Test vessel_name property
        """
        test_value = 'vmqnelutylqhktnehcvz'
        self.instance.vessel_name = test_value
        self.assertEqual(self.instance.vessel_name, test_value)
    
    def test_vessel_name_prefix_property(self):
        """
        Test vessel_name_prefix property
        """
        test_value = 'rkqozovvmfkcbiqmcewn'
        self.instance.vessel_name_prefix = test_value
        self.assertEqual(self.instance.vessel_name_prefix, test_value)
    
    def test_radio_call_sign_property(self):
        """
        Test radio_call_sign property
        """
        test_value = 'hxvkacnyznazdsrsesct'
        self.instance.radio_call_sign = test_value
        self.assertEqual(self.instance.radio_call_sign, test_value)
    
    def test_nationality_property(self):
        """
        Test nationality property
        """
        test_value = 'xfstlfmdrfuqkantxhzj'
        self.instance.nationality = test_value
        self.assertEqual(self.instance.nationality, test_value)
    
    def test_vessel_type_code_property(self):
        """
        Test vessel_type_code property
        """
        test_value = int(13)
        self.instance.vessel_type_code = test_value
        self.assertEqual(self.instance.vessel_type_code, test_value)
    
    def test_domestic_traffic_arrival_property(self):
        """
        Test domestic_traffic_arrival property
        """
        test_value = False
        self.instance.domestic_traffic_arrival = test_value
        self.assertEqual(self.instance.domestic_traffic_arrival, test_value)
    
    def test_domestic_traffic_departure_property(self):
        """
        Test domestic_traffic_departure property
        """
        test_value = False
        self.instance.domestic_traffic_departure = test_value
        self.assertEqual(self.instance.domestic_traffic_departure, test_value)
    
    def test_arrival_with_cargo_property(self):
        """
        Test arrival_with_cargo property
        """
        test_value = True
        self.instance.arrival_with_cargo = test_value
        self.assertEqual(self.instance.arrival_with_cargo, test_value)
    
    def test_not_loading_property(self):
        """
        Test not_loading property
        """
        test_value = True
        self.instance.not_loading = test_value
        self.assertEqual(self.instance.not_loading, test_value)
    
    def test_discharge_property(self):
        """
        Test discharge property
        """
        test_value = int(57)
        self.instance.discharge = test_value
        self.assertEqual(self.instance.discharge, test_value)
    
    def test_current_security_level_property(self):
        """
        Test current_security_level property
        """
        test_value = int(96)
        self.instance.current_security_level = test_value
        self.assertEqual(self.instance.current_security_level, test_value)
    
    def test_agents_property(self):
        """
        Test agents property
        """
        test_value = [None]
        self.instance.agents = test_value
        self.assertEqual(self.instance.agents, test_value)
    
    def test_port_areas_property(self):
        """
        Test port_areas property
        """
        test_value = [None, None, None, None]
        self.instance.port_areas = test_value
        self.assertEqual(self.instance.port_areas, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = PortCall.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = PortCall.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

