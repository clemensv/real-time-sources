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
            irwin_id='cdgwtvyqnbxnctcllfsq',
            incident_name='ftzfrhgxyexoioclbxcb',
            unique_fire_identifier='fhqbaskzkkyeckvsukfu',
            incident_type_category='ftfsoqrxetpfpjsnrjac',
            incident_type_kind='jzhanwceaekqkgentrsx',
            fire_discovery_datetime='ejgjtkntqhrqerrbifjs',
            daily_acres=float(11.044408034312092),
            calculated_acres=float(4.299166457928417),
            discovery_acres=float(97.92116340246014),
            percent_contained=float(64.72525016792608),
            poo_state='ynvinngsvxbgxlvsjyil',
            poo_county='rivaxnjhhmqwfyvkcjaj',
            latitude=float(17.782795417755835),
            longitude=float(37.062978355597274),
            fire_cause='sqjwchcbeumhfxyxvqdm',
            fire_cause_general='znfsygbwhtsemyquekjs',
            gacc='zdlvkaxskuxegltbjpmq',
            total_incident_personnel=int(38),
            incident_management_organization='oqtfnjbqzwebifijetie',
            fire_mgmt_complexity='hrliiohqbjjjncmxmqly',
            residences_destroyed=int(8),
            other_structures_destroyed=int(69),
            injuries=int(17),
            fatalities=int(11),
            containment_datetime='uwkirawglrxtiauodchi',
            control_datetime='fiotfdicnhnmcdebketg',
            fire_out_datetime='mdabbnzvshhdwcajavor',
            final_acres=float(36.35097033660944),
            modified_on_datetime='oetgocdddhwylzhkxcgb',
            state='dkfgrhlkbfszkapvdxlh',
            status='qowgjfsuibftcntkyoxf'
        )
        return instance

    
    def test_irwin_id_property(self):
        """
        Test irwin_id property
        """
        test_value = 'cdgwtvyqnbxnctcllfsq'
        self.instance.irwin_id = test_value
        self.assertEqual(self.instance.irwin_id, test_value)
    
    def test_incident_name_property(self):
        """
        Test incident_name property
        """
        test_value = 'ftzfrhgxyexoioclbxcb'
        self.instance.incident_name = test_value
        self.assertEqual(self.instance.incident_name, test_value)
    
    def test_unique_fire_identifier_property(self):
        """
        Test unique_fire_identifier property
        """
        test_value = 'fhqbaskzkkyeckvsukfu'
        self.instance.unique_fire_identifier = test_value
        self.assertEqual(self.instance.unique_fire_identifier, test_value)
    
    def test_incident_type_category_property(self):
        """
        Test incident_type_category property
        """
        test_value = 'ftfsoqrxetpfpjsnrjac'
        self.instance.incident_type_category = test_value
        self.assertEqual(self.instance.incident_type_category, test_value)
    
    def test_incident_type_kind_property(self):
        """
        Test incident_type_kind property
        """
        test_value = 'jzhanwceaekqkgentrsx'
        self.instance.incident_type_kind = test_value
        self.assertEqual(self.instance.incident_type_kind, test_value)
    
    def test_fire_discovery_datetime_property(self):
        """
        Test fire_discovery_datetime property
        """
        test_value = 'ejgjtkntqhrqerrbifjs'
        self.instance.fire_discovery_datetime = test_value
        self.assertEqual(self.instance.fire_discovery_datetime, test_value)
    
    def test_daily_acres_property(self):
        """
        Test daily_acres property
        """
        test_value = float(11.044408034312092)
        self.instance.daily_acres = test_value
        self.assertEqual(self.instance.daily_acres, test_value)
    
    def test_calculated_acres_property(self):
        """
        Test calculated_acres property
        """
        test_value = float(4.299166457928417)
        self.instance.calculated_acres = test_value
        self.assertEqual(self.instance.calculated_acres, test_value)
    
    def test_discovery_acres_property(self):
        """
        Test discovery_acres property
        """
        test_value = float(97.92116340246014)
        self.instance.discovery_acres = test_value
        self.assertEqual(self.instance.discovery_acres, test_value)
    
    def test_percent_contained_property(self):
        """
        Test percent_contained property
        """
        test_value = float(64.72525016792608)
        self.instance.percent_contained = test_value
        self.assertEqual(self.instance.percent_contained, test_value)
    
    def test_poo_state_property(self):
        """
        Test poo_state property
        """
        test_value = 'ynvinngsvxbgxlvsjyil'
        self.instance.poo_state = test_value
        self.assertEqual(self.instance.poo_state, test_value)
    
    def test_poo_county_property(self):
        """
        Test poo_county property
        """
        test_value = 'rivaxnjhhmqwfyvkcjaj'
        self.instance.poo_county = test_value
        self.assertEqual(self.instance.poo_county, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(17.782795417755835)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(37.062978355597274)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_fire_cause_property(self):
        """
        Test fire_cause property
        """
        test_value = 'sqjwchcbeumhfxyxvqdm'
        self.instance.fire_cause = test_value
        self.assertEqual(self.instance.fire_cause, test_value)
    
    def test_fire_cause_general_property(self):
        """
        Test fire_cause_general property
        """
        test_value = 'znfsygbwhtsemyquekjs'
        self.instance.fire_cause_general = test_value
        self.assertEqual(self.instance.fire_cause_general, test_value)
    
    def test_gacc_property(self):
        """
        Test gacc property
        """
        test_value = 'zdlvkaxskuxegltbjpmq'
        self.instance.gacc = test_value
        self.assertEqual(self.instance.gacc, test_value)
    
    def test_total_incident_personnel_property(self):
        """
        Test total_incident_personnel property
        """
        test_value = int(38)
        self.instance.total_incident_personnel = test_value
        self.assertEqual(self.instance.total_incident_personnel, test_value)
    
    def test_incident_management_organization_property(self):
        """
        Test incident_management_organization property
        """
        test_value = 'oqtfnjbqzwebifijetie'
        self.instance.incident_management_organization = test_value
        self.assertEqual(self.instance.incident_management_organization, test_value)
    
    def test_fire_mgmt_complexity_property(self):
        """
        Test fire_mgmt_complexity property
        """
        test_value = 'hrliiohqbjjjncmxmqly'
        self.instance.fire_mgmt_complexity = test_value
        self.assertEqual(self.instance.fire_mgmt_complexity, test_value)
    
    def test_residences_destroyed_property(self):
        """
        Test residences_destroyed property
        """
        test_value = int(8)
        self.instance.residences_destroyed = test_value
        self.assertEqual(self.instance.residences_destroyed, test_value)
    
    def test_other_structures_destroyed_property(self):
        """
        Test other_structures_destroyed property
        """
        test_value = int(69)
        self.instance.other_structures_destroyed = test_value
        self.assertEqual(self.instance.other_structures_destroyed, test_value)
    
    def test_injuries_property(self):
        """
        Test injuries property
        """
        test_value = int(17)
        self.instance.injuries = test_value
        self.assertEqual(self.instance.injuries, test_value)
    
    def test_fatalities_property(self):
        """
        Test fatalities property
        """
        test_value = int(11)
        self.instance.fatalities = test_value
        self.assertEqual(self.instance.fatalities, test_value)
    
    def test_containment_datetime_property(self):
        """
        Test containment_datetime property
        """
        test_value = 'uwkirawglrxtiauodchi'
        self.instance.containment_datetime = test_value
        self.assertEqual(self.instance.containment_datetime, test_value)
    
    def test_control_datetime_property(self):
        """
        Test control_datetime property
        """
        test_value = 'fiotfdicnhnmcdebketg'
        self.instance.control_datetime = test_value
        self.assertEqual(self.instance.control_datetime, test_value)
    
    def test_fire_out_datetime_property(self):
        """
        Test fire_out_datetime property
        """
        test_value = 'mdabbnzvshhdwcajavor'
        self.instance.fire_out_datetime = test_value
        self.assertEqual(self.instance.fire_out_datetime, test_value)
    
    def test_final_acres_property(self):
        """
        Test final_acres property
        """
        test_value = float(36.35097033660944)
        self.instance.final_acres = test_value
        self.assertEqual(self.instance.final_acres, test_value)
    
    def test_modified_on_datetime_property(self):
        """
        Test modified_on_datetime property
        """
        test_value = 'oetgocdddhwylzhkxcgb'
        self.instance.modified_on_datetime = test_value
        self.assertEqual(self.instance.modified_on_datetime, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'dkfgrhlkbfszkapvdxlh'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'qowgjfsuibftcntkyoxf'
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

