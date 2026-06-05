"""
Test case for WildfireIncident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident


class Test_WildfireIncident(unittest.TestCase):
    """
    Test case for WildfireIncident
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_WildfireIncident.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of WildfireIncident for testing
        """
        instance = WildfireIncident(
            irwin_id='qnzhqolhudvrdgbgudbp',
            incident_name='fbljmbwksapozeprbpwh',
            unique_fire_identifier='buhmyvwhxmsucwmnaftk',
            incident_type_category='dpmllvegaaojeuuwxura',
            incident_type_kind='pvqhxeuhmshfoatnmtug',
            fire_discovery_datetime='xayujwwzzijbfzjierkv',
            daily_acres=float(25.34000904089738),
            calculated_acres=float(18.72681785714302),
            discovery_acres=float(3.2262743868085586),
            percent_contained=float(83.46708789509059),
            poo_state='qbrjsarsvlmkxmrqbfuk',
            poo_county='txiuvknomurljetiuvhb',
            latitude=float(50.120260992494906),
            longitude=float(49.71706876225327),
            fire_cause='kfapruvsdnfqvpgksmgn',
            fire_cause_general='efgeeczaeccsctwerfnd',
            gacc='qomiulantputwsfowzzo',
            total_incident_personnel=int(33),
            incident_management_organization='awhvkdiykcwuuvzybpew',
            fire_mgmt_complexity='yiposkhvywcyhglhnqij',
            residences_destroyed=int(37),
            other_structures_destroyed=int(44),
            injuries=int(64),
            fatalities=int(100),
            containment_datetime='mrhmnioiedjwldiklsof',
            control_datetime='sgohkdynwgglmvmxolgu',
            fire_out_datetime='aaklsyicddbwywkydvzm',
            final_acres=float(87.07986342790113),
            modified_on_datetime='wcrelylikqlcfdmczuza',
            state='snggxrsujmdbxopkhdty',
            status='bczthvdqdetezflyzkef'
        )
        return instance

    
    def test_irwin_id_property(self):
        """
        Test irwin_id property
        """
        test_value = 'qnzhqolhudvrdgbgudbp'
        self.instance.irwin_id = test_value
        self.assertEqual(self.instance.irwin_id, test_value)
    
    def test_incident_name_property(self):
        """
        Test incident_name property
        """
        test_value = 'fbljmbwksapozeprbpwh'
        self.instance.incident_name = test_value
        self.assertEqual(self.instance.incident_name, test_value)
    
    def test_unique_fire_identifier_property(self):
        """
        Test unique_fire_identifier property
        """
        test_value = 'buhmyvwhxmsucwmnaftk'
        self.instance.unique_fire_identifier = test_value
        self.assertEqual(self.instance.unique_fire_identifier, test_value)
    
    def test_incident_type_category_property(self):
        """
        Test incident_type_category property
        """
        test_value = 'dpmllvegaaojeuuwxura'
        self.instance.incident_type_category = test_value
        self.assertEqual(self.instance.incident_type_category, test_value)
    
    def test_incident_type_kind_property(self):
        """
        Test incident_type_kind property
        """
        test_value = 'pvqhxeuhmshfoatnmtug'
        self.instance.incident_type_kind = test_value
        self.assertEqual(self.instance.incident_type_kind, test_value)
    
    def test_fire_discovery_datetime_property(self):
        """
        Test fire_discovery_datetime property
        """
        test_value = 'xayujwwzzijbfzjierkv'
        self.instance.fire_discovery_datetime = test_value
        self.assertEqual(self.instance.fire_discovery_datetime, test_value)
    
    def test_daily_acres_property(self):
        """
        Test daily_acres property
        """
        test_value = float(25.34000904089738)
        self.instance.daily_acres = test_value
        self.assertEqual(self.instance.daily_acres, test_value)
    
    def test_calculated_acres_property(self):
        """
        Test calculated_acres property
        """
        test_value = float(18.72681785714302)
        self.instance.calculated_acres = test_value
        self.assertEqual(self.instance.calculated_acres, test_value)
    
    def test_discovery_acres_property(self):
        """
        Test discovery_acres property
        """
        test_value = float(3.2262743868085586)
        self.instance.discovery_acres = test_value
        self.assertEqual(self.instance.discovery_acres, test_value)
    
    def test_percent_contained_property(self):
        """
        Test percent_contained property
        """
        test_value = float(83.46708789509059)
        self.instance.percent_contained = test_value
        self.assertEqual(self.instance.percent_contained, test_value)
    
    def test_poo_state_property(self):
        """
        Test poo_state property
        """
        test_value = 'qbrjsarsvlmkxmrqbfuk'
        self.instance.poo_state = test_value
        self.assertEqual(self.instance.poo_state, test_value)
    
    def test_poo_county_property(self):
        """
        Test poo_county property
        """
        test_value = 'txiuvknomurljetiuvhb'
        self.instance.poo_county = test_value
        self.assertEqual(self.instance.poo_county, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(50.120260992494906)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(49.71706876225327)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_fire_cause_property(self):
        """
        Test fire_cause property
        """
        test_value = 'kfapruvsdnfqvpgksmgn'
        self.instance.fire_cause = test_value
        self.assertEqual(self.instance.fire_cause, test_value)
    
    def test_fire_cause_general_property(self):
        """
        Test fire_cause_general property
        """
        test_value = 'efgeeczaeccsctwerfnd'
        self.instance.fire_cause_general = test_value
        self.assertEqual(self.instance.fire_cause_general, test_value)
    
    def test_gacc_property(self):
        """
        Test gacc property
        """
        test_value = 'qomiulantputwsfowzzo'
        self.instance.gacc = test_value
        self.assertEqual(self.instance.gacc, test_value)
    
    def test_total_incident_personnel_property(self):
        """
        Test total_incident_personnel property
        """
        test_value = int(33)
        self.instance.total_incident_personnel = test_value
        self.assertEqual(self.instance.total_incident_personnel, test_value)
    
    def test_incident_management_organization_property(self):
        """
        Test incident_management_organization property
        """
        test_value = 'awhvkdiykcwuuvzybpew'
        self.instance.incident_management_organization = test_value
        self.assertEqual(self.instance.incident_management_organization, test_value)
    
    def test_fire_mgmt_complexity_property(self):
        """
        Test fire_mgmt_complexity property
        """
        test_value = 'yiposkhvywcyhglhnqij'
        self.instance.fire_mgmt_complexity = test_value
        self.assertEqual(self.instance.fire_mgmt_complexity, test_value)
    
    def test_residences_destroyed_property(self):
        """
        Test residences_destroyed property
        """
        test_value = int(37)
        self.instance.residences_destroyed = test_value
        self.assertEqual(self.instance.residences_destroyed, test_value)
    
    def test_other_structures_destroyed_property(self):
        """
        Test other_structures_destroyed property
        """
        test_value = int(44)
        self.instance.other_structures_destroyed = test_value
        self.assertEqual(self.instance.other_structures_destroyed, test_value)
    
    def test_injuries_property(self):
        """
        Test injuries property
        """
        test_value = int(64)
        self.instance.injuries = test_value
        self.assertEqual(self.instance.injuries, test_value)
    
    def test_fatalities_property(self):
        """
        Test fatalities property
        """
        test_value = int(100)
        self.instance.fatalities = test_value
        self.assertEqual(self.instance.fatalities, test_value)
    
    def test_containment_datetime_property(self):
        """
        Test containment_datetime property
        """
        test_value = 'mrhmnioiedjwldiklsof'
        self.instance.containment_datetime = test_value
        self.assertEqual(self.instance.containment_datetime, test_value)
    
    def test_control_datetime_property(self):
        """
        Test control_datetime property
        """
        test_value = 'sgohkdynwgglmvmxolgu'
        self.instance.control_datetime = test_value
        self.assertEqual(self.instance.control_datetime, test_value)
    
    def test_fire_out_datetime_property(self):
        """
        Test fire_out_datetime property
        """
        test_value = 'aaklsyicddbwywkydvzm'
        self.instance.fire_out_datetime = test_value
        self.assertEqual(self.instance.fire_out_datetime, test_value)
    
    def test_final_acres_property(self):
        """
        Test final_acres property
        """
        test_value = float(87.07986342790113)
        self.instance.final_acres = test_value
        self.assertEqual(self.instance.final_acres, test_value)
    
    def test_modified_on_datetime_property(self):
        """
        Test modified_on_datetime property
        """
        test_value = 'wcrelylikqlcfdmczuza'
        self.instance.modified_on_datetime = test_value
        self.assertEqual(self.instance.modified_on_datetime, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'snggxrsujmdbxopkhdty'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'bczthvdqdetezflyzkef'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = WildfireIncident.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = WildfireIncident.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

