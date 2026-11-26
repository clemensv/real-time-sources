"""
Test case for MonitoringLocationMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_producer_data.usgs.waterdata.monitoringlocationmetadata import MonitoringLocationMetadata
from usgs_waterdata_producer_data.usgs.waterdata.point import Point
import datetime


class Test_MonitoringLocationMetadata(unittest.TestCase):
    """
    Test case for MonitoringLocationMetadata
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_MonitoringLocationMetadata.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of MonitoringLocationMetadata for testing
        """
        instance = MonitoringLocationMetadata(
            id='qjluqvekbifdzyctbusg',
            agency_code='xslkznacsvepmoxrpzdo',
            agency_name='umnbfrnipwxsavbcoxff',
            monitoring_location_number='ozcakulwkgmvbkdirobc',
            monitoring_location_name='hwupzwhmgpwlpdotjjdm',
            district_code='pqoewahdffztxtbcaqlr',
            country_code='cjvazdymcuqunojvdlwa',
            country_name='squlfkrdjuslzkvzpcdf',
            state_code='fckcasgswpxgjcrdjqmo',
            state_name='pzqsolqqllliwemcwofh',
            county_code='qtenfvopjoumhxcpzdjr',
            county_name='purgpqpfvmltbzmhflwr',
            minor_civil_division_code='tntayovfhrdlbviifuev',
            site_type_code='eldlydtssbkftuknaxvv',
            site_type='posemhggjiqvtplfkbhc',
            hydrologic_unit_code='aqczugjchzutpzmxlzgm',
            basin_code='txoiewrqpdyqpfgbjhed',
            altitude=float(99.28345728864593),
            altitude_accuracy=float(73.00016448372273),
            altitude_method_code='jtlhqazpmjdshqfhueop',
            altitude_method_name='xcqnkxwhcirnieyxgxto',
            vertical_datum='tqjxykgkkbtgplnkhsve',
            vertical_datum_name='zpmubkxzfqxbeyohqamz',
            horizontal_positional_accuracy_code='zlsbaelkmykvnmuwehhq',
            horizontal_positional_accuracy='uouexistykcspzzjkqmm',
            horizontal_position_method_code='rbvyefnbcywlzhbfedow',
            horizontal_position_method_name='ckjdabtdnlioskerhosm',
            original_horizontal_datum='ytqtadmcdwlmgqscmtwx',
            original_horizontal_datum_name='hvqywjahdpitdmodrrme',
            drainage_area=float(67.60406071780116),
            contributing_drainage_area=float(93.63877643831225),
            time_zone_abbreviation='kpvmsahbdtugtmabtnug',
            uses_daylight_savings='epatdeoksgavapulcmpy',
            construction_date='kqcimbpdvatstdwvdmzy',
            aquifer_code='zxmngiugcxwbhdwlohfs',
            national_aquifer_code='psxreddagvkkrkoxhsvl',
            aquifer_type_code='buaqkopvlsmzhkpprkcr',
            well_constructed_depth=float(18.241868304357155),
            hole_constructed_depth=float(55.16267274761732),
            depth_source_code='dirflcvffbpdvyfxxmvp',
            revision_note='bqpxxndnqoxfklfofvtu',
            revision_created=datetime.datetime.now(datetime.timezone.utc),
            revision_modified=datetime.datetime.now(datetime.timezone.utc),
            geometry=None
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'qjluqvekbifdzyctbusg'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_agency_code_property(self):
        """
        Test agency_code property
        """
        test_value = 'xslkznacsvepmoxrpzdo'
        self.instance.agency_code = test_value
        self.assertEqual(self.instance.agency_code, test_value)
    
    def test_agency_name_property(self):
        """
        Test agency_name property
        """
        test_value = 'umnbfrnipwxsavbcoxff'
        self.instance.agency_name = test_value
        self.assertEqual(self.instance.agency_name, test_value)
    
    def test_monitoring_location_number_property(self):
        """
        Test monitoring_location_number property
        """
        test_value = 'ozcakulwkgmvbkdirobc'
        self.instance.monitoring_location_number = test_value
        self.assertEqual(self.instance.monitoring_location_number, test_value)
    
    def test_monitoring_location_name_property(self):
        """
        Test monitoring_location_name property
        """
        test_value = 'hwupzwhmgpwlpdotjjdm'
        self.instance.monitoring_location_name = test_value
        self.assertEqual(self.instance.monitoring_location_name, test_value)
    
    def test_district_code_property(self):
        """
        Test district_code property
        """
        test_value = 'pqoewahdffztxtbcaqlr'
        self.instance.district_code = test_value
        self.assertEqual(self.instance.district_code, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'cjvazdymcuqunojvdlwa'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_country_name_property(self):
        """
        Test country_name property
        """
        test_value = 'squlfkrdjuslzkvzpcdf'
        self.instance.country_name = test_value
        self.assertEqual(self.instance.country_name, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'fckcasgswpxgjcrdjqmo'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_state_name_property(self):
        """
        Test state_name property
        """
        test_value = 'pzqsolqqllliwemcwofh'
        self.instance.state_name = test_value
        self.assertEqual(self.instance.state_name, test_value)
    
    def test_county_code_property(self):
        """
        Test county_code property
        """
        test_value = 'qtenfvopjoumhxcpzdjr'
        self.instance.county_code = test_value
        self.assertEqual(self.instance.county_code, test_value)
    
    def test_county_name_property(self):
        """
        Test county_name property
        """
        test_value = 'purgpqpfvmltbzmhflwr'
        self.instance.county_name = test_value
        self.assertEqual(self.instance.county_name, test_value)
    
    def test_minor_civil_division_code_property(self):
        """
        Test minor_civil_division_code property
        """
        test_value = 'tntayovfhrdlbviifuev'
        self.instance.minor_civil_division_code = test_value
        self.assertEqual(self.instance.minor_civil_division_code, test_value)
    
    def test_site_type_code_property(self):
        """
        Test site_type_code property
        """
        test_value = 'eldlydtssbkftuknaxvv'
        self.instance.site_type_code = test_value
        self.assertEqual(self.instance.site_type_code, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = 'posemhggjiqvtplfkbhc'
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_hydrologic_unit_code_property(self):
        """
        Test hydrologic_unit_code property
        """
        test_value = 'aqczugjchzutpzmxlzgm'
        self.instance.hydrologic_unit_code = test_value
        self.assertEqual(self.instance.hydrologic_unit_code, test_value)
    
    def test_basin_code_property(self):
        """
        Test basin_code property
        """
        test_value = 'txoiewrqpdyqpfgbjhed'
        self.instance.basin_code = test_value
        self.assertEqual(self.instance.basin_code, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(99.28345728864593)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_altitude_accuracy_property(self):
        """
        Test altitude_accuracy property
        """
        test_value = float(73.00016448372273)
        self.instance.altitude_accuracy = test_value
        self.assertEqual(self.instance.altitude_accuracy, test_value)
    
    def test_altitude_method_code_property(self):
        """
        Test altitude_method_code property
        """
        test_value = 'jtlhqazpmjdshqfhueop'
        self.instance.altitude_method_code = test_value
        self.assertEqual(self.instance.altitude_method_code, test_value)
    
    def test_altitude_method_name_property(self):
        """
        Test altitude_method_name property
        """
        test_value = 'xcqnkxwhcirnieyxgxto'
        self.instance.altitude_method_name = test_value
        self.assertEqual(self.instance.altitude_method_name, test_value)
    
    def test_vertical_datum_property(self):
        """
        Test vertical_datum property
        """
        test_value = 'tqjxykgkkbtgplnkhsve'
        self.instance.vertical_datum = test_value
        self.assertEqual(self.instance.vertical_datum, test_value)
    
    def test_vertical_datum_name_property(self):
        """
        Test vertical_datum_name property
        """
        test_value = 'zpmubkxzfqxbeyohqamz'
        self.instance.vertical_datum_name = test_value
        self.assertEqual(self.instance.vertical_datum_name, test_value)
    
    def test_horizontal_positional_accuracy_code_property(self):
        """
        Test horizontal_positional_accuracy_code property
        """
        test_value = 'zlsbaelkmykvnmuwehhq'
        self.instance.horizontal_positional_accuracy_code = test_value
        self.assertEqual(self.instance.horizontal_positional_accuracy_code, test_value)
    
    def test_horizontal_positional_accuracy_property(self):
        """
        Test horizontal_positional_accuracy property
        """
        test_value = 'uouexistykcspzzjkqmm'
        self.instance.horizontal_positional_accuracy = test_value
        self.assertEqual(self.instance.horizontal_positional_accuracy, test_value)
    
    def test_horizontal_position_method_code_property(self):
        """
        Test horizontal_position_method_code property
        """
        test_value = 'rbvyefnbcywlzhbfedow'
        self.instance.horizontal_position_method_code = test_value
        self.assertEqual(self.instance.horizontal_position_method_code, test_value)
    
    def test_horizontal_position_method_name_property(self):
        """
        Test horizontal_position_method_name property
        """
        test_value = 'ckjdabtdnlioskerhosm'
        self.instance.horizontal_position_method_name = test_value
        self.assertEqual(self.instance.horizontal_position_method_name, test_value)
    
    def test_original_horizontal_datum_property(self):
        """
        Test original_horizontal_datum property
        """
        test_value = 'ytqtadmcdwlmgqscmtwx'
        self.instance.original_horizontal_datum = test_value
        self.assertEqual(self.instance.original_horizontal_datum, test_value)
    
    def test_original_horizontal_datum_name_property(self):
        """
        Test original_horizontal_datum_name property
        """
        test_value = 'hvqywjahdpitdmodrrme'
        self.instance.original_horizontal_datum_name = test_value
        self.assertEqual(self.instance.original_horizontal_datum_name, test_value)
    
    def test_drainage_area_property(self):
        """
        Test drainage_area property
        """
        test_value = float(67.60406071780116)
        self.instance.drainage_area = test_value
        self.assertEqual(self.instance.drainage_area, test_value)
    
    def test_contributing_drainage_area_property(self):
        """
        Test contributing_drainage_area property
        """
        test_value = float(93.63877643831225)
        self.instance.contributing_drainage_area = test_value
        self.assertEqual(self.instance.contributing_drainage_area, test_value)
    
    def test_time_zone_abbreviation_property(self):
        """
        Test time_zone_abbreviation property
        """
        test_value = 'kpvmsahbdtugtmabtnug'
        self.instance.time_zone_abbreviation = test_value
        self.assertEqual(self.instance.time_zone_abbreviation, test_value)
    
    def test_uses_daylight_savings_property(self):
        """
        Test uses_daylight_savings property
        """
        test_value = 'epatdeoksgavapulcmpy'
        self.instance.uses_daylight_savings = test_value
        self.assertEqual(self.instance.uses_daylight_savings, test_value)
    
    def test_construction_date_property(self):
        """
        Test construction_date property
        """
        test_value = 'kqcimbpdvatstdwvdmzy'
        self.instance.construction_date = test_value
        self.assertEqual(self.instance.construction_date, test_value)
    
    def test_aquifer_code_property(self):
        """
        Test aquifer_code property
        """
        test_value = 'zxmngiugcxwbhdwlohfs'
        self.instance.aquifer_code = test_value
        self.assertEqual(self.instance.aquifer_code, test_value)
    
    def test_national_aquifer_code_property(self):
        """
        Test national_aquifer_code property
        """
        test_value = 'psxreddagvkkrkoxhsvl'
        self.instance.national_aquifer_code = test_value
        self.assertEqual(self.instance.national_aquifer_code, test_value)
    
    def test_aquifer_type_code_property(self):
        """
        Test aquifer_type_code property
        """
        test_value = 'buaqkopvlsmzhkpprkcr'
        self.instance.aquifer_type_code = test_value
        self.assertEqual(self.instance.aquifer_type_code, test_value)
    
    def test_well_constructed_depth_property(self):
        """
        Test well_constructed_depth property
        """
        test_value = float(18.241868304357155)
        self.instance.well_constructed_depth = test_value
        self.assertEqual(self.instance.well_constructed_depth, test_value)
    
    def test_hole_constructed_depth_property(self):
        """
        Test hole_constructed_depth property
        """
        test_value = float(55.16267274761732)
        self.instance.hole_constructed_depth = test_value
        self.assertEqual(self.instance.hole_constructed_depth, test_value)
    
    def test_depth_source_code_property(self):
        """
        Test depth_source_code property
        """
        test_value = 'dirflcvffbpdvyfxxmvp'
        self.instance.depth_source_code = test_value
        self.assertEqual(self.instance.depth_source_code, test_value)
    
    def test_revision_note_property(self):
        """
        Test revision_note property
        """
        test_value = 'bqpxxndnqoxfklfofvtu'
        self.instance.revision_note = test_value
        self.assertEqual(self.instance.revision_note, test_value)
    
    def test_revision_created_property(self):
        """
        Test revision_created property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.revision_created = test_value
        self.assertEqual(self.instance.revision_created, test_value)
    
    def test_revision_modified_property(self):
        """
        Test revision_modified property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.revision_modified = test_value
        self.assertEqual(self.instance.revision_modified, test_value)
    
    def test_geometry_property(self):
        """
        Test geometry property
        """
        test_value = None
        self.instance.geometry = test_value
        self.assertEqual(self.instance.geometry, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = MonitoringLocationMetadata.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = MonitoringLocationMetadata.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

