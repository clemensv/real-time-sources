"""
Test case for ChargingLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_amqp_producer_data.io.openchargemap.charginglocation import ChargingLocation
from open_charge_map_amqp_producer_data.io.openchargemap.connection import Connection
import datetime


class Test_ChargingLocation(unittest.TestCase):
    """
    Test case for ChargingLocation
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_ChargingLocation.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of ChargingLocation for testing
        """
        instance = ChargingLocation(
            poi_id=int(46),
            uuid='uilgpxxgtudiygsdbxfl',
            data_provider_id=int(49),
            operator_id=int(35),
            operator_title='wccgxlbmirautmwgcjnj',
            usage_type_id=int(99),
            usage_type_title='ttojeyqzattabhhlhphg',
            usage_cost='fiwsasjgwrfdutuyqfcu',
            status_type_id=int(20),
            status_title='dzrtakmnesczvswywqpi',
            is_operational=True,
            submission_status_type_id=int(91),
            submission_status_title='iaeiomlyxsoqlnsoqwug',
            data_quality_level=int(0),
            number_of_points=int(14),
            general_comments='wdnsiljuixwlbhnkdoxv',
            is_recently_verified=False,
            date_created=datetime.datetime.now(datetime.timezone.utc),
            date_last_status_update=datetime.datetime.now(datetime.timezone.utc),
            date_last_verified=datetime.datetime.now(datetime.timezone.utc),
            date_last_confirmed=datetime.datetime.now(datetime.timezone.utc),
            date_planned=datetime.datetime.now(datetime.timezone.utc),
            address_id=int(23),
            address_title='nuenarygqvrtxnmzeixm',
            address_line1='skrjhrngangaclabgsfb',
            address_line2='kmgaauurimrtxconzvmg',
            town='vphwnkjokzuwngkdhmwq',
            state_or_province='cewqhvomepdwxfegomjh',
            postcode='hzjazxvnjveajaqwsbge',
            country_id=int(65),
            country_iso_code='rawqafuligkgsfcrshvo',
            country_title='dinjtcijbqpyxyqhgyrx',
            latitude=float(78.37976030072039),
            longitude=float(51.75439827643669),
            contact_telephone1='wgftwnqymolhxwvtebkp',
            contact_telephone2='noivelzpffngeuycvqgq',
            contact_email='kjvzdzmnincawjvxzork',
            access_comments='wixencziigxsakcwemle',
            related_url='ugpvjxttlsubfupjypwi',
            connections=[None, None, None, None, None]
        )
        return instance

    
    def test_poi_id_property(self):
        """
        Test poi_id property
        """
        test_value = int(46)
        self.instance.poi_id = test_value
        self.assertEqual(self.instance.poi_id, test_value)
    
    def test_uuid_property(self):
        """
        Test uuid property
        """
        test_value = 'uilgpxxgtudiygsdbxfl'
        self.instance.uuid = test_value
        self.assertEqual(self.instance.uuid, test_value)
    
    def test_data_provider_id_property(self):
        """
        Test data_provider_id property
        """
        test_value = int(49)
        self.instance.data_provider_id = test_value
        self.assertEqual(self.instance.data_provider_id, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = int(35)
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_operator_title_property(self):
        """
        Test operator_title property
        """
        test_value = 'wccgxlbmirautmwgcjnj'
        self.instance.operator_title = test_value
        self.assertEqual(self.instance.operator_title, test_value)
    
    def test_usage_type_id_property(self):
        """
        Test usage_type_id property
        """
        test_value = int(99)
        self.instance.usage_type_id = test_value
        self.assertEqual(self.instance.usage_type_id, test_value)
    
    def test_usage_type_title_property(self):
        """
        Test usage_type_title property
        """
        test_value = 'ttojeyqzattabhhlhphg'
        self.instance.usage_type_title = test_value
        self.assertEqual(self.instance.usage_type_title, test_value)
    
    def test_usage_cost_property(self):
        """
        Test usage_cost property
        """
        test_value = 'fiwsasjgwrfdutuyqfcu'
        self.instance.usage_cost = test_value
        self.assertEqual(self.instance.usage_cost, test_value)
    
    def test_status_type_id_property(self):
        """
        Test status_type_id property
        """
        test_value = int(20)
        self.instance.status_type_id = test_value
        self.assertEqual(self.instance.status_type_id, test_value)
    
    def test_status_title_property(self):
        """
        Test status_title property
        """
        test_value = 'dzrtakmnesczvswywqpi'
        self.instance.status_title = test_value
        self.assertEqual(self.instance.status_title, test_value)
    
    def test_is_operational_property(self):
        """
        Test is_operational property
        """
        test_value = True
        self.instance.is_operational = test_value
        self.assertEqual(self.instance.is_operational, test_value)
    
    def test_submission_status_type_id_property(self):
        """
        Test submission_status_type_id property
        """
        test_value = int(91)
        self.instance.submission_status_type_id = test_value
        self.assertEqual(self.instance.submission_status_type_id, test_value)
    
    def test_submission_status_title_property(self):
        """
        Test submission_status_title property
        """
        test_value = 'iaeiomlyxsoqlnsoqwug'
        self.instance.submission_status_title = test_value
        self.assertEqual(self.instance.submission_status_title, test_value)
    
    def test_data_quality_level_property(self):
        """
        Test data_quality_level property
        """
        test_value = int(0)
        self.instance.data_quality_level = test_value
        self.assertEqual(self.instance.data_quality_level, test_value)
    
    def test_number_of_points_property(self):
        """
        Test number_of_points property
        """
        test_value = int(14)
        self.instance.number_of_points = test_value
        self.assertEqual(self.instance.number_of_points, test_value)
    
    def test_general_comments_property(self):
        """
        Test general_comments property
        """
        test_value = 'wdnsiljuixwlbhnkdoxv'
        self.instance.general_comments = test_value
        self.assertEqual(self.instance.general_comments, test_value)
    
    def test_is_recently_verified_property(self):
        """
        Test is_recently_verified property
        """
        test_value = False
        self.instance.is_recently_verified = test_value
        self.assertEqual(self.instance.is_recently_verified, test_value)
    
    def test_date_created_property(self):
        """
        Test date_created property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_created = test_value
        self.assertEqual(self.instance.date_created, test_value)
    
    def test_date_last_status_update_property(self):
        """
        Test date_last_status_update property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_last_status_update = test_value
        self.assertEqual(self.instance.date_last_status_update, test_value)
    
    def test_date_last_verified_property(self):
        """
        Test date_last_verified property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_last_verified = test_value
        self.assertEqual(self.instance.date_last_verified, test_value)
    
    def test_date_last_confirmed_property(self):
        """
        Test date_last_confirmed property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_last_confirmed = test_value
        self.assertEqual(self.instance.date_last_confirmed, test_value)
    
    def test_date_planned_property(self):
        """
        Test date_planned property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.date_planned = test_value
        self.assertEqual(self.instance.date_planned, test_value)
    
    def test_address_id_property(self):
        """
        Test address_id property
        """
        test_value = int(23)
        self.instance.address_id = test_value
        self.assertEqual(self.instance.address_id, test_value)
    
    def test_address_title_property(self):
        """
        Test address_title property
        """
        test_value = 'nuenarygqvrtxnmzeixm'
        self.instance.address_title = test_value
        self.assertEqual(self.instance.address_title, test_value)
    
    def test_address_line1_property(self):
        """
        Test address_line1 property
        """
        test_value = 'skrjhrngangaclabgsfb'
        self.instance.address_line1 = test_value
        self.assertEqual(self.instance.address_line1, test_value)
    
    def test_address_line2_property(self):
        """
        Test address_line2 property
        """
        test_value = 'kmgaauurimrtxconzvmg'
        self.instance.address_line2 = test_value
        self.assertEqual(self.instance.address_line2, test_value)
    
    def test_town_property(self):
        """
        Test town property
        """
        test_value = 'vphwnkjokzuwngkdhmwq'
        self.instance.town = test_value
        self.assertEqual(self.instance.town, test_value)
    
    def test_state_or_province_property(self):
        """
        Test state_or_province property
        """
        test_value = 'cewqhvomepdwxfegomjh'
        self.instance.state_or_province = test_value
        self.assertEqual(self.instance.state_or_province, test_value)
    
    def test_postcode_property(self):
        """
        Test postcode property
        """
        test_value = 'hzjazxvnjveajaqwsbge'
        self.instance.postcode = test_value
        self.assertEqual(self.instance.postcode, test_value)
    
    def test_country_id_property(self):
        """
        Test country_id property
        """
        test_value = int(65)
        self.instance.country_id = test_value
        self.assertEqual(self.instance.country_id, test_value)
    
    def test_country_iso_code_property(self):
        """
        Test country_iso_code property
        """
        test_value = 'rawqafuligkgsfcrshvo'
        self.instance.country_iso_code = test_value
        self.assertEqual(self.instance.country_iso_code, test_value)
    
    def test_country_title_property(self):
        """
        Test country_title property
        """
        test_value = 'dinjtcijbqpyxyqhgyrx'
        self.instance.country_title = test_value
        self.assertEqual(self.instance.country_title, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(78.37976030072039)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(51.75439827643669)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_contact_telephone1_property(self):
        """
        Test contact_telephone1 property
        """
        test_value = 'wgftwnqymolhxwvtebkp'
        self.instance.contact_telephone1 = test_value
        self.assertEqual(self.instance.contact_telephone1, test_value)
    
    def test_contact_telephone2_property(self):
        """
        Test contact_telephone2 property
        """
        test_value = 'noivelzpffngeuycvqgq'
        self.instance.contact_telephone2 = test_value
        self.assertEqual(self.instance.contact_telephone2, test_value)
    
    def test_contact_email_property(self):
        """
        Test contact_email property
        """
        test_value = 'kjvzdzmnincawjvxzork'
        self.instance.contact_email = test_value
        self.assertEqual(self.instance.contact_email, test_value)
    
    def test_access_comments_property(self):
        """
        Test access_comments property
        """
        test_value = 'wixencziigxsakcwemle'
        self.instance.access_comments = test_value
        self.assertEqual(self.instance.access_comments, test_value)
    
    def test_related_url_property(self):
        """
        Test related_url property
        """
        test_value = 'ugpvjxttlsubfupjypwi'
        self.instance.related_url = test_value
        self.assertEqual(self.instance.related_url, test_value)
    
    def test_connections_property(self):
        """
        Test connections property
        """
        test_value = [None, None, None, None, None]
        self.instance.connections = test_value
        self.assertEqual(self.instance.connections, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = ChargingLocation.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = ChargingLocation.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

