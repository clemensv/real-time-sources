"""
Test case for MonitoringLocationMetadata
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_waterdata_amqp_producer_data.usgs.waterdata.monitoringlocationmetadata import MonitoringLocationMetadata
from usgs_waterdata_amqp_producer_data.usgs.waterdata.point import Point
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
            id='pczzypqxdxztebmfbfra',
            agency_code='czrhfnsnsfpkdcsoxgfj',
            agency_name='nlnanjfbwespqbwqhery',
            monitoring_location_number='bmlajdqgyaidbarcymis',
            monitoring_location_name='spntnldgivwivsfwhgnv',
            district_code='jrdkwrnlxdhsbawmalps',
            country_code='mtuwaotgnfcnzfkxeiep',
            country_name='qyrhgqdaebvuotiuqict',
            state_code='kgwpuriwfcscyksoduzq',
            state_name='wljwgmznahgfabgnhdio',
            county_code='omriiphxueypctjlddbr',
            county_name='jutukbcfzwxcrogrtlhq',
            minor_civil_division_code='fmnrzdzdqyehywvjmljt',
            site_type_code='pcnlraybzthjcwrtjlka',
            site_type='rxryxmpoaiecxyvneyms',
            hydrologic_unit_code='xdlbzadtifwmqlovmmls',
            basin_code='fjlqmaopwdgjybpymxqv',
            altitude=float(16.382390532164347),
            altitude_accuracy=float(95.56736827954099),
            altitude_method_code='bezmkydqrnjnwwmbpikd',
            altitude_method_name='zcomwsltafwbqtygjrcv',
            vertical_datum='sifbipmhticridfalgfx',
            vertical_datum_name='ndbsyoxxbomyjjkotulm',
            horizontal_positional_accuracy_code='ztlycfjitcqlzhjfulgw',
            horizontal_positional_accuracy='kyxzdwgfheonzgnqsasd',
            horizontal_position_method_code='zeafalwqtfcfhvuryuyz',
            horizontal_position_method_name='bubijnpqhzmqagtuxims',
            original_horizontal_datum='tnzmsrktxfldytyemnzs',
            original_horizontal_datum_name='axzkeadycvrenhtqelmc',
            drainage_area=float(30.23788897685882),
            contributing_drainage_area=float(2.3514408695612277),
            time_zone_abbreviation='pjxtnlvpgwgdpenyzcxu',
            uses_daylight_savings='ulpdkoidtsrmcwuczmdo',
            construction_date='xpewrkhdsmrvsftcbdgi',
            aquifer_code='hfymbnsxmpujnbklgocr',
            national_aquifer_code='awijwtelwzeytjsknikt',
            aquifer_type_code='xxeruotchtkamolylnlt',
            well_constructed_depth=float(48.47380229431765),
            hole_constructed_depth=float(2.3808367563236232),
            depth_source_code='aotfmaxwhxkketrgdupx',
            revision_note='tzictiuzhnejkmktlcby',
            revision_created=datetime.datetime.now(datetime.timezone.utc),
            revision_modified=datetime.datetime.now(datetime.timezone.utc),
            geometry=None
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'pczzypqxdxztebmfbfra'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_agency_code_property(self):
        """
        Test agency_code property
        """
        test_value = 'czrhfnsnsfpkdcsoxgfj'
        self.instance.agency_code = test_value
        self.assertEqual(self.instance.agency_code, test_value)
    
    def test_agency_name_property(self):
        """
        Test agency_name property
        """
        test_value = 'nlnanjfbwespqbwqhery'
        self.instance.agency_name = test_value
        self.assertEqual(self.instance.agency_name, test_value)
    
    def test_monitoring_location_number_property(self):
        """
        Test monitoring_location_number property
        """
        test_value = 'bmlajdqgyaidbarcymis'
        self.instance.monitoring_location_number = test_value
        self.assertEqual(self.instance.monitoring_location_number, test_value)
    
    def test_monitoring_location_name_property(self):
        """
        Test monitoring_location_name property
        """
        test_value = 'spntnldgivwivsfwhgnv'
        self.instance.monitoring_location_name = test_value
        self.assertEqual(self.instance.monitoring_location_name, test_value)
    
    def test_district_code_property(self):
        """
        Test district_code property
        """
        test_value = 'jrdkwrnlxdhsbawmalps'
        self.instance.district_code = test_value
        self.assertEqual(self.instance.district_code, test_value)
    
    def test_country_code_property(self):
        """
        Test country_code property
        """
        test_value = 'mtuwaotgnfcnzfkxeiep'
        self.instance.country_code = test_value
        self.assertEqual(self.instance.country_code, test_value)
    
    def test_country_name_property(self):
        """
        Test country_name property
        """
        test_value = 'qyrhgqdaebvuotiuqict'
        self.instance.country_name = test_value
        self.assertEqual(self.instance.country_name, test_value)
    
    def test_state_code_property(self):
        """
        Test state_code property
        """
        test_value = 'kgwpuriwfcscyksoduzq'
        self.instance.state_code = test_value
        self.assertEqual(self.instance.state_code, test_value)
    
    def test_state_name_property(self):
        """
        Test state_name property
        """
        test_value = 'wljwgmznahgfabgnhdio'
        self.instance.state_name = test_value
        self.assertEqual(self.instance.state_name, test_value)
    
    def test_county_code_property(self):
        """
        Test county_code property
        """
        test_value = 'omriiphxueypctjlddbr'
        self.instance.county_code = test_value
        self.assertEqual(self.instance.county_code, test_value)
    
    def test_county_name_property(self):
        """
        Test county_name property
        """
        test_value = 'jutukbcfzwxcrogrtlhq'
        self.instance.county_name = test_value
        self.assertEqual(self.instance.county_name, test_value)
    
    def test_minor_civil_division_code_property(self):
        """
        Test minor_civil_division_code property
        """
        test_value = 'fmnrzdzdqyehywvjmljt'
        self.instance.minor_civil_division_code = test_value
        self.assertEqual(self.instance.minor_civil_division_code, test_value)
    
    def test_site_type_code_property(self):
        """
        Test site_type_code property
        """
        test_value = 'pcnlraybzthjcwrtjlka'
        self.instance.site_type_code = test_value
        self.assertEqual(self.instance.site_type_code, test_value)
    
    def test_site_type_property(self):
        """
        Test site_type property
        """
        test_value = 'rxryxmpoaiecxyvneyms'
        self.instance.site_type = test_value
        self.assertEqual(self.instance.site_type, test_value)
    
    def test_hydrologic_unit_code_property(self):
        """
        Test hydrologic_unit_code property
        """
        test_value = 'xdlbzadtifwmqlovmmls'
        self.instance.hydrologic_unit_code = test_value
        self.assertEqual(self.instance.hydrologic_unit_code, test_value)
    
    def test_basin_code_property(self):
        """
        Test basin_code property
        """
        test_value = 'fjlqmaopwdgjybpymxqv'
        self.instance.basin_code = test_value
        self.assertEqual(self.instance.basin_code, test_value)
    
    def test_altitude_property(self):
        """
        Test altitude property
        """
        test_value = float(16.382390532164347)
        self.instance.altitude = test_value
        self.assertEqual(self.instance.altitude, test_value)
    
    def test_altitude_accuracy_property(self):
        """
        Test altitude_accuracy property
        """
        test_value = float(95.56736827954099)
        self.instance.altitude_accuracy = test_value
        self.assertEqual(self.instance.altitude_accuracy, test_value)
    
    def test_altitude_method_code_property(self):
        """
        Test altitude_method_code property
        """
        test_value = 'bezmkydqrnjnwwmbpikd'
        self.instance.altitude_method_code = test_value
        self.assertEqual(self.instance.altitude_method_code, test_value)
    
    def test_altitude_method_name_property(self):
        """
        Test altitude_method_name property
        """
        test_value = 'zcomwsltafwbqtygjrcv'
        self.instance.altitude_method_name = test_value
        self.assertEqual(self.instance.altitude_method_name, test_value)
    
    def test_vertical_datum_property(self):
        """
        Test vertical_datum property
        """
        test_value = 'sifbipmhticridfalgfx'
        self.instance.vertical_datum = test_value
        self.assertEqual(self.instance.vertical_datum, test_value)
    
    def test_vertical_datum_name_property(self):
        """
        Test vertical_datum_name property
        """
        test_value = 'ndbsyoxxbomyjjkotulm'
        self.instance.vertical_datum_name = test_value
        self.assertEqual(self.instance.vertical_datum_name, test_value)
    
    def test_horizontal_positional_accuracy_code_property(self):
        """
        Test horizontal_positional_accuracy_code property
        """
        test_value = 'ztlycfjitcqlzhjfulgw'
        self.instance.horizontal_positional_accuracy_code = test_value
        self.assertEqual(self.instance.horizontal_positional_accuracy_code, test_value)
    
    def test_horizontal_positional_accuracy_property(self):
        """
        Test horizontal_positional_accuracy property
        """
        test_value = 'kyxzdwgfheonzgnqsasd'
        self.instance.horizontal_positional_accuracy = test_value
        self.assertEqual(self.instance.horizontal_positional_accuracy, test_value)
    
    def test_horizontal_position_method_code_property(self):
        """
        Test horizontal_position_method_code property
        """
        test_value = 'zeafalwqtfcfhvuryuyz'
        self.instance.horizontal_position_method_code = test_value
        self.assertEqual(self.instance.horizontal_position_method_code, test_value)
    
    def test_horizontal_position_method_name_property(self):
        """
        Test horizontal_position_method_name property
        """
        test_value = 'bubijnpqhzmqagtuxims'
        self.instance.horizontal_position_method_name = test_value
        self.assertEqual(self.instance.horizontal_position_method_name, test_value)
    
    def test_original_horizontal_datum_property(self):
        """
        Test original_horizontal_datum property
        """
        test_value = 'tnzmsrktxfldytyemnzs'
        self.instance.original_horizontal_datum = test_value
        self.assertEqual(self.instance.original_horizontal_datum, test_value)
    
    def test_original_horizontal_datum_name_property(self):
        """
        Test original_horizontal_datum_name property
        """
        test_value = 'axzkeadycvrenhtqelmc'
        self.instance.original_horizontal_datum_name = test_value
        self.assertEqual(self.instance.original_horizontal_datum_name, test_value)
    
    def test_drainage_area_property(self):
        """
        Test drainage_area property
        """
        test_value = float(30.23788897685882)
        self.instance.drainage_area = test_value
        self.assertEqual(self.instance.drainage_area, test_value)
    
    def test_contributing_drainage_area_property(self):
        """
        Test contributing_drainage_area property
        """
        test_value = float(2.3514408695612277)
        self.instance.contributing_drainage_area = test_value
        self.assertEqual(self.instance.contributing_drainage_area, test_value)
    
    def test_time_zone_abbreviation_property(self):
        """
        Test time_zone_abbreviation property
        """
        test_value = 'pjxtnlvpgwgdpenyzcxu'
        self.instance.time_zone_abbreviation = test_value
        self.assertEqual(self.instance.time_zone_abbreviation, test_value)
    
    def test_uses_daylight_savings_property(self):
        """
        Test uses_daylight_savings property
        """
        test_value = 'ulpdkoidtsrmcwuczmdo'
        self.instance.uses_daylight_savings = test_value
        self.assertEqual(self.instance.uses_daylight_savings, test_value)
    
    def test_construction_date_property(self):
        """
        Test construction_date property
        """
        test_value = 'xpewrkhdsmrvsftcbdgi'
        self.instance.construction_date = test_value
        self.assertEqual(self.instance.construction_date, test_value)
    
    def test_aquifer_code_property(self):
        """
        Test aquifer_code property
        """
        test_value = 'hfymbnsxmpujnbklgocr'
        self.instance.aquifer_code = test_value
        self.assertEqual(self.instance.aquifer_code, test_value)
    
    def test_national_aquifer_code_property(self):
        """
        Test national_aquifer_code property
        """
        test_value = 'awijwtelwzeytjsknikt'
        self.instance.national_aquifer_code = test_value
        self.assertEqual(self.instance.national_aquifer_code, test_value)
    
    def test_aquifer_type_code_property(self):
        """
        Test aquifer_type_code property
        """
        test_value = 'xxeruotchtkamolylnlt'
        self.instance.aquifer_type_code = test_value
        self.assertEqual(self.instance.aquifer_type_code, test_value)
    
    def test_well_constructed_depth_property(self):
        """
        Test well_constructed_depth property
        """
        test_value = float(48.47380229431765)
        self.instance.well_constructed_depth = test_value
        self.assertEqual(self.instance.well_constructed_depth, test_value)
    
    def test_hole_constructed_depth_property(self):
        """
        Test hole_constructed_depth property
        """
        test_value = float(2.3808367563236232)
        self.instance.hole_constructed_depth = test_value
        self.assertEqual(self.instance.hole_constructed_depth, test_value)
    
    def test_depth_source_code_property(self):
        """
        Test depth_source_code property
        """
        test_value = 'aotfmaxwhxkketrgdupx'
        self.instance.depth_source_code = test_value
        self.assertEqual(self.instance.depth_source_code, test_value)
    
    def test_revision_note_property(self):
        """
        Test revision_note property
        """
        test_value = 'tzictiuzhnejkmktlcby'
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

