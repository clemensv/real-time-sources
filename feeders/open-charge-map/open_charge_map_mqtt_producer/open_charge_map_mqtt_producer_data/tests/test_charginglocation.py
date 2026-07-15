"""
Test case for ChargingLocation
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from open_charge_map_mqtt_producer_data.io.openchargemap.charginglocation import ChargingLocation
from open_charge_map_mqtt_producer_data.io.openchargemap.connection import Connection
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
            poi_id=int(22),
            uuid='bacvaieggxehvmzjqfci',
            data_provider_id=int(14),
            operator_id=int(40),
            operator_title='zhzllmvzhfkstpleqgji',
            usage_type_id=int(9),
            usage_type_title='afxxaunrhlibzvemzfwg',
            usage_cost='wolcviaifpvzbgcgmzpf',
            status_type_id=int(87),
            status_title='lfzmopuhjlzhwxukmeob',
            is_operational=True,
            submission_status_type_id=int(21),
            submission_status_title='kuiyqquvdbbfzqaazwvb',
            data_quality_level=int(39),
            number_of_points=int(23),
            general_comments='nzufwkbtvjhpjwyovzls',
            is_recently_verified=False,
            date_created=datetime.datetime.now(datetime.timezone.utc),
            date_last_status_update=datetime.datetime.now(datetime.timezone.utc),
            date_last_verified=datetime.datetime.now(datetime.timezone.utc),
            date_last_confirmed=datetime.datetime.now(datetime.timezone.utc),
            date_planned=datetime.datetime.now(datetime.timezone.utc),
            address_id=int(83),
            address_title='rypkkkqlsdmmykmrnnss',
            address_line1='kskbxsbqwrsialvvdzwi',
            address_line2='bioravatonlxrdfkvtcm',
            town='mycsgcikhoubbvbcgwtx',
            state_or_province='djmspowkyisjwwuwrbrd',
            postcode='snfdcmibjazbosgljlum',
            country_id=int(28),
            country_iso_code='dhpclvovatseuwjtjtsm',
            country_title='kylihdvmkbnkepzktyed',
            latitude=float(96.27547340431354),
            longitude=float(0.8295924492855877),
            contact_telephone1='naihgqceoxxjjtxzamwy',
            contact_telephone2='tcmtflbglbarwokhlckm',
            contact_email='zuwsbwrkfefrcqzyfkga',
            access_comments='nrmffzmbbrnonnlxrtqe',
            related_url='ysheygdejxvjhlojofly',
            connections=[None, None, None, None, None]
        )
        return instance

    
    def test_poi_id_property(self):
        """
        Test poi_id property
        """
        test_value = int(22)
        self.instance.poi_id = test_value
        self.assertEqual(self.instance.poi_id, test_value)
    
    def test_uuid_property(self):
        """
        Test uuid property
        """
        test_value = 'bacvaieggxehvmzjqfci'
        self.instance.uuid = test_value
        self.assertEqual(self.instance.uuid, test_value)
    
    def test_data_provider_id_property(self):
        """
        Test data_provider_id property
        """
        test_value = int(14)
        self.instance.data_provider_id = test_value
        self.assertEqual(self.instance.data_provider_id, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = int(40)
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_operator_title_property(self):
        """
        Test operator_title property
        """
        test_value = 'zhzllmvzhfkstpleqgji'
        self.instance.operator_title = test_value
        self.assertEqual(self.instance.operator_title, test_value)
    
    def test_usage_type_id_property(self):
        """
        Test usage_type_id property
        """
        test_value = int(9)
        self.instance.usage_type_id = test_value
        self.assertEqual(self.instance.usage_type_id, test_value)
    
    def test_usage_type_title_property(self):
        """
        Test usage_type_title property
        """
        test_value = 'afxxaunrhlibzvemzfwg'
        self.instance.usage_type_title = test_value
        self.assertEqual(self.instance.usage_type_title, test_value)
    
    def test_usage_cost_property(self):
        """
        Test usage_cost property
        """
        test_value = 'wolcviaifpvzbgcgmzpf'
        self.instance.usage_cost = test_value
        self.assertEqual(self.instance.usage_cost, test_value)
    
    def test_status_type_id_property(self):
        """
        Test status_type_id property
        """
        test_value = int(87)
        self.instance.status_type_id = test_value
        self.assertEqual(self.instance.status_type_id, test_value)
    
    def test_status_title_property(self):
        """
        Test status_title property
        """
        test_value = 'lfzmopuhjlzhwxukmeob'
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
        test_value = int(21)
        self.instance.submission_status_type_id = test_value
        self.assertEqual(self.instance.submission_status_type_id, test_value)
    
    def test_submission_status_title_property(self):
        """
        Test submission_status_title property
        """
        test_value = 'kuiyqquvdbbfzqaazwvb'
        self.instance.submission_status_title = test_value
        self.assertEqual(self.instance.submission_status_title, test_value)
    
    def test_data_quality_level_property(self):
        """
        Test data_quality_level property
        """
        test_value = int(39)
        self.instance.data_quality_level = test_value
        self.assertEqual(self.instance.data_quality_level, test_value)
    
    def test_number_of_points_property(self):
        """
        Test number_of_points property
        """
        test_value = int(23)
        self.instance.number_of_points = test_value
        self.assertEqual(self.instance.number_of_points, test_value)
    
    def test_general_comments_property(self):
        """
        Test general_comments property
        """
        test_value = 'nzufwkbtvjhpjwyovzls'
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
        test_value = int(83)
        self.instance.address_id = test_value
        self.assertEqual(self.instance.address_id, test_value)
    
    def test_address_title_property(self):
        """
        Test address_title property
        """
        test_value = 'rypkkkqlsdmmykmrnnss'
        self.instance.address_title = test_value
        self.assertEqual(self.instance.address_title, test_value)
    
    def test_address_line1_property(self):
        """
        Test address_line1 property
        """
        test_value = 'kskbxsbqwrsialvvdzwi'
        self.instance.address_line1 = test_value
        self.assertEqual(self.instance.address_line1, test_value)
    
    def test_address_line2_property(self):
        """
        Test address_line2 property
        """
        test_value = 'bioravatonlxrdfkvtcm'
        self.instance.address_line2 = test_value
        self.assertEqual(self.instance.address_line2, test_value)
    
    def test_town_property(self):
        """
        Test town property
        """
        test_value = 'mycsgcikhoubbvbcgwtx'
        self.instance.town = test_value
        self.assertEqual(self.instance.town, test_value)
    
    def test_state_or_province_property(self):
        """
        Test state_or_province property
        """
        test_value = 'djmspowkyisjwwuwrbrd'
        self.instance.state_or_province = test_value
        self.assertEqual(self.instance.state_or_province, test_value)
    
    def test_postcode_property(self):
        """
        Test postcode property
        """
        test_value = 'snfdcmibjazbosgljlum'
        self.instance.postcode = test_value
        self.assertEqual(self.instance.postcode, test_value)
    
    def test_country_id_property(self):
        """
        Test country_id property
        """
        test_value = int(28)
        self.instance.country_id = test_value
        self.assertEqual(self.instance.country_id, test_value)
    
    def test_country_iso_code_property(self):
        """
        Test country_iso_code property
        """
        test_value = 'dhpclvovatseuwjtjtsm'
        self.instance.country_iso_code = test_value
        self.assertEqual(self.instance.country_iso_code, test_value)
    
    def test_country_title_property(self):
        """
        Test country_title property
        """
        test_value = 'kylihdvmkbnkepzktyed'
        self.instance.country_title = test_value
        self.assertEqual(self.instance.country_title, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(96.27547340431354)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(0.8295924492855877)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_contact_telephone1_property(self):
        """
        Test contact_telephone1 property
        """
        test_value = 'naihgqceoxxjjtxzamwy'
        self.instance.contact_telephone1 = test_value
        self.assertEqual(self.instance.contact_telephone1, test_value)
    
    def test_contact_telephone2_property(self):
        """
        Test contact_telephone2 property
        """
        test_value = 'tcmtflbglbarwokhlckm'
        self.instance.contact_telephone2 = test_value
        self.assertEqual(self.instance.contact_telephone2, test_value)
    
    def test_contact_email_property(self):
        """
        Test contact_email property
        """
        test_value = 'zuwsbwrkfefrcqzyfkga'
        self.instance.contact_email = test_value
        self.assertEqual(self.instance.contact_email, test_value)
    
    def test_access_comments_property(self):
        """
        Test access_comments property
        """
        test_value = 'nrmffzmbbrnonnlxrtqe'
        self.instance.access_comments = test_value
        self.assertEqual(self.instance.access_comments, test_value)
    
    def test_related_url_property(self):
        """
        Test related_url property
        """
        test_value = 'ysheygdejxvjhlojofly'
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

