"""
Test case for ChargingLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_producer_data.io.openchargemap.charginglocation import ChargingLocation
from open_charge_map_producer_data.io.openchargemap.connection import Connection
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
            poi_id=int(32),
            uuid='wlcjdtfzeycwaqtigwdo',
            data_provider_id=int(66),
            operator_id=int(26),
            operator_title='augriximucyfovdwbvap',
            usage_type_id=int(99),
            usage_type_title='hzseongiuvtyxjjzuxwj',
            usage_cost='eyrxjxtkwffbawmizulx',
            status_type_id=int(82),
            status_title='knnlahhgoqghattjduhu',
            is_operational=True,
            submission_status_type_id=int(4),
            submission_status_title='tzqkioatkjbbzelyhaco',
            data_quality_level=int(73),
            number_of_points=int(6),
            general_comments='mrifvpeezulcqxaajdbt',
            is_recently_verified=True,
            date_created=datetime.datetime.now(datetime.timezone.utc),
            date_last_status_update=datetime.datetime.now(datetime.timezone.utc),
            date_last_verified=datetime.datetime.now(datetime.timezone.utc),
            date_last_confirmed=datetime.datetime.now(datetime.timezone.utc),
            date_planned=datetime.datetime.now(datetime.timezone.utc),
            address_id=int(7),
            address_title='whebypsavyhdhfrlkgik',
            address_line1='upiuoqgjjlbvhsuxqifl',
            address_line2='bigltmnujirrxhqjvdxy',
            town='araqzdxwzxkixfrscysy',
            state_or_province='fmqhytzkzdclyaoeltgg',
            postcode='zhoncpcpbsenqeompvua',
            country_id=int(15),
            country_iso_code='tlllqxkvsqtaicmmostv',
            country_title='iirkgfwjopzmouecxnqk',
            latitude=float(5.5174513473599145),
            longitude=float(9.83766601770516),
            contact_telephone1='ktxsfwthelbmwjthavon',
            contact_telephone2='jlukhbhixxdsuqnowlya',
            contact_email='bcosucvcfomniwicpebh',
            access_comments='itfbvnzzpxledtzivvhi',
            related_url='qjualafnvztoqktyxfpa',
            connections=[None, None, None]
        )
        return instance

    
    def test_poi_id_property(self):
        """
        Test poi_id property
        """
        test_value = int(32)
        self.instance.poi_id = test_value
        self.assertEqual(self.instance.poi_id, test_value)
    
    def test_uuid_property(self):
        """
        Test uuid property
        """
        test_value = 'wlcjdtfzeycwaqtigwdo'
        self.instance.uuid = test_value
        self.assertEqual(self.instance.uuid, test_value)
    
    def test_data_provider_id_property(self):
        """
        Test data_provider_id property
        """
        test_value = int(66)
        self.instance.data_provider_id = test_value
        self.assertEqual(self.instance.data_provider_id, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = int(26)
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_operator_title_property(self):
        """
        Test operator_title property
        """
        test_value = 'augriximucyfovdwbvap'
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
        test_value = 'hzseongiuvtyxjjzuxwj'
        self.instance.usage_type_title = test_value
        self.assertEqual(self.instance.usage_type_title, test_value)
    
    def test_usage_cost_property(self):
        """
        Test usage_cost property
        """
        test_value = 'eyrxjxtkwffbawmizulx'
        self.instance.usage_cost = test_value
        self.assertEqual(self.instance.usage_cost, test_value)
    
    def test_status_type_id_property(self):
        """
        Test status_type_id property
        """
        test_value = int(82)
        self.instance.status_type_id = test_value
        self.assertEqual(self.instance.status_type_id, test_value)
    
    def test_status_title_property(self):
        """
        Test status_title property
        """
        test_value = 'knnlahhgoqghattjduhu'
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
        test_value = int(4)
        self.instance.submission_status_type_id = test_value
        self.assertEqual(self.instance.submission_status_type_id, test_value)
    
    def test_submission_status_title_property(self):
        """
        Test submission_status_title property
        """
        test_value = 'tzqkioatkjbbzelyhaco'
        self.instance.submission_status_title = test_value
        self.assertEqual(self.instance.submission_status_title, test_value)
    
    def test_data_quality_level_property(self):
        """
        Test data_quality_level property
        """
        test_value = int(73)
        self.instance.data_quality_level = test_value
        self.assertEqual(self.instance.data_quality_level, test_value)
    
    def test_number_of_points_property(self):
        """
        Test number_of_points property
        """
        test_value = int(6)
        self.instance.number_of_points = test_value
        self.assertEqual(self.instance.number_of_points, test_value)
    
    def test_general_comments_property(self):
        """
        Test general_comments property
        """
        test_value = 'mrifvpeezulcqxaajdbt'
        self.instance.general_comments = test_value
        self.assertEqual(self.instance.general_comments, test_value)
    
    def test_is_recently_verified_property(self):
        """
        Test is_recently_verified property
        """
        test_value = True
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
        test_value = int(7)
        self.instance.address_id = test_value
        self.assertEqual(self.instance.address_id, test_value)
    
    def test_address_title_property(self):
        """
        Test address_title property
        """
        test_value = 'whebypsavyhdhfrlkgik'
        self.instance.address_title = test_value
        self.assertEqual(self.instance.address_title, test_value)
    
    def test_address_line1_property(self):
        """
        Test address_line1 property
        """
        test_value = 'upiuoqgjjlbvhsuxqifl'
        self.instance.address_line1 = test_value
        self.assertEqual(self.instance.address_line1, test_value)
    
    def test_address_line2_property(self):
        """
        Test address_line2 property
        """
        test_value = 'bigltmnujirrxhqjvdxy'
        self.instance.address_line2 = test_value
        self.assertEqual(self.instance.address_line2, test_value)
    
    def test_town_property(self):
        """
        Test town property
        """
        test_value = 'araqzdxwzxkixfrscysy'
        self.instance.town = test_value
        self.assertEqual(self.instance.town, test_value)
    
    def test_state_or_province_property(self):
        """
        Test state_or_province property
        """
        test_value = 'fmqhytzkzdclyaoeltgg'
        self.instance.state_or_province = test_value
        self.assertEqual(self.instance.state_or_province, test_value)
    
    def test_postcode_property(self):
        """
        Test postcode property
        """
        test_value = 'zhoncpcpbsenqeompvua'
        self.instance.postcode = test_value
        self.assertEqual(self.instance.postcode, test_value)
    
    def test_country_id_property(self):
        """
        Test country_id property
        """
        test_value = int(15)
        self.instance.country_id = test_value
        self.assertEqual(self.instance.country_id, test_value)
    
    def test_country_iso_code_property(self):
        """
        Test country_iso_code property
        """
        test_value = 'tlllqxkvsqtaicmmostv'
        self.instance.country_iso_code = test_value
        self.assertEqual(self.instance.country_iso_code, test_value)
    
    def test_country_title_property(self):
        """
        Test country_title property
        """
        test_value = 'iirkgfwjopzmouecxnqk'
        self.instance.country_title = test_value
        self.assertEqual(self.instance.country_title, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(5.5174513473599145)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(9.83766601770516)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_contact_telephone1_property(self):
        """
        Test contact_telephone1 property
        """
        test_value = 'ktxsfwthelbmwjthavon'
        self.instance.contact_telephone1 = test_value
        self.assertEqual(self.instance.contact_telephone1, test_value)
    
    def test_contact_telephone2_property(self):
        """
        Test contact_telephone2 property
        """
        test_value = 'jlukhbhixxdsuqnowlya'
        self.instance.contact_telephone2 = test_value
        self.assertEqual(self.instance.contact_telephone2, test_value)
    
    def test_contact_email_property(self):
        """
        Test contact_email property
        """
        test_value = 'bcosucvcfomniwicpebh'
        self.instance.contact_email = test_value
        self.assertEqual(self.instance.contact_email, test_value)
    
    def test_access_comments_property(self):
        """
        Test access_comments property
        """
        test_value = 'itfbvnzzpxledtzivvhi'
        self.instance.access_comments = test_value
        self.assertEqual(self.instance.access_comments, test_value)
    
    def test_related_url_property(self):
        """
        Test related_url property
        """
        test_value = 'qjualafnvztoqktyxfpa'
        self.instance.related_url = test_value
        self.assertEqual(self.instance.related_url, test_value)
    
    def test_connections_property(self):
        """
        Test connections property
        """
        test_value = [None, None, None]
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

