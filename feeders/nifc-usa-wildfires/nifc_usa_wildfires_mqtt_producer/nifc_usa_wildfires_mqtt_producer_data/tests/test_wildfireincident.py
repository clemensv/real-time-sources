"""
Test case for WildfireIncident
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from nifc_usa_wildfires_mqtt_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident


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
            irwin_id='qhvfwaotlzpstfrdetog',
            incident_name='snobhyuwoyxxxvqketul',
            unique_fire_identifier='qynuhosbgujqgrnqzilm',
            incident_type_category='ufvtykestibolwklhlmz',
            incident_type_kind='shqftmruyjmoinscwgfd',
            fire_discovery_datetime='osojzrzwodkpqktafnyq',
            daily_acres=float(48.08624834913525),
            calculated_acres=float(91.84629953817667),
            discovery_acres=float(94.95637404719704),
            percent_contained=float(45.18828509235643),
            poo_state='jfukdsspooykftywrpwn',
            poo_county='whazkoailwxlwtswvxll',
            latitude=float(28.17054731604427),
            longitude=float(49.42671526136731),
            fire_cause='lytgwunqnmkzexsmnwrv',
            fire_cause_general='xsrnbknwytazfdsskfkd',
            gacc='hkrkkdcldhtcdcjdvdae',
            total_incident_personnel=int(98),
            incident_management_organization='fhayvgeptljkeaexvxoz',
            fire_mgmt_complexity='nzjxjpzjnipwdfbpykxa',
            residences_destroyed=int(12),
            other_structures_destroyed=int(76),
            injuries=int(5),
            fatalities=int(35),
            containment_datetime='sromocwtbmrwrxruefgb',
            control_datetime='phlcqgpyzezuyntcafra',
            fire_out_datetime='gzikllbrnfrsgehtefgc',
            final_acres=float(73.18708891854659),
            modified_on_datetime='rcgfopdwkqdfnlsbbzsw',
            state='bpawiglimzwxdvqpoktp',
            status='xlxnmbaxqfeogfpkyams'
        )
        return instance

    
    def test_irwin_id_property(self):
        """
        Test irwin_id property
        """
        test_value = 'qhvfwaotlzpstfrdetog'
        self.instance.irwin_id = test_value
        self.assertEqual(self.instance.irwin_id, test_value)
    
    def test_incident_name_property(self):
        """
        Test incident_name property
        """
        test_value = 'snobhyuwoyxxxvqketul'
        self.instance.incident_name = test_value
        self.assertEqual(self.instance.incident_name, test_value)
    
    def test_unique_fire_identifier_property(self):
        """
        Test unique_fire_identifier property
        """
        test_value = 'qynuhosbgujqgrnqzilm'
        self.instance.unique_fire_identifier = test_value
        self.assertEqual(self.instance.unique_fire_identifier, test_value)
    
    def test_incident_type_category_property(self):
        """
        Test incident_type_category property
        """
        test_value = 'ufvtykestibolwklhlmz'
        self.instance.incident_type_category = test_value
        self.assertEqual(self.instance.incident_type_category, test_value)
    
    def test_incident_type_kind_property(self):
        """
        Test incident_type_kind property
        """
        test_value = 'shqftmruyjmoinscwgfd'
        self.instance.incident_type_kind = test_value
        self.assertEqual(self.instance.incident_type_kind, test_value)
    
    def test_fire_discovery_datetime_property(self):
        """
        Test fire_discovery_datetime property
        """
        test_value = 'osojzrzwodkpqktafnyq'
        self.instance.fire_discovery_datetime = test_value
        self.assertEqual(self.instance.fire_discovery_datetime, test_value)
    
    def test_daily_acres_property(self):
        """
        Test daily_acres property
        """
        test_value = float(48.08624834913525)
        self.instance.daily_acres = test_value
        self.assertEqual(self.instance.daily_acres, test_value)
    
    def test_calculated_acres_property(self):
        """
        Test calculated_acres property
        """
        test_value = float(91.84629953817667)
        self.instance.calculated_acres = test_value
        self.assertEqual(self.instance.calculated_acres, test_value)
    
    def test_discovery_acres_property(self):
        """
        Test discovery_acres property
        """
        test_value = float(94.95637404719704)
        self.instance.discovery_acres = test_value
        self.assertEqual(self.instance.discovery_acres, test_value)
    
    def test_percent_contained_property(self):
        """
        Test percent_contained property
        """
        test_value = float(45.18828509235643)
        self.instance.percent_contained = test_value
        self.assertEqual(self.instance.percent_contained, test_value)
    
    def test_poo_state_property(self):
        """
        Test poo_state property
        """
        test_value = 'jfukdsspooykftywrpwn'
        self.instance.poo_state = test_value
        self.assertEqual(self.instance.poo_state, test_value)
    
    def test_poo_county_property(self):
        """
        Test poo_county property
        """
        test_value = 'whazkoailwxlwtswvxll'
        self.instance.poo_county = test_value
        self.assertEqual(self.instance.poo_county, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(28.17054731604427)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(49.42671526136731)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_fire_cause_property(self):
        """
        Test fire_cause property
        """
        test_value = 'lytgwunqnmkzexsmnwrv'
        self.instance.fire_cause = test_value
        self.assertEqual(self.instance.fire_cause, test_value)
    
    def test_fire_cause_general_property(self):
        """
        Test fire_cause_general property
        """
        test_value = 'xsrnbknwytazfdsskfkd'
        self.instance.fire_cause_general = test_value
        self.assertEqual(self.instance.fire_cause_general, test_value)
    
    def test_gacc_property(self):
        """
        Test gacc property
        """
        test_value = 'hkrkkdcldhtcdcjdvdae'
        self.instance.gacc = test_value
        self.assertEqual(self.instance.gacc, test_value)
    
    def test_total_incident_personnel_property(self):
        """
        Test total_incident_personnel property
        """
        test_value = int(98)
        self.instance.total_incident_personnel = test_value
        self.assertEqual(self.instance.total_incident_personnel, test_value)
    
    def test_incident_management_organization_property(self):
        """
        Test incident_management_organization property
        """
        test_value = 'fhayvgeptljkeaexvxoz'
        self.instance.incident_management_organization = test_value
        self.assertEqual(self.instance.incident_management_organization, test_value)
    
    def test_fire_mgmt_complexity_property(self):
        """
        Test fire_mgmt_complexity property
        """
        test_value = 'nzjxjpzjnipwdfbpykxa'
        self.instance.fire_mgmt_complexity = test_value
        self.assertEqual(self.instance.fire_mgmt_complexity, test_value)
    
    def test_residences_destroyed_property(self):
        """
        Test residences_destroyed property
        """
        test_value = int(12)
        self.instance.residences_destroyed = test_value
        self.assertEqual(self.instance.residences_destroyed, test_value)
    
    def test_other_structures_destroyed_property(self):
        """
        Test other_structures_destroyed property
        """
        test_value = int(76)
        self.instance.other_structures_destroyed = test_value
        self.assertEqual(self.instance.other_structures_destroyed, test_value)
    
    def test_injuries_property(self):
        """
        Test injuries property
        """
        test_value = int(5)
        self.instance.injuries = test_value
        self.assertEqual(self.instance.injuries, test_value)
    
    def test_fatalities_property(self):
        """
        Test fatalities property
        """
        test_value = int(35)
        self.instance.fatalities = test_value
        self.assertEqual(self.instance.fatalities, test_value)
    
    def test_containment_datetime_property(self):
        """
        Test containment_datetime property
        """
        test_value = 'sromocwtbmrwrxruefgb'
        self.instance.containment_datetime = test_value
        self.assertEqual(self.instance.containment_datetime, test_value)
    
    def test_control_datetime_property(self):
        """
        Test control_datetime property
        """
        test_value = 'phlcqgpyzezuyntcafra'
        self.instance.control_datetime = test_value
        self.assertEqual(self.instance.control_datetime, test_value)
    
    def test_fire_out_datetime_property(self):
        """
        Test fire_out_datetime property
        """
        test_value = 'gzikllbrnfrsgehtefgc'
        self.instance.fire_out_datetime = test_value
        self.assertEqual(self.instance.fire_out_datetime, test_value)
    
    def test_final_acres_property(self):
        """
        Test final_acres property
        """
        test_value = float(73.18708891854659)
        self.instance.final_acres = test_value
        self.assertEqual(self.instance.final_acres, test_value)
    
    def test_modified_on_datetime_property(self):
        """
        Test modified_on_datetime property
        """
        test_value = 'rcgfopdwkqdfnlsbbzsw'
        self.instance.modified_on_datetime = test_value
        self.assertEqual(self.instance.modified_on_datetime, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'bpawiglimzwxdvqpoktp'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'xlxnmbaxqfeogfpkyams'
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

